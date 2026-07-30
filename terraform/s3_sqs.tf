# Random identifier for unique bucket name
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# S3 Bucket for raw Markdown documents landing
resource "aws_s3_bucket" "docs_landing" {
  bucket        = "${var.project_name}-landing-${random_id.bucket_suffix.hex}"
  force_destroy = true
}

# SQS Queue to buffer document upload events
resource "aws_sqs_queue" "s3_events" {
  name                      = "${var.project_name}-s3-events-queue"
  receive_wait_time_seconds = 10
  
  # Configure redrive policy if needed, let's keep it simple
  visibility_timeout_seconds = 90
}

# Allow S3 to publish events to SQS queue
resource "aws_sqs_queue_policy" "allow_s3" {
  queue_url = aws_sqs_queue.s3_events.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          Service = "s3.amazonaws.com"
        }
        Action    = "sqs:SendMessage"
        Resource  = aws_sqs_queue.s3_events.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_s3_bucket.docs_landing.arn
          }
        }
      }
    ]
  })
}

# S3 Event Notification to SQS Queue
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.docs_landing.id

  queue {
    queue_arn     = aws_sqs_queue.s3_events.arn
    events        = ["s3:ObjectCreated:*"]
    filter_suffix = ".md"
  }

  depends_on = [aws_sqs_queue_policy.allow_s3]
}
