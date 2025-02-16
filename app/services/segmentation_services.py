import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


class SegmentationService:
    @staticmethod
    def segment_customers(df, num_of_clusters, chosen_metric):
        """Performs KMeans Clustering and returns a DataFrame with the chosen metric and cluster labels."""
        df_clustering = df[[chosen_metric]].copy()

        n_clusters = (
            SegmentationService.get_optimal_num_of_clusters(df_clustering)
            if num_of_clusters == "auto"
            else int(num_of_clusters)
        )

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df_clustering["Cluster"] = kmeans.fit_predict(df_clustering)

        return df_clustering

    @staticmethod
    def get_optimal_num_of_clusters(df_clustering):
        """Returns the number of clusters with the highest silhouette score."""
        cluster_range = range(2, 11)
        silhouette_scores = []

        for k in cluster_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(df_clustering)
            labels = kmeans.labels_
            silhouette_avg = silhouette_score(df_clustering, labels)
            silhouette_scores.append(silhouette_avg)

        return cluster_range[np.argmax(silhouette_scores)]

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
