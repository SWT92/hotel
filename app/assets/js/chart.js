document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('myChart').getContext('2d');

    $(document).ready(function() {
        $.ajax({
            url: "/getChart",
            type: "GET",
            contentType: 'application/json;charset=UTF-8',
            error: function(e) {
                console.log("Error : ", e);
            },
            success: function(responses) {
                // Extract and sort labels (months) in chronological order
                var labels = Object.keys(responses.deluxe);
                labels = labels.sort(function(a, b) {
                    var dateA = new Date(a);
                    var dateB = new Date(b);
                    return dateA - dateB;
                });

                // Sort data accordingly
                var deluxeData = labels.map(function(label) {
                    return responses.deluxe[label];
                });

                var standardData = labels.map(function(label) {
                    return responses.standard[label];
                });

                // Determine the maximum value for the y-axis
                var maxYValue = Math.max(...deluxeData, ...standardData);
                // Set a step size based on the maximum value
                var stepSize = Math.ceil(maxYValue / 5); // You can adjust the number of intervals (5 in this case)

                // Create a chart context
                var myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Deluxe Room',
                                data: deluxeData,
                                borderColor: 'rgba(75, 192, 192, 1)',
                                borderWidth: 3,
                                fill: false
                            },
                            {
                                label: 'Standard Room',
                                data: standardData,
                                borderColor: 'rgba(255, 99, 132, 1)',
                                borderWidth: 3,
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            x: {
                                type: 'category', // Use a category scale for labels
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Date'
                                }
                            },
                            y: {
                                beginAtZero: true, // Start the y-axis at 0
                                max: maxYValue,
                                stepSize: stepSize, // Set the step size
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Value'
                                }
                            }
                        }
                    }
                });
            }
        });
    });
});
