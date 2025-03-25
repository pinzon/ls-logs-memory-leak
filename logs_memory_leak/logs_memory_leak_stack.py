import aws_cdk as cdk
from aws_cdk import (
    aws_sns as sns,
    aws_lambda as lambda_,
    aws_sns_subscriptions as subscriptions,
    aws_ssm as ssm,
)
from constructs import Construct

class LogsMemoryLeakStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an SNS topic
        topic = sns.Topic(
            self, "RecursiveTopic",
            display_name="Recursive Topic"
        )

        # Create a parameter with default value of 0
        parameter = ssm.StringParameter(
            self, "CountParameter",
            parameter_name="/recursive-lambda/count",
            string_value="2"
        )

        # Create a Lambda function
        recursive_lambda = lambda_.Function(
            self, "RecursiveLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=lambda_.Code.from_inline("""
import json
import boto3
import time
import os

def handler(event, context):
    # Print the event
    print("Received event:", json.dumps(event))
    
    # Wait for 2 seconds
    time.sleep(2)
    
    # Get the parameter value
    ssm_client = boto3.client('ssm')
    response = ssm_client.get_parameter(Name=os.environ['PARAMETER_NAME'])
    count = int(response['Parameter']['Value'])
    
    print(f"Current count value: {count}")
    
    # If count is greater than 0, send messages to the SNS topic
    if count > 0:
        sns_client = boto3.client('sns')
        for i in range(count):
            message = {
                "message": f"Recursive message {i+1} of {count}",
                "timestamp": str(time.time())
            }
            sns_client.publish(
                TopicArn=os.environ['TOPIC_ARN'],
                Message=json.dumps(message)
            )
            print(f"Published message {i+1} of {count} to SNS topic")
    else:
        print("Count is 0, not sending any messages")
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'count': count,
            'message': f"Processed event and sent {count} messages" if count > 0 else "Processed event but didn't send any messages"
        })
    }
"""),
            environment={
                "TOPIC_ARN": topic.topic_arn,
                "PARAMETER_NAME": parameter.parameter_name
            },
            timeout=cdk.Duration.seconds(10)  # Increased timeout for localstack testing
        )
        
        # Subscribe the Lambda to the SNS topic
        topic.add_subscription(subscriptions.LambdaSubscription(recursive_lambda))
        
        # Grant Lambda permissions to read the parameter
        parameter.grant_read(recursive_lambda)
        
        # Grant Lambda permissions to publish to the SNS topic
        topic.grant_publish(recursive_lambda)
        
        # Output the resources for reference
        cdk.CfnOutput(self, "TopicArn", value=topic.topic_arn)
        cdk.CfnOutput(self, "ParameterName", value=parameter.parameter_name)
        cdk.CfnOutput(self, "LambdaName", value=recursive_lambda.function_name)

