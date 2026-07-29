resource "random_password" "db_password" {
  length  = 16
  special = false
}

resource "aws_secretsmanager_secret" "db_credentials" {
  name        = "${var.project_name}-db-credentials-${var.environment}"
  description = "RDS Postgres connection credentials"
  
  # Allow deletion without waiting for recovery window during testing
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "db_credentials_val" {
  secret_id = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username             = var.db_username
    password             = random_password.db_password.result
    host                 = aws_db_instance.postgres.address
    port                 = 5432
    dbname               = var.db_name
    dbInstanceIdentifier = aws_db_instance.postgres.identifier
  })
}
