# Xmas Gift AI API - Design IaC (SOLO STUDIO, NO APPLY)
# Questo è un esercizio di Infrastructure as Code, non creare risorse reali

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "xmas_gift_vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    Name        = "--vpc"
    Project     = var.project_name
    Environment = var.environment
  }
}
