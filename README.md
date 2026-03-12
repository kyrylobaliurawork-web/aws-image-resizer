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


### Estimated monthly cost


---

# 📦 Amazon S3

First, create an **S3 bucket** that will store the images.


After creating the bucket, upload an image that will later be resized by the Lambda function.


---

# ⚙️ AWS Lambda

Next, create an **AWS Lambda function**.

### Lambda configuration

| Parameter | Value |
|----------|------|
| Runtime | Python 3.11 |
| Architecture | x86_64 |
| Timeout | 3 seconds |

![Create Lambda Function](images/image6.png)

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

Make sure the runtime and architecture match the Lambda function.

Attach the layer to the Lambda function.

---

# 🧠 Deploy Lambda Code

Insert your Lambda function code into the Lambda editor.

Then deploy the function and run a test.

If the test runs successfully, the Lambda function is configured correctly.

---

# 🌐 API Gateway

Now create an HTTP API in API Gateway.

We use HTTP API because:

it is cheaper

it has lower latency

it provides all required functionality

Enable Dualstack to support IPv4 and IPv6.

Then integrate the API with the Lambda function.

---

# 🔗 API Endpoint

---

#🔌 Lambda Trigger

After deployment, API Gateway will appear as a Lambda trigger.

The generated URL becomes the main endpoint of the service.

Optionally, you can configure a custom domain using Amazon Route 53.

---

🪵 Debugging with CloudWatch

If errors occur, check CloudWatch Logs.
Common error:
```
AccessDenied: s3:GetObject
```
This means the Lambda function does not have permission to access the S3 bucket.
---

# 🔐 Fix IAM Permissions

Go to IAM Roles and add the following policy to the Lambda role:

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

---

# 🚀 Possible Improvements

1.For production environments, consider the following improvements:

2.Configure a custom domain with Route 53

3.Add Amazon SQS for request queueing

4.Optimize image processing performance

5.Cache resized images closer to users with CloudFront

These improvements will make the system more scalable and production-ready.

