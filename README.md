# Katas API

REST API built with FastAPI that solves three katas, deployed on AWS Lambda using Function URLs.

## Architecture

### Main Components

- **FastAPI Application**: REST API with three endpoints to solve katas
- **AWS Lambda**: Executes the application using Docker images
- **Lambda Function URL**: Exposes the API publicly without API Gateway
- **ECR (Elastic Container Registry)**: Stores Docker images of the application
- **Terraform**: Infrastructure as Code to manage all AWS resources
- **GitHub Actions**: CI/CD pipelines for automated build, push and deployment

### Data Flow

```
HTTP Client
    |
    v
Lambda Function URL (Public HTTPS)
    |
    v
Lambda Function (Docker Container)
    |
    v
Mangum (Adapter)
    |
    v
FastAPI Application
    |
    v
JSON Response
```

### AWS Infrastructure

- **Lambda Function**: Executes Docker image with FastAPI
- **ECR Repository**: Private registry for Docker images
- **IAM Role**: Permissions for Lambda (CloudWatch Logs)
- **S3 Bucket**: Terraform state storage
- **DynamoDB Table**: State locking for Terraform

## DevOps Implementation

### CI/CD Pipeline

The project implements a complete CI/CD pipeline using GitHub Actions:

#### 1. Docker Build Pipeline (`docker-build.yml`)

**Trigger**: Push to `main` branch

**Process**:

- Build Docker image using Dockerfile
- Tag image with commit SHA and `latest`
- Push to ECR using AWS credentials stored in GitHub Secrets

**Result**: New image available in ECR with `latest` tag

#### 2. Terraform Validation Pipeline (`terraform-validate.yml`)

**Trigger**: Push to `ludsrill` branch

**Process**:

- Format validation with `terraform fmt -check`
- Syntax validation with `terraform validate`
- Does not require AWS credentials (uses `-backend=false`)

**Purpose**: Detect configuration errors before deployment

#### 3. Terraform Plan Pipeline (`terraform-plan.yml`)

**Trigger**: Push to `ludsrill` branch

**Process**:

- Terraform initialization with S3 backend
- Execute `terraform plan`
- Shows proposed changes without applying them

**Purpose**: Review infrastructure changes before deployment

#### 4. Terraform Deploy Pipeline (`terraform-deploy.yml`)

**Trigger**: Push to `main` branch

**Process**:

- Terraform initialization with S3 backend
- Configuration validation
- Automatic plan and apply of changes
- Creates/updates AWS resources (Lambda, ECR, IAM, etc.)

**Result**: Infrastructure deployed and updated in AWS

#### 5. Lint Pipeline (`lint.yml`)

**Trigger**: Push to `ludsrill` branch

**Process**:

- Execute `ruff check` to validate Python code
- Uses lightweight Docker image (`python:3.11-slim`)

**Purpose**: Maintain code quality

### Secrets Management

Pipelines use GitHub Secrets to authenticate with AWS:

- `AWS_ACCESS_KEY_ID`: IAM User Access Key
- `AWS_SECRET_ACCESS_KEY`: Secret Access Key
- `AWS_REGION`: AWS region (optional, default: us-east-1)

### State Management

Terraform uses S3 backend to persist state:

- **S3 Bucket**: `codewars-katas-terraform-state-{account-id}`
- **DynamoDB Table**: `codewars-katas-terraform-lock` (state locking)
- **Versioning**: Enabled in S3 for change history
- **Encryption**: AES256 for state file security

### Deployment Order

1. Push to `main` executes Docker Build → image in ECR
2. Push to `main` executes Terraform Deploy → creates/updates Lambda
3. Lambda uses `latest` image from ECR
4. Function URL exposes API publicly

## Project Structure

```
python-tasks-katas/
├── app/
│   ├── main.py              # FastAPI application
│   ├── routers/             # API endpoints
│   └── katas/               # Kata logic
├── terraform/
│   ├── main.tf              # Main configuration
│   ├── lambda.tf            # Lambda Function and Function URL
│   ├── ecr.tf               # ECR Repository
│   ├── backend.tf           # S3 and DynamoDB for state
│   ├── variables.tf         # Configuration variables
│   └── outputs.tf           # Terraform outputs
├── .github/workflows/
│   ├── docker-build.yml     # Docker build and push
│   ├── terraform-deploy.yml # Infrastructure deployment
│   ├── terraform-plan.yml   # Change plan
│   ├── terraform-validate.yml # Terraform validation
│   └── lint.yml             # Code linting
├── Dockerfile               # Docker image for Lambda
├── lambda_handler.py        # Lambda handler (Mangum)
└── requirements.txt         # Python dependencies
```

## API Endpoints

### Dictionary (`/api/dictionary`)

- `POST /api/dictionary/newentry` - Add word to dictionary
- `GET /api/dictionary/look/{word}` - Look up word
- `GET /api/dictionary/entries` - List all entries

### Substring (`/api/substring`)

- `POST /api/substring/nth_char` - Get nth character from each word
- `GET /api/substring/nth_char?words=word1,word2` - GET version

### Spending (`/api/spending`)

- `POST /api/spending/total` - Calculate total cost of items

## Local Usage

### Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run local server
uvicorn app.main:app --reload
```

### Local Docker Build

```bash
# Build image
docker build -t codewars-katas .

# Run locally
docker run -p 8000:8000 codewars-katas
```

## Technologies Used

- **FastAPI**: Web framework for Python
- **AWS Lambda**: Serverless compute
- **AWS ECR**: Container registry
- **Terraform**: Infrastructure as Code
- **GitHub Actions**: CI/CD pipelines
- **Docker**: Containerization
- **Ruff**: Python linter

## Security Considerations

- Lambda Function URL with `NONE` authorization (public)
- CORS enabled for all origins
- Terraform state encrypted in S3
- AWS credentials stored in GitHub Secrets
- IAM Role with minimum necessary permissions

For production, consider:

- Function URL authentication (AWS_IAM)
- Rate limiting
- WAF for additional protection
- Secrets Manager for sensitive configuration
