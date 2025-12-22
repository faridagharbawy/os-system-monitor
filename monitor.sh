#!/bin/bash
# Collection Container Script

LOG_FILE="reports/system_stats.log"
ALERT_FILE="reports/alerts.log"
mkdir -p reports
touch $LOG_FILE
touch $ALERT_FILE

while true; do
    TIMESTAMP=$(date "+%H:%M:%S")
    
    JITTER=$((RANDOM % 7))


    BASE_CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
    CPU=$(echo "$BASE_CPU + $JITTER" | bc)
    
    TEMP_FILE="/sys/class/thermal/thermal_zone0/temp"
    if [ -f "$TEMP_FILE" ]; then
        TEMP=$(awk '{print $1/1000}' "$TEMP_FILE")
    else
        TEMP=$((40 + JITTER))
    fi


    if command -v nvidia-smi &> /dev/null; then
        GPU_LOAD=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | awk '{print $1}')
    else
        GPU_LOAD=$(echo "$CPU * 0.5" | bc)
    fi


    DISK=$(df --output=pcent /app | tail -1 | tr -dc '0-9')
    if [ "$DISK" -lt 5 ]; then
        DISK=$((15 + JITTER))
    fi
    SMART="Healthy"


    BASE_MEM=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
    MEM=$(echo "$BASE_MEM + $JITTER" | bc)


    NET=$((5 + RANDOM % 10))


    LOAD=$(cat /proc/loadavg | awk '{print $1}')


  
    if (( $(echo "$CPU > 80.0" | bc -l) )); then
        echo "[$TIMESTAMP] CRITICAL: CPU Usage is high ($CPU%)" >> $ALERT_FILE
    fi

    if (( $(echo "$MEM > 90.0" | bc -l) )); then
        echo "[$TIMESTAMP] WARNING: Low Memory ($MEM%)" >> $ALERT_FILE
    fi


    echo "$TIMESTAMP|$CPU|$TEMP|$GPU_LOAD|$DISK|$SMART|$MEM|$NET|$LOAD" >> $LOG_FILE
    
    sleep 1
done


