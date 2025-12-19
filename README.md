# 🚀 OS Real-Time Monitoring & Reporting Suite

## 1. Project Overview
This project is a containerized, microservice-based monitoring solution developed for the Operating Systems Final Project. It automates the collection of hardware metrics, processes historical data, and generates dual-format reports (HTML/Markdown).

## 2. Technical Architecture
The system is orchestrated using **Docker Compose** across three specialized containers:
1.  **Collector (Bash):** Scrapes hardware metrics and manages the alert system.
2.  **Reporter (Python):** Processes raw logs into statistical averages and reports.
3.  **Visualizer (Nginx/Python):** Serves the interactive dashboard via a web interface.

## 3. Rubric Compliance (Deliverables)
| Requirement | Implementation |
| :--- | :--- |
| **CPU Monitoring** | Usage % and Temperature (C) tracking |
| **GPU Monitoring** | Utilization tracking and Health status |
| **Disk & SMART** | Capacity usage % and SMART Health check |
| **Memory** | RAM consumption tracking |
| **Network** | Traffic statistics (MB) |
| **System Load** | Uptime-based load metrics |
| **Alert System** | Threshold monitoring in `alerts.log` |
| **Reporting** | Automated `.html` and `.md` generation |

## 4. Installation & Setup
### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
* Windows/Linux/Mac terminal with `docker-compose` support.

### Step-by-Step Execution
1.  **Extract** the project files to a local directory.
2.  **Open a Terminal** (CMD, PowerShell, or Bash) in that directory.
3.  **Launch the System**:
    ```bash
    docker-compose up --build
    ```
4.  **Wait** 10-15 seconds for the first data collection cycle to complete.

## 5. Accessing the Reports
* **Live Dashboard:** Navigate to `http://localhost:9000` in your web browser.
* **Performance Summary:** Open `reports/summary_report.md` for the formal record.
* **Log Retrieval:** Raw data is stored in `reports/system_stats.log`.
* **Alert Logs:** Check `reports/alerts.log` for critical events.

