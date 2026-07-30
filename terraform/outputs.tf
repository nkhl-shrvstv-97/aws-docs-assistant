output "vpc_id" {
  description = "The ID of the custom VPC"
  value       = aws_vpc.main.id
}

output "rds_endpoint" {
  description = "The database endpoint address"
  value       = aws_db_instance.postgres.endpoint
}

output "s3_bucket_name" {
  description = "The name of the S3 landing bucket"
  value       = aws_s3_bucket.docs_landing.id
}

output "sqs_queue_url" {
  description = "The URL of the SQS queue buffering S3 events"
  value       = aws_sqs_queue.s3_events.id
}

output "db_credentials_secret_arn" {
  description = "The ARN of the database credentials secret"
  value       = aws_secretsmanager_secret.db_credentials.arn
}

output "apprunner_service_url" {
  description = "The URL of the App Runner service"
  value       = aws_apprunner_service.backend.service_url
}

