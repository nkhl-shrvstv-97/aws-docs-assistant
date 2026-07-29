variable "aws_region" {
  description = "The AWS region to deploy resources into"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name prefix for resources"
  type        = string
  default     = "nikhil-aws-docs-assistant"
}

variable "environment" {
  description = "Environment identifier (e.g. dev, prod)"
  type        = string
  default     = "dev"
}

variable "db_name" {
  description = "The name of the database to create"
  type        = string
  default     = "aws_docs"
}

variable "db_username" {
  description = "The master username for the database"
  type        = string
  default     = "postgres"
}
