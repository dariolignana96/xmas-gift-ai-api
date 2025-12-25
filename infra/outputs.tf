output "vpc_id" {
  description = "ID della VPC"
  value       = aws_vpc.xmas_gift_vpc.id
}

output "vpc_arn" {
  description = "ARN della VPC"
  value       = aws_vpc.xmas_gift_vpc.arn
}
