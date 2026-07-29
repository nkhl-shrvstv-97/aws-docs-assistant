resource "aws_db_subnet_group" "rds" {
  name        = "${var.project_name}-db-subnet-group"
  description = "RDS private database subnet group"
  subnet_ids  = [aws_subnet.private_1.id, aws_subnet.private_2.id]

  tags = {
    Name = "${var.project_name}-db-subnet-group"
  }
}

# Custom DB parameter group
resource "aws_db_parameter_group" "postgres" {
  name        = "${var.project_name}-pg-params"
  family      = "postgres16"
  description = "Custom parameter group for PostgreSQL 16"
}

# Single instance RDS PostgreSQL (db.t4g.micro for cost-efficient test deployments)
resource "aws_db_instance" "postgres" {
  identifier             = "${var.project_name}-postgres-${var.environment}"
  engine                 = "postgres"
  engine_version         = "16.3"
  instance_class         = "db.t4g.micro"
  allocated_storage      = 20
  max_allocated_storage  = 50
  db_name                = var.db_name
  username               = var.db_username
  password               = random_password.db_password.result
  
  db_subnet_group_name   = aws_db_subnet_group.rds.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name   = aws_db_parameter_group.postgres.name

  skip_final_snapshot    = true
  publicly_accessible    = false

  tags = {
    Name = "${var.project_name}-postgres-db"
  }
}
