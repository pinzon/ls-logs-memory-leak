# Recursive SNS Lambda Project

## 🚀 Overview

This CDK Python application demonstrates a self-triggering Lambda function with an SNS topic and a configurable parameter. The project is designed to be deployed and tested on LocalStack.
## 🧩 Key Components

- **SNS Topic**: A messaging topic that triggers the Lambda function
- **Lambda Function**: A Python function with complex behavior
- **SSM Parameter**: Controls the number of messages sent

## 🔍 How It Works

The Lambda function performs the following steps when triggered:

1. **Event Reception**
   - Receives message from SNS topic
   - Logs the incoming event details

2. **Pause and Reflection**
   - Waits for 2 seconds
   - Retrieves current SSM Parameter value

3. **Message Generation**
   - If parameter value > 0
     - Sends multiple messages to SNS topic
     - Each message includes:
       - Unique identifier
       - Timestamp

## 📊 Parameter Behavior

- **Default Value**: 0 (no additional messages)
- **Configurable**: Adjust to control message generation
- **Purpose**: Test event propagation and recursive patterns

## 🛠 Deployment Prerequisites

- AWS CDK
- Python 3.9+
- LocalStack (recommended)

### Quick Start

```bash
# Install dependencies
pip install aws-cdk-lib boto3

# Deploy to LocalStack
cdk deploy
```

## 🔬 Use Cases

- Event-driven architecture demonstrations
- Message propagation testing
- Lambda recursion pattern exploration
- LocalStack development

## ⚠️ Caution

Avoid unintended costs or infinite loops in production environments.
