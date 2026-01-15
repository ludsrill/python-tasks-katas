terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Backend S3 - Descomenta después de crear el bucket y DynamoDB
  # Ejecuta primero: terraform apply (sin backend)
  # Luego descomenta esto y ejecuta: terraform init -migrate-state
  backend "s3" {
    bucket         = "codewars-katas-terraform-state-343218193902"
    key            = "codewars-katas/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "codewars-katas-terraform-lock"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
}

