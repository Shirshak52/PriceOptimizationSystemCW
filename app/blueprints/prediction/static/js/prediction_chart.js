// Get the DOM elements
const chartCanvas = document.getElementById("prediction-chart");
const form = document.getElementById("prediction-file-upload-form");
const formErrors = document.getElementById(
    "prediction-file-upload-form-errors"
);
const downloadButton = document.getElementById(
    "download-prediction-report-button"
);

formErrors.style.display = "none";

// Get chart context
const context = chartCanvas.getContext("2d");

// Define color palette
const COLORS = ["#16CA1F", "#34D399", "#60A5FA "];

// Initialize the chart
const predictionChart = new Chart(context, {
    type: "bar", // Type of chart
    data: {
        labels: [], // Will be populated with prediction labels
        datasets: [
            {
                label: "Predicted Sales",
                data: [], // Will be populated with weekly prediction value
                backgroundColor: COLORS,
                borderColor: "#202020",
                borderWidth: 1,
            },
        ],
    },
    options: {
        responsive: true,
        barThickness: 50,
        animations: {
            duration: 3000,
            easing: "easeOutQuart",
            x: {
                from: false,
            },
        },

        scales: {
            y: {
                beginAtZero: true, // Ensure the y-axis starts at 0
                grid: {
                    color: "#FFFFFF", // Gridline color
                },
                ticks: {
                    color: "#FFFFFF",
                },
            },
            x: {
                grid: {
                    display: false,
                },
                ticks: {
                    color: "#FFFFFF",
                },
            },
        },
        plugins: {
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: "Predicted Sales",
                font: { size: 22 },
                color: "#FFFFFF",
                padding: 20,
            },
            tooltip: {
                callbacks: {
                    label: function (tooltipItem) {
                        const value = tooltipItem.raw;
                        return `Prediction: ${value.toFixed(2)}`;
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

        // If the response was not empty, update the chart UI
        if (
            data?.prediction_weekly ||
            data?.prediction_monthly ||
            data?.prediction_quarterly
        ) {
            // Set the labels for each predicted value
            const predictionLabels = [
                "Next Week",
                "Next Month",
                "Next Quarter",
            ];
            predictionChart.data.labels = predictionLabels;

            // Set the data values from the fetched predictions
            predictionChart.data.datasets[0].data = [
                data.prediction_weekly || 0,
                data.prediction_monthly || 0,
                data.prediction_quarterly || 0,
            ];

            // Update the chart
            predictionChart.update();

            // Stop the polling for predictions and reset the polling ID
            clearInterval(pollingInterval);
            pollingInterval = null;
        }
    } catch (error) {
        console.error("Error fetching predictions:", error);
    }
}

// Trigger the endpoint to start the prediction
async function triggerPrediction() {
    try {
        const response = await fetch("predict_sales");

        const data = await response.json();

        if (data.success) {
            console.log("Predictions triggered successfully");
            pollingInterval = setInterval(fetchPredictions, 3000);
        } else {
            if (data.message && data.message.length > 0) {
                console.error("Failed to trigger predictions", data.message);
            }
        }
    } catch (error) {
        console.error("Error triggering prediction:", error);
    }
}

// Handle the form submission (file upload form)
form.addEventListener("submit", async (event) => {
    // Prevent default submission
    event.preventDefault();
    formErrors.style.display = "none";

    try {
        // Submit the form inputs to the endpoint
        const response = await fetch("upload", {
            method: "POST",
            body: new FormData(form),
        });

        const data = await response.json();

        formErrors.innerHTML = "";

        if (data.success) {
            // Parse the JSON response
            console.log("File uploaded successfully", data);

            // Trigger the prediction process
            await triggerPrediction();
        } else {
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
        const response = await fetch("save_to_db", {
            method: "POST",
        });

        // IF unsuccessful when saving to db, throw error
        if (!response.success)
            throw new Error("Failed to save the prediction report.");

        // Else simply log the success message
        console.log((await response.json()).message);
    } catch (error) {
        console.error("Error saving prediction report:", error);
    }
}

// Trigger downloadChart() when the Download Report button is clicked
downloadButton.addEventListener("click", downloadChart);
