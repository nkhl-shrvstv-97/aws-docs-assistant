data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = "${path.module}/lambda_function.zip"

  source {
    content  = file("${path.module}/../backend/ingestion/lambda_function.py")
    filename = "backend/ingestion/lambda_function.py"
  }
  source {
    content  = file("${path.module}/../backend/ingestion/parser.py")
    filename = "backend/ingestion/parser.py"
  }
  source {
    content  = ""
    filename = "backend/__init__.py"
  }
  source {
    content  = ""
    filename = "backend/ingestion/__init__.py"
  }
}

resource "aws_lambda_function" "ingest_worker" {
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  function_name    = "${var.project_name}-ingest-worker-${var.environment}"
  role             = aws_iam_role.lambda_ingest.arn
  handler          = "backend.ingestion.lambda_function.lambda_handler"
  runtime          = "python3.12"
  timeout          = 60
  memory_size      = 512

  vpc_config {
    subnet_ids         = [aws_subnet.private_1.id, aws_subnet.private_2.id]
    security_group_ids = [aws_security_group.lambda_ingest.id]
  }

  environment {
    variables = {
      DB_SECRET_ARN    = aws_secretsmanager_secret.db_credentials.arn
      AWS_REGION_NAME  = var.aws_region
      PYTHONPATH       = "/var/task"
    }
  }

  tags = {
    Environment = var.environment
  }
}

# Bind SQS queue events to Lambda trigger
resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = aws_sqs_queue.s3_events.arn
  function_name    = aws_lambda_function.ingest_worker.arn
  batch_size       = 5
}
