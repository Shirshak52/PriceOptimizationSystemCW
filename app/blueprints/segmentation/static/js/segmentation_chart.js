// Get the DOM elements
const chartCanvas = document.getElementById("cluster-chart");
const form = document.getElementById("segmentation-parameters-form");
const downloadButton = document.getElementById(
    "download-segmentation-report-button"
);

// Get chart context
const context = chartCanvas.getContext("2d");

// Define color palette
const COLORS = [
    "#16CA1F",
    "#097248",
    "#007A25",
    "#0E99A3",
    "#1D5B79",
    "#4059AD",
    "#613DC1",
    "#9D0191",
    "#D90429",
    "#F3722C",
    "#FFBA08",
    "#97CC04",
    "#7C3E66",
    "#582F0E",
    "#5A5A66",
];

// Initialize the chart
const clusterChart = new Chart(context, {
    type: "doughnut", // Type of chart
    data: {
        labels: [], // Will be populated with cluster labels
        datasets: [
            {
                label: "Customer Count",
                data: [], // Will be populated with cluster count values
                backgroundColor: COLORS,
                borderColor: "#202020", // Border color of each section of the chart
                hoverOffset: 10,
                rotation: 50,
                spacing: 10,
            },
        ],
    },
    options: {
        responsive: true,
        datasets: {
            doughnut: {
                radius: "90%",
                borderRadius: 15,
            },
        },
        plugins: {
            legend: {
                position: "left",
                labels: {
                    color: "#FFFFFF",
                    padding: 20,
                },
            },
            title: {
                display: true,
                text: "Customer Composition",
                font: { size: 22 },
                color: "#FFFFFF",
            },
            subtitle: {
                display: true,
                text: "",
                font: { size: 18 },
                color: "#FFFFFF",
            },
            tooltip: {
                callbacks: {
                    label: function (tooltipItem) {
                        const total = clusterChart.data.datasets[0].data.reduce(
                            (a, b) => a + b,
                            0
                        );
                        const count =
                            clusterChart.data.datasets[0].data[
                                tooltipItem.dataIndex
                            ];
                        const percentage = ((count / total) * 100).toFixed(2);
                        return `${percentage}%`;
                    },
                },
            },
        },
    },
});

// Declare a polling interval
let pollingInterval;

// Function to fetch cluster profiles (counts and metric averages) from the server
async function fetchClusterProfiles() {
    try {
        const response = await fetch("get_cluster_profiles"); // Hit the endpoint
        const data = await response.json(); // Parse the JSON object

        // If the response was not empty, update the chart UI
        if (data?.cluster_counts) {
            // Cluster Keys (0, 1, 2, ...)
            const clusterKeys = Object.keys(data.cluster_counts);

            // Set the keys as the labels, but start from 1
            clusterChart.data.labels = clusterKeys.map((key) => {
                const avgMetric =
                    data.metric_averages?.[key]?.toFixed(2) || "N/A";
                return `Cluster ${parseInt(key) + 1} (Avg :${avgMetric})`;
            });

            // Set the chart sections as the cluster counts
            clusterChart.data.datasets[0].data = clusterKeys.map(
                (key) => data.cluster_counts[key]
            );

            // Set the tooptip to show the percentage of customers in each cluster
            // NOTE: Tooltips are the texts shown when hovering on each section of the chart
            clusterChart.options.plugins.tooltip.callbacks.label = (
                tooltipItem
            ) => {
                const clusterKey = clusterKeys[tooltipItem.dataIndex];
                return `${
                    data.cluster_percentages?.[clusterKey]?.toFixed(2) || "N/A"
                }%`;
            };

            // Set the subtitle as the chosen metric
            clusterChart.options.plugins.subtitle.text = `Based on ${data.chosen_metric}`;

            // Update the chart
            clusterChart.update();

            // Stop the polling for cluster data and reset the polling ID
            clearInterval(pollingInterval);
            pollingInterval = null;
        }
    } catch (error) {
        console.error("Error fetching cluster profiles:", error);
    }
}

// Handle the form submission (of chosen metric and number of clusters)
form.addEventListener("submit", async (event) => {
    // Prevent default submission
    event.preventDefault();

    try {
        // Submit the form inputs to the endpoint
        const response = await fetch("cluster_customers", {
            method: "POST",
            body: new FormData(form),
        });

        // Parse the JSON object
        const data = await response.json();

        // If succesful clustering, start polling for cluster data
        if (data.success) {
            console.log("Successfully clustered, starting polling...");

            // Start polling every 3 seconds
            if (!pollingInterval) {
                pollingInterval = setInterval(fetchClusterProfiles, 3000);
            }
        } else {
            console.error("Clustering failed.");
        }
    } catch (error) {
        console.error("Error submitting form:", error);
    }
});

// Function to download the chart
async function downloadChart(event) {
    // Prevent default submission
    event.preventDefault();

    // Convert the chart UI into a string
    const imageUrl = clusterChart.toBase64Image();

    // Get the current timestamp
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");

    // Create a download link with the image URL and click it
    const downloadLink = document.createElement("a");
    downloadLink.href = imageUrl;
    downloadLink.download = `segmentation-report-chart-${timestamp}.png`;
    downloadLink.click();

    try {
        // Trigger the endpoint to save clustering data in the db as well
        const response = await fetch("save_segmentation_to_db", {
            method: "POST",
        });

        // IF unsuccessful when saving to db, throw error
        if (!response.ok)
            throw new Error("Failed to save the segmentation report.");

        // Else simply log the success message
        console.log((await response.json()).message);
    } catch (error) {
        console.error("Error saving segmentation report:", error);
    }
}

// Trigger downloadChart() when the Download Report button is clicked
downloadButton.addEventListener("click", downloadChart);
