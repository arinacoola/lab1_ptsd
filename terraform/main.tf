provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  region                      = "us-east-1"
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    s3     = "http://localhost:4566"
    lambda = "http://localhost:4566"
    iam    = "http://localhost:4566"
    sqs    = "http://localhost:4566"
  }
}

resource "aws_s3_bucket" "s3_start" {
  bucket = "s3-start"
}

resource "aws_s3_bucket" "s3_finish" {
  bucket = "s3-finish"
}

resource "aws_sqs_queue" "lambda_queue" {
  name = "lambda-queue"
}

resource "aws_s3_bucket_lifecycle_configuration" "s3_start_lifecycle" {
  bucket = aws_s3_bucket.s3_start.id

  rule {
    id     = "Rule-1"
    status = "Enabled"
    filter {
        prefix = ""
    }
    expiration {
      days = 90
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "s3_finish_lifecycle" {
  bucket = aws_s3_bucket.s3_finish.id

  rule {
    id     = "Rule-2"
    status = "Enabled"
    filter {
        prefix = ""
    }
    expiration {
      days = 100
    }
  }
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda/lambda_function.py"
  output_path = "${path.module}/lambda/lambda_function.zip"
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_s3_policy" {
  name = "lambda_s3_policy"
  role = aws_iam_role.lambda_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource = [
          aws_s3_bucket.s3_start.arn,
          "${aws_s3_bucket.s3_start.arn}/*",
          aws_s3_bucket.s3_finish.arn,
          "${aws_s3_bucket.s3_finish.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_sqs_policy" {
  name = "lambda_sqs_policy"
  role = aws_iam_role.lambda_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = ["sqs:SendMessage"],
        Resource = aws_sqs_queue.lambda_queue.arn
      }
    ]
  })
}

resource "aws_lambda_function" "lambda_copy_s3" {
  function_name    = "lambda_copy_s3"
  runtime          = "python3.11"
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "lambda_function.lambda_handler"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      S3_START  = aws_s3_bucket.s3_start.id
      S3_FINISH = aws_s3_bucket.s3_finish.id
      SQS_QUEUE_URL = aws_sqs_queue.lambda_queue.url
    }
  }
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_copy_s3.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.s3_start.arn
}

resource "aws_s3_bucket_notification" "trigger_lambda" {
  bucket = aws_s3_bucket.s3_start.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.lambda_copy_s3.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3]
} 
