# doc_to_voice
An Application that converts the document to voice
# Text-to-Speech using AWS Lambda Function

This AWS Lambda function reads a `.txt` or `.docx` file stored in an S3 bucket and uses Amazon Polly to convert the text into an audio file (MP3 format). The generated audio file is then uploaded back to the same S3 bucket.

## Features

- Reads `.txt` and `.docx` files from an S3 bucket.
- Converts the text content into speech using Amazon Polly.
- Saves the generated MP3 file back to the S3 bucket.

## Prerequisites

1. **AWS Account**: Ensure you have an active AWS account.
2. **AWS Services**:
   - **Amazon S3**: To store the input text files and output audio files.
   - **Amazon Polly**: For text-to-speech conversion.
3. **IAM Role**: The Lambda execution role must have the following permissions:
   - `AmazonS3FullAccess`
   - `AmazonPollyFullAccess`
4. **Dependencies**: The following Python libraries are used:
   - `boto3`: AWS SDK for Python.
   - `python-docx`: For reading `.docx` files.

## Deployment

### 1. Create the Lambda Function
1. Open the [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Create a new Lambda function and select Python 3.x as the runtime.
3. Attach the required IAM role to the Lambda function.

### 2. Upload the Code
1. Copy the Python script from [Lambda Function Code](#lambda-function-code) into the function editor or package it as a `.zip` file for deployment.
2. If packaging as a `.zip`, include the dependencies:
   - Use a tool like `pip` to install dependencies into a directory:
     ```bash
     mkdir package
     pip install boto3 python-docx -t package/
     ```
   - Add your Lambda function code to the package directory, zip everything, and upload it.

### 3. Set Environment Variables (Optional)
You can set environment variables in the Lambda function for configuration flexibility.

### 4. Configure the Trigger
1. Add an S3 trigger to the Lambda function.
2. Specify the bucket where your input files will be uploaded.

## Input Format

### Manual Invocation
When manually invoking the Lambda function, use the following input format:
```json
{
  "bucket_name": "your-s3-bucket-name",
  "object_key": "path-to-your-file.txt"
}
