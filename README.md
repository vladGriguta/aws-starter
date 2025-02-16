# ML Inference API
FastAPI-based service for LLM inference using AWS Bedrock (Llama models).

## Prerequisites
- AWS Account
- Terraform
- Docker
- Python 3.12

## Setup
1. Deploy AWS resources:
```bash
cd terraform
terraform init
terraform apply
```

2. Set AWS credentials in your environment:
```bash
export AWS_ACCESS_KEY_ID=<your_access_key>
export AWS_SECRET_ACCESS_KEY=<your_secret_key>
export AWS_DEFAULT_REGION=<your_region>
```

3. Build and run container:
```bash
docker build -t ml-inference-api .
docker run -p 8000:8000 -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e ml-inference-api
```

## API Usage
POST `/predict`
```json
{
    "text": "Your prompt here"
}
```

## Infrastructure
- AWS Bedrock for LLM inference
- S3 for request logging
- IAM for access management