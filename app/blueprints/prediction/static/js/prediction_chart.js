// Get the DOM elements
const chartCanvas = document.getElementById("prediction-chart");
const form = document.getElementById("prediction-file-upload-form");
const downloadButton = document.getElementById(
    "download-prediction-report-button"
);

// Get chart context
const context = chartCanvas.getContext("2d");

// Define color palette
const COLORS = ["#EF582E", "#00A878", "#00A1E4", "#F4D35E", "#BC63F8"];

// Initialize the chart
const predictionChart = new Chart(context, {
    type: "doughnut", // Type of chart
    data: {
        labels: [], // Will be populated with cluster labels
        datasets: [
            {
                label: "Predicted Sales",
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
                text: "Predicted Sales",
                font: { size: 22 },
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

// Function to fetch predicted sales (weekly, monthly, quarterly) from the server
async function fetchPredictions() {
    try {
        const response = await fetch("get_predictions"); // Hit the endpoint
        const data = await response.json(); // Parse the JSON object

        // // If the response was not empty, update the chart UI
        // if (data?.cluster_counts) {
        //     // Cluster Keys (0, 1, 2, ...)
        //     const clusterKeys = Object.keys(data.cluster_counts);

        //     // Set the keys as the labels, but start from 1
        //     clusterChart.data.labels = clusterKeys.map((key) => {
        //         const avgMetric =
        //             data.metric_averages?.[key]?.toFixed(2) || "N/A";
        //         return `Cluster ${parseInt(key) + 1} (Avg :${avgMetric})`;
        //     });

        //     // Set the chart sections as the cluster counts
        //     clusterChart.data.datasets[0].data = clusterKeys.map(
        //         (key) => data.cluster_counts[key]
        //     );

        //     // Set the tooptip to show the percentage of customers in each cluster
        //     // NOTE: Tooltips are the texts shown when hovering on each section of the chart
        //     clusterChart.options.plugins.tooltip.callbacks.label = (
        //         tooltipItem
        //     ) => {
        //         const clusterKey = clusterKeys[tooltipItem.dataIndex];
        //         return `${
        //             data.cluster_percentages?.[clusterKey]?.toFixed(2) || "N/A"
        //         }%`;
        //     };

        //     // Set the subtitle as the chosen metric
        //     clusterChart.options.plugins.subtitle.text = `Based on ${data.chosen_metric}`;

        //     // Update the chart
        //     clusterChart.update();

        //     // Stop the polling for cluster data and reset the polling ID
        //     clearInterval(pollingInterval);
        //     pollingInterval = null;
        // }
    } catch (error) {
        console.error("Error fetching predictions:", error);
    }
}

// Handle the form submission (file upload form)
form.addEventListener("submit", async (event) => {
    // Prevent default submission
    event.preventDefault();

    try {
        // Submit the form inputs to the endpoint
        const response = await fetch("upload", {
            method: "POST",
            body: new FormData(form),
        });

        if (response.ok) {
            // Parse the JSON response
            const data = await response.json();
            console.log("File uploaded successfully", data);
        } else {
            console.error("Failed to upload file.");
        }
    } catch (error) {
        console.error("Error during file upload:", error);
    }
});

// Function to download the chart
async function downloadChart(event) {
    // Prevent default submission
    event.preventDefault();

    // Convert the chart UI into a string
    const imageUrl = predictionChart.toBase64Image();

    // Get the current timestamp
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");

    // Create a download link with the image URL and click it
    const downloadLink = document.createElement("a");
    downloadLink.href = imageUrl;
    downloadLink.download = `prediction-report-chart-${timestamp}.png`;
    downloadLink.click();

    try {
        // Trigger the endpoint to save predictions in the db as well
        const response = await fetch("prediction/save_to_db", {
            method: "POST",
        });

        // IF unsuccessful when saving to db, throw error
        if (!response.ok)
            throw new Error("Failed to save the prediction report.");

        // Else simply log the success message
        console.log((await response.json()).message);
    } catch (error) {
        console.error("Error saving prediction report:", error);
    }
}

// Trigger downloadChart() when the Download Report button is clicked
downloadButton.addEventListener("click", downloadChart);
