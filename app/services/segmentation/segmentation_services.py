import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler

from app import db
from app.models.Cluster.model import Cluster
from app.models.Segmentation.model import Segmentation


class SegmentationService:
    @staticmethod
    def save_to_db(dataset_file_id, chosen_metric, cluster_counts, metric_averages):
        """Saves the segmentation and cluster details to the database."""

        # Save segmentation details to the db
        num_of_clusters = len(cluster_counts)

        segmentation = Segmentation(
            chosen_metric=chosen_metric,
            num_of_clusters=num_of_clusters,
            dataset_file_id=dataset_file_id,
        )
        db.session.add(segmentation)
        db.session.commit()
        segmentation_id = segmentation.id

        # Save cluster details to the db
        clusters = []
        for cluster_id, cluster_count in cluster_counts.items():
            metric_avg = metric_averages.get(cluster_id, None)

            cluster = Cluster(
                segmentation_id=segmentation_id,
                cluster_id=int(cluster_id),
                cluster_count=int(cluster_count),
                metric_avg=metric_avg,
            )
            clusters.append(cluster)

        db.session.add_all(clusters)
        db.session.commit()

    @staticmethod
    def segment_customers(df, num_of_clusters, chosen_metric):
        """Performs KMeans Clustering and returns cluster profiles (cluster counts and metric averages)."""
        try:
            # Set a copy of the original dataset with the chosen metric
            df_original = df[[chosen_metric]].copy()

            # Scale the dataset with the chosen metric
            df_clustering = df[[chosen_metric]].copy()
            df_clustering = SegmentationService.scale_dataset(df_clustering)

            # Number of clusters
            n_clusters = (
                SegmentationService.get_optimal_num_of_clusters(df_clustering)
                if num_of_clusters == "auto"
                else int(num_of_clusters)
            )

            if n_clusters is None or n_clusters < 2:
                return None, None

            # Initialize KMeans model
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)

            # Cluster the data and return labels
            df_original["Cluster"] = kmeans.fit_predict(
                df_clustering
            )  # this line is where the error starts

            # Calculate the cluster counts and the metric averages
            cluster_counts, metric_averages = SegmentationService.get_cluster_profiles(
                df_original, chosen_metric
            )

            # Return the cluster counts and metric averages dicts
            return cluster_counts, metric_averages
        except Exception as e:
            print(f"Error when clustering: {str(e)}")

    @staticmethod
    def get_optimal_num_of_clusters(df_clustering):
        """Returns the number of clusters with the highest silhouette score."""
        try:
            cluster_range = range(2, 11)
            silhouette_scores = []

            for k in cluster_range:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                labels = kmeans.fit_predict(df_clustering)

                # Check if less than 2 clusters were found
                if len(set(labels)) < 2:
                    print(f"Only {len(set(labels))} distinct clusters found.")
                    return None

                silhouette_avg = silhouette_score(df_clustering, labels)
                silhouette_scores.append(silhouette_avg)

            n_clusters = cluster_range[np.argmax(silhouette_scores)]
            # print(f"Optimal k from sil score:{n_clusters}")
            return n_clusters
        except Exception as e:
            print(f"Error during sil score: {str(e)}")
            return None

    @staticmethod
    def scale_dataset(df):
        """Scales the dataset."""
        scaler = MinMaxScaler()
        df_scaled = df.copy()
        numcols = df.select_dtypes(include=[np.number]).columns.tolist()
        df_scaled[numcols] = scaler.fit_transform(df_scaled[numcols])

        return df_scaled

    @staticmethod
    def get_cluster_profiles(df_original, chosen_metric):
        """Calculates the cluster counts and metric averages."""
        cluster_counts = df_original["Cluster"].value_counts().to_dict()
        metric_averages = df_original.groupby("Cluster")[chosen_metric].mean().to_dict()

        return cluster_counts, metric_averages

    @staticmethod
    def engineer_features(df):
        """Engineers totals and averages for segmentation."""
        df_original = df[["Customer ID", "Order Date", "Quantity", "Sales"]]

        # Engineering totals for Quantity, Sales, and Visits
        df_totals = SegmentationService.engineer_totals(df_original)

        # Engineering Year-Week, Year-Month, Year-Quarter columns
        df_timeframes = SegmentationService.engineer_timeframes(df_original)

        # Engineering weekly averages for Quantity, Sales, and Visits
        df_weekly = SegmentationService.engineer_weekly_avgs(df_timeframes)

        # Engineering monthly averages for Quantity, Sales, and Visits
        df_monthly = SegmentationService.engineer_monthly_avgs(df_timeframes)

        # Engineering quarterly averages for Quantity, Sales, and Visits
        df_quarterly = SegmentationService.engineer_quarterly_avgs(df_timeframes)

        # Merging all features into a single dataframe
        df_final = SegmentationService.merge_all_features(
            df_totals, df_weekly, df_monthly, df_quarterly
        )

        return df_final

    @staticmethod
    def engineer_totals(df_original):
        """Engineers total sales, quantity, and visits from the dataset"""
        # Creating the total sales, quantity, and visits
        df_totals = (
            df_original.groupby("Customer ID")
            .agg(
                {
                    "Order Date": "nunique",
                    "Sales": "sum",
                    "Quantity": "sum",
                }
            )
            .reset_index()
        )

        # Renaming columns appropriately
        df_totals.rename(
            columns={
                "Order Date": "Total Visits",
                "Sales": "Total Sales",
                "Quantity": "Total Quantity",
            },
            inplace=True,
        )

        return df_totals

    @staticmethod
    def engineer_timeframes(df_original):
        """Engineers Year-Week, Year-Month, and Year-Quarter features."""
        df_timeframes = df_original.copy()

        # Year-Week
        df_timeframes["Year-Week"] = df_timeframes["Order Date"].dt.strftime("%Y-%U")

        # Year-Month
        df_timeframes["Year-Month"] = df_timeframes["Order Date"].dt.strftime("%Y-%m")

        # Year-Quarter
        df_timeframes["Year-Quarter"] = df_timeframes["Order Date"].dt.to_period("Q")

        return df_timeframes

    @staticmethod
    def engineer_weekly_avgs(df_timeframes):
        """Engineers weekly averages of sales, quantity, and visits from the dataset."""
        # Calculating total per week for each customer
        df_weekly = (
            df_timeframes.groupby(["Customer ID", "Year-Week"])
            .agg(
                **{
                    "Weekly Visits": ("Order Date", "nunique"),
                    "Weekly Sales": ("Sales", "sum"),
                    "Weekly Quantity": ("Quantity", "sum"),
                }
            )
            .reset_index()
        )

        # Calculating the weekly averages
        df_weekly = (
            df_weekly.groupby("Customer ID")
            .agg(
                **{
                    "Average Weekly Visits": ("Weekly Visits", "mean"),
                    "Average Weekly Sales": ("Weekly Sales", "mean"),
                    "Average Weekly Quantity": ("Weekly Quantity", "mean"),
                }
            )
            .reset_index()
        )

        return df_weekly

    @staticmethod
    def engineer_monthly_avgs(df_timeframes):
        """Engineers monthly averages of sales, quantity, and visits from the dataset."""
        # Calculating total per month for each customer
        df_monthly = (
            df_timeframes.groupby(["Customer ID", "Year-Month"])
            .agg(
                **{
                    "Monthly Visits": ("Order Date", "nunique"),
                    "Monthly Sales": ("Sales", "sum"),
                    "Monthly Quantity": ("Quantity", "sum"),
                }
            )
            .reset_index()
        )

        # Calculating the monthly averages
        df_monthly = (
            df_monthly.groupby("Customer ID")
            .agg(
                **{
                    "Average Monthly Visits": ("Monthly Visits", "mean"),
                    "Average Monthly Sales": ("Monthly Sales", "mean"),
                    "Average Monthly Quantity": ("Monthly Quantity", "mean"),
                }
            )
            .reset_index()
        )

        return df_monthly

    @staticmethod
    def engineer_quarterly_avgs(df_timeframes):
        """Engineers quarterly averages of sales, quantity, and visits from the dataset."""
        # Calculating total per quarter for each customer
        df_quarterly = (
            df_timeframes.groupby(["Customer ID", "Year-Quarter"])
            .agg(
                **{
                    "Quarterly Visits": ("Order Date", "nunique"),
                    "Quarterly Sales": ("Sales", "sum"),
                    "Quarterly Quantity": ("Quantity", "sum"),
                }
            )
            .reset_index()
        )

        # Calculating the quarterly averages
        df_quarterly = (
            df_quarterly.groupby("Customer ID")
            .agg(
                **{
                    "Average Quarterly Visits": ("Quarterly Visits", "mean"),
                    "Average Quarterly Sales": ("Quarterly Sales", "mean"),
                    "Average Quarterly Quantity": ("Quarterly Quantity", "mean"),
                }
            )
            .reset_index()
        )

        return df_quarterly

    @staticmethod
    def merge_all_features(*dfs):
        """Horizontally merges multiple dataframes by Customer ID into a single dataset."""

        df_overall = dfs[0]

        # Adding each set of averages one by one to the set of totals
        for df in dfs[1:]:
            df_overall = df_overall.merge(df, on="Customer ID", how="left")

        # Replacing any NaN values that may form due to left join
        df_overall.fillna(0, inplace=True)

        return df_overall
