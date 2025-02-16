terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "logs" {
  bucket = var.bucket_name
}

resource "aws_iam_user" "dev" {
  name = "ml-inference-api-dev"
}

resource "aws_iam_user_policy" "dev_policy" {
  name = "ml-inference-api-dev-policy"
  user = aws_iam_user.dev.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["bedrock:InvokeModel"]
        Resource = ["arn:aws:bedrock:*:*:model/*"]
      },
      {
        Effect = "Allow"
        Action = ["s3:PutObject", "s3:GetObject"]
        Resource = ["${aws_s3_bucket.logs.arn}/*"]
      }
    ]
  })
}

resource "aws_iam_access_key" "dev" {
  user = aws_iam_user.dev.name
}