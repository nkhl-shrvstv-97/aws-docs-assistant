# Terraform & Cloud Infrastructure Architecture

This document describes the AWS resources, network topology, security mechanisms, and credentials management provisioned by our Terraform infrastructure configurations.

---

## 1. Network Topology (VPC Design)

To ensure secure data isolation, the application is deployed within a Virtual Private Cloud (VPC) with isolated private subnets.

```text
       [Internet Gateway]
               │
               ▼
       [Public Subnets]
       - Application Load Balancer (ALB)
       - App Runner VPC Connector ingress/egress
               │ (Secure VPC Traffic)
               ▼
       [Private Subnets]
       - Ingestion Worker Lambda (VPC bound)
       - RDS PostgreSQL DB Instance (No public IP)
```

* **VPC:** Custom IPv4 CIDR block (e.g. `10.0.0.0/16`).
* **Subnets:**
  * **Public Subnets:** Multi-AZ public subnets for public ingress endpoints (App Runner endpoints, load balancer routing).
  * **Private Subnets:** Multi-AZ private subnets hosting the RDS database. Traffic is strictly controlled through VPC routing and security groups.
* **VPC Connector:** Allows serverless runtimes (App Runner, Lambda) to connect securely to RDS private IPs.

---

## 2. Infrastructure Resources

The infrastructure is broken down into modular components within the `terraform/` directory:

### A. Network & VPC Configs (`vpc.tf`)
* Creates VPC, internet gateways, subnets, route tables, and NAT gateways (if egress is required for search endpoints).
* Provisions **VPC Security Groups**:
  * **Database Security Group:** Permits ingress TCP port `5432` only from source security groups associated with AWS App Runner VPC Connectors and the Ingestion Lambda.
  * **App Runner Security Group:** Governs outbound network access.

### B. Database Cluster (`rds.tf`)
* Provisions a single **Amazon RDS PostgreSQL Instance** (using db.t4g.micro or db.t4g.small to control costs).
* Configures database parameter groups to enable the `pgvector` extension.
* Sets up automated snapshot windows and storage scaling features.

### C. Container Compute & Hosting (`ecs.tf` or `apprunner.tf`)
* Provisions **AWS App Runner** services (highly structured and scalable serverless runtime) to compile, build, and run the containerized FastAPI backend.
* Creates the required VPC Connector to attach the container to the VPC.

### D. Security & IAM Configuration (`iam.tf` & `secrets.tf`)
* **AWS Secrets Manager:** Automatically generates a secure password for the database master user, uploads it, and makes it available to App Runner containers via environmental secret mapping.
* **IAM Policies & Roles:**
  * **ECS/App Runner Instance Role:** Attaches policies allowing write permissions to CloudWatch, reading secrets from Secrets Manager, and invoking Amazon Bedrock models (`bedrock:InvokeModel`).
  * **Lambda Ingestion Role:** Allows read access to the S3 bucket, Bedrock invocation, and RDS connectivity.

---

## 3. Terraform Infrastructure Implementation Checklist

Use this checklist to write and verify all required Terraform resources for deploying the complete AWS environment:

### Phase 1: Provider & VPC Networking (`vpc.tf`)
- [ ] Configure `provider.tf` targeting AWS with a defined deployment region.
- [ ] Create `aws_vpc` resource with DNS hostnames and support enabled.
- [ ] Create 2 Public Subnets (across different Availability Zones) for ingress and ALB connectivity.
- [ ] Create 2 Private Subnets (across different Availability Zones) to isolate RDS.
- [ ] Provision `aws_internet_gateway` and route tables routing public subnet egress to it.
- [ ] Provision `aws_eip` and `aws_nat_gateway` in the public subnet to allow private compute elements egress (needed for Lambda and App Runner to fetch Bedrock and Live Search APIs).
- [ ] Create route tables for private subnets routing traffic to the NAT gateway.
- [ ] Create `aws_security_group` for App Runner, allowing egress.
- [ ] Create `aws_security_group` for the Lambda Ingest function, allowing egress.
- [ ] Create `aws_security_group` for the RDS PostgreSQL DB, with an inbound rule allowing TCP Port `5432` only from the App Runner and Lambda Security Group IDs.

### Phase 2: Database Layer (`rds.tf`)
- [ ] Create `aws_db_subnet_group` containing the private subnet IDs.
- [ ] Create custom `aws_db_parameter_group` for PostgreSQL (e.g. version 15 or 16) to ensure the parameter maps are correct.
- [ ] Provision the `aws_db_instance` (PostgreSQL) resource:
  - [ ] Set size (`db.t4g.micro` or `db.t4g.small` for low test costs).
  - [ ] Bind it to the DB subnet group.
  - [ ] Bind it to the Database Security Group.
  - [ ] Set `skip_final_snapshot = true` (for test accounts).
  - [ ] Reference database credentials from Secrets Manager dynamic metadata.

### Phase 3: Security, IAM, & Secrets (`iam.tf` & `secrets.tf`)
- [ ] Create `aws_secretsmanager_secret` for RDS database credentials.
- [ ] Create `aws_secretsmanager_secret_version` to store random database usernames and passwords as JSON string blocks.
- [ ] Create IAM Role for App Runner Instance execution:
  - [ ] Policy allowing `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream`.
  - [ ] Policy allowing Secrets Manager read access for the database credentials secret ARN.
  - [ ] Policy allowing CloudWatch logging access.
- [ ] Create IAM Role for the Lambda Ingestion function:
  - [ ] Policy allowing Bedrock invoke model.
  - [ ] Policy allowing S3 read/download from the landing bucket.
  - [ ] Policy allowing Secrets Manager read access.
  - [ ] Policy allowing VPC connectivity (AWS managed `AWSLambdaVPCAccessExecutionRole`).

### Phase 4: Ingestion Storage & Event Buffer (`s3_sqs.tf`)
- [ ] Provision the S3 Document Landing Bucket (`aws_s3_bucket`) for raw `.md` uploads.
- [ ] Create `aws_sqs_queue` (standard or FIFO) to buffer S3 file upload events.
- [ ] Set the SQS Queue Policy to allow S3 service bucket events publishing.
- [ ] Create the `aws_s3_bucket_notification` resource directing S3 Object Created events to the SQS queue ARN.

### Phase 5: Lambda Ingestion Worker (`lambda.tf`)
- [ ] Create the `aws_lambda_function` resource containing the Python worker code:
  - [ ] Bind it to the private VPC subnet IDs.
  - [ ] Bind it to the Lambda Security Group.
  - [ ] Configure environment variables: `DB_SECRET_ARN`, `DB_HOST`, `DB_NAME`, `DB_PORT`, and `DB_USER`.
  - [ ] Configure memory (minimum 512MB) and timeout (e.g. 60 seconds).
- [ ] Create the `aws_lambda_event_source_mapping` linking SQS queue messages to the Lambda function.
  - [ ] Configure batch size (e.g., 5).
  - [ ] Cap execution scaling configurations.

### Phase 6: App Runner Web App (`apprunner.tf`)
- [ ] Create the `aws_apprunner_vpc_connector` resource linking the service to the private subnet IDs and App Runner Security Group.
- [ ] Create `aws_apprunner_service` resource:
  - [ ] Map the service to pull from your Docker image repository (AWS ECR URL).
  - [ ] Map instance permissions to the App Runner IAM Instance Role ARN.
  - [ ] Map database credentials dynamically from the Secrets Manager secret ARN.
  - [ ] Configure scaling settings (e.g. min size 1 container).
- [ ] Define Outputs (`outputs.tf`):
  - [ ] Export the public URL generated by App Runner.
  - [ ] Export the S3 bucket name.
  - [ ] Export the RDS database endpoint.
