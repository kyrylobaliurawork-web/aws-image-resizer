# 🚀 AWS Image Resizer

A **serverless image resizing service** built using **AWS Lambda, Amazon S3, and API Gateway**.

This project demonstrates how to build a simple **serverless architecture** that dynamically resizes images stored in an S3 bucket.

---

# 📌 Project Overview

The main goal of this project is to demonstrate:

- Serverless architecture with AWS
- Image processing with Python
- API-driven image resizing
- Low-cost infrastructure using serverless services

The main focus of this guide is **architecture and deployment**, not deep code implementation.

---

# 🏗 Architecture

![Architecture Diagram](images/1-project-diagram.png)

### Workflow

1. A **client sends a request** to API Gateway
2. API Gateway **triggers AWS Lambda**
3. Lambda retrieves an image from **Amazon S3**
4. The image is resized using **Pillow (Python library)**
5. The processed image is returned to the client

All execution logs are stored in **Amazon CloudWatch**.

---

# 💰 Cost Estimation (AWS Pricing Calculator)

Serverless services only charge **when they are used**, which makes this architecture very cost-efficient.

### Example configuration

![Project estimate configuration](images/2-cost-estimate-params.png)

### Estimated monthly cost

![Project estimate outcome](images/3-cost-estimate-result.png)

---

# 📦 Amazon S3

First, create an **S3 bucket** that will store the images.

![S3 configuration](images/4-S3-cofiguration.png)

After creating the bucket, upload an image that will later be resized by the Lambda function.

![S3 upload](images/5-S3-upload.png)

![S3 uploaded photo](images/6-S3-photo.png)

---

# ⚙️ AWS Lambda

Next, create an **AWS Lambda function**.

### Lambda configuration

| Parameter | Value |
|----------|------|
| Runtime | Python 3.11 |
| Architecture | x86_64 |
| Timeout | 3 seconds |

![Create Lambda Function](images/7-lambda-basic-info.png)

Make sure you remember the **runtime and architecture**, because the **Lambda Layer must match these settings**.

---

# 📚 Creating a Lambda Layer (Pillow)

AWS Lambda **does not include the Pillow library by default**, so we must create a **custom Lambda Layer**.

Docker is used to build the package in a compatible environment.

---

## Step 1 — Start Docker Container
```bash
docker run -it --name pillow-build python:3.11 bash
```

## Step 2 — Create Layer Directory
```bash
mkdir -p lambda-layer/python
cd lambda-layer
```

## Step 3 — Install Pillow
```bash
pip install pillow -t python/ \
--platform manylinux2014_x86_64 \
--python-version 3.11 \
--only-binary=:all:
```

## Step 4 — Verify Installation
```bash
ls python/
```
You should see folders similar to:
```bash
PIL/
pillow.libs/
pillow-*.dist-info/
```

## Step 5 — Create ZIP Archive
```bash
zip -r9 /pillow-layer.zip python/
```
Exit the container:
```bash
exit
```

## 📥 Copy the Layer to Your Computer
```bash
docker cp pillow-build:/pillow-layer.zip C:/Users/your-username/Downloads/
```
Alternative command:
```bash
docker cp pillow-build:/pillow-layer.zip %USERPROFILE%/Downloads/
```

## Cleanup (Optional)
```bash
docker stop pillow-build
docker rm pillow-build
```
Verify that the file exists:
```bash
dir %USERPROFILE%/Downloads/pillow-layer.zip
```

---

# 📦 Upload the Layer to Lambda

Create a Lambda Layer in AWS and upload the ZIP archive.
![Layer-start](images/8-layer-start.png)
![Layer-edit](images/9-layer-edit.png)
![Layer-add](images/10-add-layer.png)
![Layer-create](images/11-create-new-layer.png)

Make sure the runtime and architecture match the Lambda function.

![Layer-configuration](images/12-layer-configuration.png)

Our layer:

![Our layer](images/13-our-layer.png)

Attach the layer to the Lambda function.

![Attach the layer](images/14-add-and-apply-new-layer.png)

As outcome we can see that we have plus one layer:

![Plus one layer](images/15-result-layer.png)

---

# 🧠 Deploy Lambda Code

Insert your Lambda function code into the Lambda editor.

Then deploy the function and run a test.

![Deploy our code](images/16-deploy-code.png)
![Test our code](images/17-test-code.png)


If the test runs successfully, the Lambda function is configured correctly.

![Test outcome](images/18-test-result.png)

---

# 🌐 API Gateway

Now create an HTTP API in API Gateway.

We use HTTP API because:

it is cheaper

it has lower latency

it provides all required functionality

![Build API Gateway](images/19-build-apigateway.png)

Enable Dualstack to support IPv4 and IPv6.

![Configure API Gateway](images/20-configurate-apigateway.png)


Then integrate the API with the Lambda function.

![Inegrate with lambda](images/21-integrate-lambda.png)

And here leave the default settings

![Default settings](images/22-get-apigateway.png)

---

# 🔗 API Endpoint

![Api Endpoint](images/23-default-apigateway.png)

---

#🔌 Lambda Trigger

After deployment, API Gateway will appear as a Lambda trigger.

![API Gateway - Lambda Function trigger](images/24-lambda-connected-with-apigateway.png)

The generated URL becomes the main endpoint of the service.

![API Gateway link](images/25-our-link.png)

Optionally, you can configure a custom domain using Amazon Route 53.

---

# 🛑Small error

To fix this error you just need to read the error message, it tells to us about "missing parameters"
We need to add parametrs into this URL: https://z35ltl60id.execute-api.us-east- amazonaws.com/resize 
Example: https://z35ltl60id.execute-api.us-east- amazonaws.com/resize?image=photo.jpeg&width=300

![First error](images/26-first-error.png)

---

#🪵 Debugging with CloudWatch
New one error:
![Second error](images/27-second-error.png)

If errors occur, check CloudWatch Logs.

![CloutWatch logs](images/28-cloud-watch-logs.png)
![The error](images/28_1-cloud-watch-logs.png)

Common error:
```
AccessDenied: s3:GetObject
```
This means the Lambda function does not have permission to access the S3 bucket.
---

# 🔐 Fix IAM Permissions

Go to IAM Roles and add the following policy to the Lambda role:

![IAM roles](images/29-IAM-roles.png)

![Lambda function role](images/30-IAM-lambda-role.png)

And add a new permission to the Lambda role:
```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::images-resizer-bucket-own/*"
}
```

This allows Lambda to access objects only within the specified bucket, preserving the least privilege principle.

---

# ⏱ Handling Large Images

Large images may exceed the Lambda timeout limit.

If this happens, increase the Lambda timeout in the function settings.
![Lambda function role](images/33-high-quality-photo.png)

![Lambda 3sec](images/34-lambda-3sec-error.png)

![Lambda 10sec](images/35-lambda-10sec-fixed.png)

---

# ☺️ Results
Width = 300
![Lambda 10sec](images/31-project-result-300.png)

And width = 1000
![Lambda 10sec](images/32-project-result-1000.png)


# 🚀 Possible Improvements

1.For production environments, consider the following improvements:

2.Configure a custom domain with Route 53

3.Add Amazon SQS for request queueing

4.Optimize image processing performance

5.Cache resized images closer to users with CloudFront

These improvements will make the system more scalable and production-ready.

