// Get the DOM elements
const chartCanvas = document.getElementById("cluster-chart");
const form = document.getElementById("segmentation-parameters-form");
const formErrors = document.getElementById(
    "segmentation-parameters-form-errors"
);
const downloadButton = document.getElementById(
    "download-segmentation-report-button"
);
const loadingMessage = document.getElementById("segmentation-message");

formErrors.style.display = "none";

// Get chart context
const context = chartCanvas.getContext("2d");

// Define color palette
const COLORS = [
    "#04FF00",
    "#16CA1F",
    "#F3722C",
    "#D90429",
    "#FFBA08",
    "#0E99A3",
    "#1D5B79",
    "#4059AD",
    "#613DC1",
    "#9D0191",
    "#C0392B",
    "#F39C12",
    "#8E44AD",
    "#27AE60",
    "#3498DB",
];

Chart.register(ChartDataLabels);

// Initialize the chart
const clusterChart = new Chart(context, {
    type: "doughnut", // Type of chart
    data: {
        labels: ["No data yet"], // Will be populated with cluster labels
        datasets: [
            {
                label: "Customer Count",
                data: [1], // Will be populated with cluster count values
                backgroundColor: "#888888",
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
                    font: {
                        weight: "bold",
                    },
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
                font: { size: 14 },
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
            datalabels: {
                anchor: "center", // Position the label at the center of the slice
                align: "center",
                color: "#FFFFFF",
                font: { weight: "bold", size: 12 },
                formatter: (value, ctx) => {
                    const dataset = ctx.chart.data.datasets[0].data;
                    const total = dataset.reduce((a, b) => a + b, 0);
                    const percentage = ((value / total) * 100).toFixed(2);
                    return `${percentage}%`;
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
                return `Cluster ${parseInt(key) + 1} (Avg.: ${avgMetric})`;
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

            clusterChart.data.datasets[0].backgroundColor = COLORS;

            timestamp = new Date().toLocaleString("en-GB", {
                weekday: "short",
                year: "numeric",
                month: "short",
                day: "2-digit",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
                hour12: true,
            });

            // Set the subtitle as the chosen metric
            clusterChart.options.plugins.subtitle.text = [
                `Based on ${data.chosen_metric}`,
                `Generated on ${timestamp} using OptiPrice ©`,
            ];

            // Update the chart
            clusterChart.update();

            // Stop the polling for cluster data and reset the polling ID
            clearInterval(pollingInterval);
            pollingInterval = null;

            downloadButton.style.display = "block";
            loadingMessage.style.display = "none";
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
            downloadButton.style.display = "none";
            loadingMessage.style.display = "block";
            formErrors.style.display = "none";

            // Start polling every 3 seconds
            if (!pollingInterval) {
                pollingInterval = setInterval(fetchClusterProfiles, 3000);
            }
        } else {
            console.error("Clustering failed.");
            downloadButton.style.display = "none";
            loadingMessage.style.display = "none";

            if (data.message && data.message.length > 0) {
                const errorMessage = document.createElement("div");
                errorMessage.textContent = data.message;
                formErrors.appendChild(errorMessage);
                formErrors.style.display = "block";
            } else {
                formErrors.style.display = "none";
            }
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
        const response = await fetch("save_to_db", {
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
