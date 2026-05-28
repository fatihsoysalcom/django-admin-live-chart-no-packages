import http.server
import socketserver
import json
import random
import time

PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Live Data Chart</title>
    <!-- Chart.js loaded via CDN, no local install needed -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        #chartContainer { width: 80%; max-width: 800px; margin: auto; }
        h1 { text-align: center; color: #333; }
    </style>
</head>
<body>
    <h1>Simulated Live Data Dashboard</h1>
    <p style="text-align: center; color: #666;">(Data updates every 3 seconds)</p>
    <div id="chartContainer">
        <canvas id="myChart"></canvas>
    </div>

    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        let myChart;

        // Function to fetch data and update chart
        async function fetchDataAndUpdateChart() {
            try {
                // This simulates fetching data from a Django Admin custom view or API endpoint
                // In a real Django app, this would be a URL defined in urls.py
                // and handled by a Django view returning JsonResponse.
                const response = await fetch('/data');
                const data = await response.json();

                const labels = data.map(item => item.label);
                const values = data.map(item => item.value);

                if (myChart) {
                    myChart.data.labels = labels;
                    myChart.data.datasets[0].data = values;
                    myChart.update();
                } else {
                    myChart = new Chart(ctx, {
                        type: 'bar', // Can be 'line', 'pie', etc.
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Dynamic Data Points',
                                data: values,
                                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                                borderColor: 'rgba(75, 192, 192, 1)',
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    title: {
                                        display: true,
                                        text: 'Value'
                                    }
                                },
                                x: {
                                    title: {
                                        display: true,
                                        text: 'Category'
                                    }
                                }
                            },
                            plugins: {
                                title: {
                                    display: true,
                                    text: 'Live Data Visualization'
                                }
                            }
                        }
                    });
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }

        // Initial fetch and update when the page loads
        fetchDataAndUpdateChart();

        // Update chart every 3 seconds (simulating live updates from the backend)
        setInterval(fetchDataAndUpdateChart, 3000);
    </script>
</body>
</html>
            """
            self.wfile.write(html_content.encode('utf-8'))
        elif self.path == '/data':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            # Simulate dynamic data generation for the chart
            # In a real Django app, this would query your database
            # and return serialized data (e.g., using Django Rest Framework or simple JsonResponse).
            data = []
            for i in range(5):
                data.append({
                    "label": f"Item {i+1}",
                    "value": random.randint(10, 100)
                })
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

# Start the server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    print("This example simulates adding live charts to Django Admin without extra Python packages.")
    print("It uses a simple Python server to mimic Django's backend and client-side JavaScript for charting.")
    httpd.serve_forever()
