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

