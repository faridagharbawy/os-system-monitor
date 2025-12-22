FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    bash procps python3 bc smartmontools \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN chmod +x monitor.sh
