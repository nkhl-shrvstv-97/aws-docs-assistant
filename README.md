# AWS Documentation RAG & Agent Assistant

An agentic search and retrieval assistant that utilizes **LangGraph**, **pgvector (RDS PostgreSQL)**, and **Amazon Bedrock (Claude 3.5 Sonnet / Haiku, Titan)** to answer complex queries regarding AWS services, citing documentation with accuracy. It features a local CLI client, an embedded web interface, an automated document ingestion pipeline, and full infrastructure deployment scripts using **Terraform**.

---

## Codebase Status Check
All components of the codebase are fully implemented and in place:
1. **Backend Service** ([backend/app](file:///Users/nikhilshrivastava/Desktop/code/repos/aws-docs-assistant/backend/app)): FastAPI endpoints, config settings, DB models/sessions, tools, and the LangGraph workflow.
2. **LangGraph Agent Workflow** ([backend/app/agents](file:///Users/nikhilshrivastava/Desktop/code/repos/aws-docs-assistant/backend/app/agents)): Classify, Rewrite, Retrieve, Grade, Search, Refuse, and Generate nodes.
3. **Ingestion Pipeline** ([backend/ingestion](file:///Users/nikhilshrivastava/Desktop/code/repos/aws-docs-assistant/backend/ingestion)): Ingestion runners, parsers, and Lambda trigger function for AWS S3 landing bucket uploads.
4. **Terraform Configurations** ([terraform](file:///Users/nikhilshrivastava/Desktop/code/repos/aws-docs-assistant/terraform)): Infrastructure configurations covering VPC networking, RDS PostgreSQL with pgvector, ECR repositories, App Runner serverless compute, IAM roles/policies, Secrets Manager secrets, and S3-SQS-Lambda event linkages.
5. **Interactive Clients**:
   - Terminal CLI client ([cli.py](file:///Users/nikhilshrivastava/Desktop/code/repos/aws-docs-assistant/cli.py))
   - Static Web Interface ([backend/app/static/index.html](file:///Users/nikhilshrivastava/Desktop/code/repos/aws-docs-assistant/backend/app/static/index.html))

---

## 1. Environment Variables Configuration

To run the application locally or deploy it to AWS, you need to configure the environment.

### Local Development Env (`backend/app/.env` or root `.env`)
Create a `.env` file in `backend/app/` (or in the repository root) containing the following variables:

```ini
# AWS Configuration
AWS_REGION=us-east-1
# Standard AWS credentials for Bedrock API access (or loaded from ~/.aws/credentials)
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
# Optional if using temporary AWS credentials:
# AWS_SESSION_TOKEN=your_aws_session_token

# Database Connection (pgvector on PostgreSQL)
# Default for a local postgres container:
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/aws_docs

# Amazon Bedrock Model IDs
BEDROCK_EMBED_MODEL_ID=amazon.titan-embed-text-v2:0
BEDROCK_CLASSIFY_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
BEDROCK_GENERATE_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0

# Live Web Search (Tavily Search API)
TAVILY_API_KEY=your_tavily_api_key
```

### Production Env (AWS Deployment via Terraform)
Terraform automatically manages:
- **`DATABASE_URL`**: Configured dynamically on AWS App Runner by pulling DB connection details and dynamic password credentials from AWS Secrets Manager.
- **`AWS_REGION`**: Passed automatically as a variable to App Runner.
- **IAM Policies**: The instance role attached to AWS App Runner includes permission to call Amazon Bedrock models (`bedrock:InvokeModel`).

---

## 2. Infrastructure Deployment (Terraform)

Follow these steps to deploy the resources (VPC, RDS PostgreSQL, App Runner, S3 bucket, SQS queue, Ingestion Lambda) on AWS:

### Prerequisites
1. Install [Terraform](https://developer.hashicorp.com/terraform/downloads).
2. Authenticate your terminal session with AWS. You can do this in one of two ways:

   **Method A: Export credentials directly in your terminal (Quickest)**
   ```bash
   export AWS_ACCESS_KEY_ID="your_aws_access_key_id"
   export AWS_SECRET_ACCESS_KEY="your_aws_secret_access_key"
   export AWS_DEFAULT_REGION="us-east-1"
   ```

   **Method B: Configure the AWS CLI (Persistent)**
   ```bash
   aws configure
   # Enter your AWS Access Key ID, AWS Secret Access Key, and default region (us-east-1) when prompted.
   ```

### Deployment Steps
1. Navigate to the terraform directory:
   ```bash
   cd terraform
   ```
2. Initialize Terraform (installs provider plug-ins):
   ```bash
   terraform init
   ```
3. Validate and preview the AWS resources to be created:
   ```bash
   terraform plan
   ```
4. Deploy the infrastructure to AWS:
   ```bash
   terraform apply
   ```
   *(Type `yes` when prompted to authorize the action)*

5. Retrieve output values (such as the ECR repository URL, App Runner endpoint, and S3 bucket name):
   ```bash
   terraform output
   ```

---

## 3. Deployment Flow (Docker Image to ECR)

Once Terraform creates the ECR repository, you must build and push the backend Docker image to run it in AWS App Runner:

1. Authenticate Docker to your AWS ECR Registry (replace `<AWS_ACCOUNT_ID>` and `<REGION>`):
   ```bash
   aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
   ```
2. Build the Docker image (run from the `backend/` directory or root depending on where Dockerfile is):
   ```bash
   docker build -t nikhil-aws-docs-assistant-backend:latest ./backend
   ```
3. Tag the image for ECR:
   ```bash
   docker tag nikhil-aws-docs-assistant-backend:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/nikhil-aws-docs-assistant-backend:latest
   ```
4. Push the image:
   ```bash
   docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/nikhil-aws-docs-assistant-backend:latest
   ```
5. Deploy to App Runner:
   - Go to AWS Console -> AWS App Runner -> Select `nikhil-aws-docs-assistant-backend` -> Click **Deploy** to pull the newly uploaded image.

---

## 4. Local Development & Testing

If you want to test and develop locally:

### Run Local Database
Use Docker to spin up a PostgreSQL instance with pgvector support:
```bash
docker run --name pgvector-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=aws_docs -p 5432:5432 -d pgvector/pgvector:pg15
```

### Install Dependencies & Seed Database
1. Set up python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt
   ```
2. Run database initialization script (creates schemas & table mappings):
   ```bash
   python3 backend/app/db/init_db.py
   ```
3. Ingest sample AWS documentation:
   ```bash
   python3 backend/ingestion/run_ingest_pipeline.py
   ```

### Start FastAPI Backend
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Accessing Clients
- **Web UI:** Open `http://localhost:8000/` in your browser.
- **CLI Chat Client:** Run from repository root:
  ```bash
  python3 cli.py
  ```