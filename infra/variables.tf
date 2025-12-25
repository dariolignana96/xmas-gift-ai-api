variable "project_name" {
  description = "Nome del progetto"
  type        = string
  default     = "xmas-gift-ai"
}

variable "environment" {
  description = "Ambiente (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "Regione AWS"
  type        = string
  default     = "eu-west-1"
}

variable "vpc_cidr" {
  description = "CIDR block per la VPC"
  type        = string
  default     = "10.0.0.0/16"
}
