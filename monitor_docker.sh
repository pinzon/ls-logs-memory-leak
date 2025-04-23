#!/bin/bash

# --- INPUT CHECK ---
if [ $# -lt 2 ]; then
  echo "Usage: $0 <sns-topic-arn> <duration-in-minutes>"
  exit 1
fi

# --- CONFIGURATION ---
TOPIC_ARN="$1"
DURATION_MINUTES="$2"
MESSAGE="Hello from Bash!"
REGION="us-east-1"
CONTAINER_NAME="localstack-main"
LOG_FILE="memory_log.csv"

# --- PUSH MESSAGE TO SNS ---
echo "Publishing message to SNS topic: $TOPIC_ARN"

aws --endpoint-url=https://localhost.localstack.cloud:4566 sns publish \
  --region "$REGION" \
  --topic-arn "$TOPIC_ARN" \
  --message "$MESSAGE"

# --- PREPARE LOG FILE ---
if [ ! -f "$LOG_FILE" ]; then
  echo "timestamp,mem_usage,mem_limit" > "$LOG_FILE"
fi

# --- MONITOR LOOP ---
echo "Monitoring memory usage for container: $CONTAINER_NAME"
echo "Will stop after $DURATION_MINUTES minute(s)."
for ((i=0; i<DURATION_MINUTES; i++)); do
  TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
  STATS=$(docker stats --no-stream --format "{{.MemUsage}}" "$CONTAINER_NAME" 2>/dev/null)

  if [[ -z "$STATS" ]]; then
    echo "[$TIMESTAMP] Container $CONTAINER_NAME not running."
  else
    MEM_USED=$(echo "$STATS" | awk -F ' / ' '{print $1}')
    MEM_LIMIT=$(echo "$STATS" | awk -F ' / ' '{print $2}')
    echo "$TIMESTAMP,$MEM_USED,$MEM_LIMIT" >> "$LOG_FILE"
    echo "[$TIMESTAMP] Memory usage: $MEM_USED / $MEM_LIMIT"
  fi

  sleep 60
done

# --- STOP CONTAINER ---
echo "Stopping container: $CONTAINER_NAME"
docker stop "$CONTAINER_NAME"
