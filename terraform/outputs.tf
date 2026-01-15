output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.api.repository_url
}

output "ecr_repository_name" {
  description = "Name of the ECR repository"
  value       = aws_ecr_repository.api.name
}

output "ecr_repository_arn" {
  description = "ARN of the ECR repository"
  value       = aws_ecr_repository.api.arn
}

output "lambda_function_url" {
  description = "URL of the Lambda Function"
  value       = aws_lambda_function_url.api.function_url
}

output "lambda_function_name" {
  description = "Name of the Lambda Function"
  value       = aws_lambda_function.api.function_name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda Function"
  value       = aws_lambda_function.api.arn
}

