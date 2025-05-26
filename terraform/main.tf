provider "aws" {
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  region                      = "us-east-1"
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    s3 = "http://s3.localhost.localstack.cloud:4566"
  }
}

resource "aws_s3_bucket" "s3_start" {
  bucket = "s3-start"
}

resource "aws_s3_bucket" "s3_finish" {
  bucket = "s3-finish"
}

resource "aws_s3_bucket_lifecycle_configuration" "s3_start_lifecycle" {
  bucket = aws_s3_bucket.s3_start.id

  rule {
    id     = "Rule-1"
    status = "Enabled"
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
    expiration {
      days = 100
    }
  }
}
