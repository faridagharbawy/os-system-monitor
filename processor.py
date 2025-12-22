"""
Final Multi-Graph Historical Processor.
Generates 6 distinct auto-scaling charts + SMART status table + Full MD Report.
"""
import os
import time


def generate_dashboard():
    """
    Reads the system log file and generates a responsive HTML
    dashboard and a comprehensive Markdown summary report.
    """
    log_path = "reports/system_stats.log"
    if not os.path.exists(log_path):
        return

    try:
        with open(log_path, "r", encoding="utf-8") as file:
            lines = file.readlines()[-20:]
    except (IOError, OSError):
        return

    if not lines:
        return

    times, cpu_p, temp_p, gpu_p = [], [], [], []
    disk_p, mem_p, net_p, load_p = [], [], [], []
    smart_status = "Unknown"

    for line in lines:
        parts = line.strip().split("|")
        if len(parts) >= 9:
            times.append(parts[0])
            cpu_p.append(parts[1])
            temp_p.append(parts[2])
            gpu_p.append(parts[3])
            disk_p.append(parts[4])
            smart_status = parts[5]
            mem_p.append(parts[6])
            net_p.append(parts[7].replace("MB", ""))
            load_p.append(parts[8])

    html_head = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OS Project Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <meta http-equiv="refresh" content="1">
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #121212;
                   color: white; padding: 20px; }
            .container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
            .card { background: #1e1e1e; padding: 15px; border-radius: 10px; 
                    border: 1px solid #333; }
            .status-box { margin-top: 20px; padding: 20px; background: #004d40;
                          border-radius: 10px; text-align: center; font-size: 20px; }
            h1 { text-align: center; color: #00d4ff; margin-bottom: 30px; }
            h3 { margin-top: 0; color: #ccc; font-size: 16px; }
        </style>
    </head>
    """

    html_body = f"""
    <body>
        <h1>System Monitoring Dashboard</h1>
        <div class="container">
            <div class="card"><h3>1. CPU (%)</h3><canvas id="cpu"></canvas></div>
            <div class="card"><h3>2. Temp (C)</h3><canvas id="temp"></canvas></div>
            <div class="card"><h3>3. GPU (%)</h3><canvas id="gpu"></canvas></div>
            <div class="card"><h3>4. Disk (%)</h3><canvas id="disk"></canvas></div>
            <div class="card"><h3>5. Memory (%)</h3><canvas id="mem"></canvas></div>
            <div class="card"><h3>6. Network (MB)</h3><canvas id="net"></canvas></div>
        </div>
        <div class="status-box">
             Disk Health (SMART): <strong>{smart_status}</strong> |
            System Load: <strong>{load_p[-1] if load_p else "N/A"}</strong>
        </div>
        <script>
            const makeChart = (id, label, data, color) => {{
                new Chart(document.getElementById(id), {{
                    type: 'line',
                    data: {{
                        labels: {times},
                        datasets: [{{
                            label: label, data: data, borderColor: color,
                            backgroundColor: color + '33', fill: true, tension: 0.4
                        }}]
                    }},
                    options: {{
                        animation: false, responsive: true,
                        scales: {{
                            y: {{ beginAtZero: false, ticks: {{ color: '#aaa' }} }},
                            x: {{ ticks: {{ color: '#aaa' }} }}
                        }},
                        plugins: {{ legend: {{ labels: {{ color: 'white' }} }} }}
                    }}
                }});
            }};
            makeChart('cpu', 'CPU Usage', {cpu_p}, '#00d4ff');
            makeChart('temp', 'Temperature', {temp_p}, '#ffae00');
            makeChart('gpu', 'GPU Load', {gpu_p}, '#00ff44');
            makeChart('disk', 'Disk Space', {disk_p}, '#ffffff');
            makeChart('mem', 'RAM Usage', {mem_p}, '#9d00ff');
            makeChart('net', 'Network MB', {net_p}, '#ff4d4d');
        </script>
    </body>
    </html>
    """

    with open("reports/index.html", "w", encoding="utf-8") as file:
        file.write(html_head + html_body)


    try:
        def get_avg(data_list):
            nums = [float(x) for x in data_list if x.strip()]
            return sum(nums) / len(nums) if nums else 0

        md_report = f"""# 📝 System Performance Summary Report
Generated on: {time.ctime()}

## 📊 Requirements Health Check
1. **CPU Usage:** Avg {get_avg(cpu_p):.2f}% (Last: {cpu_p[-1]}%)
2. **CPU Temperature:** {temp_p[-1]}°C
3. **GPU Utilization:** {gpu_p[-1]}%
4. **Disk Usage:** {disk_p[-1]}% (SMART Status: {smart_status})
5. **Memory Consumption:** Avg {get_avg(mem_p):.2f}% (Last: {mem_p[-1]}%)
6. **Network Statistics:** {net_p[-1]} MB/s
7. **System Load Metrics:** {load_p[-1]}

## 📂 Report Storage & Retrieval
- **HTML Report Path:** `reports/index.html`
- **Markdown Report Path:** `reports/summary_report.md`
"""
        with open("reports/summary_report.md", "w", encoding="utf-8") as file:
            file.write(md_report)

    except (ValueError, ZeroDivisionError, IOError):
        with open("reports/error.log", "a", encoding="utf-8") as f:
            f.write(f"Logging error at {time.ctime()}\\n")


if __name__ == "__main__":
    while True:
        generate_dashboard()
        time.sleep(1)
