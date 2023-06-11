resource "aws_security_group" "database" {
  name        = format("%s-sg-rds", local.project_name)
  description = format("Security group for %s RDS", local.project_name)

  # vpc_id = module.vpc.vpc_id

  # Allow postgresql ingress traffic only
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    description = "PostgreSQL"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    description = "All traffic"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
