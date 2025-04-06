// Get the DOM elements
const salesChartCanvas = document.getElementById("optimization_sales_chart");
const form = document.getElementById("optimization-file-upload-form");
const formErrors = document.getElementById(
    "optimization-file-upload-form-errors"
);
const downloadButton = document.getElementById(
    "download-optimization-report-button"
);
const loadingMessage = document.getElementById("optimizing-message");

formErrors.style.display = "none";

// Get chart context
const context = salesChartCanvas.getContext("2d");

// Define color palette
const COLORS = ["#10B981", "#3B82F6"];
const COLOR_PREDICTED_SALES = COLORS[1];
const COLOR_OPTIMIZED_SALES = COLORS[0];

Chart.register(ChartDataLabels);

// Initialize the chart
const salesChart = new Chart(context, {
    type: "bar", // Type of chart
    data: {
        labels: [], // Will be populated with prediction labels
        datasets: [
            {
                label: "Predicted Sales",
                data: [], // Will be populated with predicted sales
                backgroundColor: COLOR_PREDICTED_SALES,
                borderColor: "#202020",
                borderWidth: 1,
            },
            {
                label: "Optimized Sales",
                data: [], // Will be populated with optimized sales
                backgroundColor: COLOR_OPTIMIZED_SALES,
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
                    padding: 15,
                    font: { weight: "bold", size: 13 },
                },
            },
        },
        plugins: {
            legend: {
                display: true,
                labels: {
                    color: "#FFFFFF",
                    boxPadding: 10,
                },
            },
            title: {
                display: true,
                text: "Comparison of Predicted Sales",
                font: { size: 22 },
                color: "#FFFFFF",
            },
            subtitle: {
                display: true,
                text: "Generated on:",
                font: { size: 14 },
                color: "#FFFFFF",
            },
            tooltip: {
                callbacks: {
                    label: function (tooltipItem) {
                        const value = tooltipItem.raw;
                        return `Prediction: ${value.toFixed(2)}`;
                    },
                },
            },
            datalabels: {
                anchor: "start", // Position the label on top of the bar
                align: "bottom",
                color: "#FFFFFF",
                font: { weight: "bold", size: 12 },
                formatter: (value) => value.toFixed(2), // Show two decimal places
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
            salesChart.data.labels = predictionLabels;

            // Set the data values from the fetched predictions
            salesChart.data.datasets[0].data = [
                data.prediction_weekly || 0,
                data.prediction_monthly || 0,
                data.prediction_quarterly || 0,
            ];

            // Update the chart
            salesChart.update();

            // Stop the polling for predictions and reset the polling ID
            clearInterval(pollingInterval);
            pollingInterval = null;

            await triggerOptimization();
        }
    } catch (error) {
        console.error("Error fetching predictions:", error);
    }
}

async function triggerOptimization() {
    try {
        const response = await fetch("optimize_prices");

        const data = await response.json();

        if (data.success) {
            console.log("Optimization process triggered successfully.");
            pollingInterval = setInterval(fetchOptimizations, 3000);
        } else {
            console.error("Failed to trigger optimization", data.message);
        }
    } catch (error) {
        console.error("Error triggering optimization:", error);
    }
}

let reportTimestamp;
let priceList;

async function fetchOptimizations() {
    try {
        const response = await fetch("get_optimizations");
        const data = await response.json();

        // If the response is valid, update the chart
        if (data?.optimized_sales && data?.price_list) {
            const predictionLabels = [
                "Next Week",
                "Next Month",
                "Next Quarter",
            ];

            // Set the labels for each optimized sales value

            salesChart.data.labels = predictionLabels;

            salesChart.data.datasets[1].data = [
                data.optimized_sales[0] || 0,
                data.optimized_sales[1] || 0,
                data.optimized_sales[2] || 0,
            ];

            // Store price_list in priceList
            priceList = data.price_list;

            reportTimestamp = new Date().toLocaleString("en-GB", {
                weekday: "short",
                year: "numeric",
                month: "short",
                day: "2-digit",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
                hour12: true,
            });
            salesChart.options.plugins.subtitle.text = [
                `Generated on: ${reportTimestamp} using OptiPrice ©`,
            ];

            salesChart.update();
            loadingMessage.style.display = "none";
            downloadButton.style.display = "block";

            // Stop the polling for optimization data and reset the polling interval ID
            clearInterval(pollingInterval);
            pollingInterval = null;
        }
    } catch (error) {
        console.error("Error fetching optimizations:", error);
    }
}

// Trigger the endpoint to start the prediction
async function triggerPrediction() {
    downloadButton.style.display = "none";
    loadingMessage.style.display = "block";
    try {
        const response = await fetch("predict_sales");

        const data = await response.json();

        if (data.success) {
            console.log("Optimization's predictions triggered successfully");
            pollingInterval = setInterval(fetchPredictions, 3000);
        } else {
            if (data.message && data.message.length > 0) {
                console.error(
                    "Failed to trigger optimization's predictions",
                    data.message
                );
            }
        }
    } catch (error) {
        console.error("Error triggering optimization's prediction:", error);
    }
}

// Handle the form submission (file upload form)
form.addEventListener("submit", async (event) => {
    // Prevent default submission
    event.preventDefault();
    formErrors.style.display = "none";

    try {
        clearChart();
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
        console.error("Error during optimization file upload:", error);
    }
});

function clearChart() {
    salesChart.data.datasets[0].data = [];
    salesChart.data.datasets[1].data = [];
}

// Function to download the chart
async function downloadChart(event) {
    // Prevent default submission
    event.preventDefault();

    // Convert the chart UI into a string
    const imageUrl = salesChart.toBase64Image();

    // Get the current timestamp
    const timestamp = new Date();
    const timestampString = timestamp.toISOString().replace(/[:.]/g, "-");

    // Create a download link with the image URL and click it
    const downloadLink = document.createElement("a");
    downloadLink.href = imageUrl;
    downloadLink.download = `optimization-report-chart-${timestampString}.png`;
    downloadLink.click();

    try {
        await generateExcelFile(timestamp);
        // Trigger the endpoint to save optimizations in the db as well
        const save_to_db_response = await fetch("save_to_db", {
            method: "GET",
        });

        console.log("Moved on to saving to db");
        const data = save_to_db_response.json();
        // IF unsuccessful when saving to db, throw error
        if (!data.success)
            console.error("Failed to save the optimization report.");

        // Else simply log the success message
        console.log(data.message);
    } catch (error) {
        console.error("Error saving optimization report:", error);
    }
}

async function generateExcelFile(timestamp) {
    const workbook = XLSX.utils.book_new();

    // Headers of Excel columns
    const mainHeaders = [
        "Next Week",
        "",
        "",
        "",
        "Next Month",
        "",
        "",
        "",
        "Next Quarter",
    ];

    // Subheaders
    const subHeaders = [
        "Product ID",
        "Current Price",
        "Optimized Price",
        "",
        "Product ID",
        "Current Price",
        "Optimized Price",
        "",
        "Product ID",
        "Current Price",
        "Optimized Price",
    ];

    const data = [mainHeaders, subHeaders];

    // Extract Product ID
    const productIds = new Set();
    for (const section of Object.values(priceList)) {
        for (const product of section) {
            productIds.add(product.product_id);
        }
    }

    for (const productId of productIds) {
        const row = [];

        // Add data for weekly, monthly, quarterly
        for (const section of ["weekly", "monthly", "quarterly"]) {
            const productData = priceList[section].find(
                (p) => p.product_id === productId
            );
            if (productData) {
                row.push(
                    productData.product_id,
                    productData.current_price,
                    productData.optimized_price,
                    ""
                );
            } else {
                // If there is no data for a particular product, add empty cells
                row.push("", "", "", "");
            }
        }

        // Add the row to 'data'
        data.push(row);
    }

    // Create a worksheet
    const worksheet = XLSX.utils.aoa_to_sheet(data);

    // Add the worksheet to the workbook
    XLSX.utils.book_append_sheet(workbook, worksheet, "Optimized Prices");

    // Add the timestamp and source to a metadata sheet
    const metadataSheetData = [
        [
            "Generated on",
            timestamp
                .toLocaleString("en-GB", {
                    weekday: "short",
                    year: "numeric",
                    month: "short",
                    day: "2-digit",
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit",
                    hour12: true,
                })
                .replace(/[:.]/g, "-"),
        ],
        ["Source", "OptiPrice ©"],
    ];
    const metadataSheet = XLSX.utils.aoa_to_sheet(metadataSheetData);
    XLSX.utils.book_append_sheet(workbook, metadataSheet, "Metadata");

    // Write the workbook into a binary string
    const excelBuffer = XLSX.write(workbook, {
        bookType: "xlsx",
        type: "array",
    });

    // Create a BLOB from the buffer
    const blob = new Blob([excelBuffer], {
        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    });

    // Create a download link for the Excel file and click it
    const excelDownloadLink = document.createElement("a");
    excelDownloadLink.href = URL.createObjectURL(blob);
    excelDownloadLink.download = `optimization-report-prices-${timestamp
        .toISOString()
        .replace(/[:.]/g, "-")}.xlsx`;
    excelDownloadLink.click();
}

// Trigger downloadChart() when the Download Report button is clicked
downloadButton.addEventListener("click", downloadChart);
