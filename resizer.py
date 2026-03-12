import boto3
from PIL import Image
import io
import base64
import json

# Create an S3 client
s3 = boto3.client("s3")

# Name of the S3 bucket
BUCKET = "images-resizer-bucket-own"

def lambda_handler(event, context):

    # Detect where parameters come from
    if "queryStringParameters" in event and event["queryStringParameters"]:
        params = event["queryStringParameters"]
    else:
        params = event

    # Validate parameters
    if "image" not in params or "width" not in params:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Missing parameters. Required: image, width"
            })
        }

    key = params["image"]
    width = int(params["width"])

    # Get image from S3
    obj = s3.get_object(Bucket=BUCKET, Key=key)
    image_bytes = obj["Body"].read()

    # Open image
    image = Image.open(io.BytesIO(image_bytes))

    # Keep aspect ratio
    ratio = width / image.width
    height = int(image.height * ratio)

    # Resize image
    resized = image.resize((width, height))

    # Save to memory
    buffer = io.BytesIO()
    resized.save(buffer, "JPEG")

    # Return image
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "image/jpeg"
        },
        "body": base64.b64encode(buffer.getvalue()).decode("utf-8"),
        "isBase64Encoded": True
    }