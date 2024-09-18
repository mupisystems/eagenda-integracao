# Slack

In this example, we receive new appointment notifications via webhook and send an alert to a Slack channel, leveraging AWS API Gateway and AWS Lambda to execute serverless code seamlessly. This setup ensures scalability and low-latency processing, making it ideal for real-time notifications in cloud environments.

## Configuration
Environment variable: SLACK_TOKEN - Authentication token for Slack.

## How to Use
The code is pre-configured to run as an AWS Lambda function. To get started, deploy the code within your AWS environment. Ensure that you configure the AWS endpoint in your eAgenda webhook settings to point to the AWS API Gateway endpoint. This setup will enable your Lambda function to receive and process webhook notifications from eAgenda efficiently.