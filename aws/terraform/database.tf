################################################################################
##                          CREATE DATABASE INSTANCE                          ##
################################################################################

locals {
  rds = {
    dev = {
      # Name
      db_name = "monitordb"

      # Instance type
      instance_class = "db.t3.micro"

      # Software
      engine               = "postgres"
      major_engine_version = "15"
      engine_version       = "15.3"
      family               = "postgres15"

      # Access
      username                            = "administrator"
      create_random_password              = false
      iam_database_authentication_enabled = false
      create_db_parameter_group           = false
      create_db_option_group              = false

      # Storage
      allocated_storage = 20 # gigabytes
      storage_type      = "gp2"
      storage_encrypted = true

      # Backup
      backup_retention_period = 7 # days
      skip_final_snapshot     = true
      deletion_protection     = false

      # Network
      multi_az            = false
      publicly_accessible = true
      port                = 5432
      network_type        = "IPV4"

      # Maintenance
      maintenance_window         = "Mon:03:00-Mon:04:30"
      auto_minor_version_upgrade = true

      # Monitoring
      enabled_cloudwatch_logs_exports       = ["postgresql", "upgrade"]
      create_cloudwatch_log_group           = true
      performance_insights_enabled          = true
      performance_insights_retention_period = 7 # days
      create_monitoring_role                = true
      monitoring_role_name                  = format("%s-%s-rds-monitoring-role", local.project_name, terraform.workspace)
      monitoring_interval                   = 60 # seconds
    }
  }
}

module "db" {
  source  = "terraform-aws-modules/rds/aws"
  version = "5.9.0"

  # Name
  db_name    = local.rds[terraform.workspace].db_name
  identifier = format("%s-%s", local.project_name, terraform.workspace)

  # Instance type
  instance_class = local.rds[terraform.workspace].instance_class

  # Software
  engine               = local.rds[terraform.workspace].engine
  engine_version       = local.rds[terraform.workspace].engine_version
  major_engine_version = local.rds[terraform.workspace].major_engine_version
  family               = local.rds[terraform.workspace].family

  # Access
  username                            = local.rds[terraform.workspace].username
  password                            = random_password.database.result
  create_random_password              = local.rds[terraform.workspace].create_random_password
  iam_database_authentication_enabled = local.rds[terraform.workspace].iam_database_authentication_enabled
  create_db_parameter_group           = local.rds[terraform.workspace].create_db_parameter_group
  create_db_option_group              = local.rds[terraform.workspace].create_db_option_group

  # Storage
  allocated_storage = local.rds[terraform.workspace].allocated_storage
  storage_type      = local.rds[terraform.workspace].storage_type
  storage_encrypted = local.rds[terraform.workspace].storage_encrypted

  # Backup
  backup_retention_period = local.rds[terraform.workspace].backup_retention_period
  skip_final_snapshot     = local.rds[terraform.workspace].skip_final_snapshot
  deletion_protection     = local.rds[terraform.workspace].deletion_protection

  # Network
  multi_az            = local.rds[terraform.workspace].multi_az
  publicly_accessible = local.rds[terraform.workspace].publicly_accessible
  port                = local.rds[terraform.workspace].port
  network_type        = local.rds[terraform.workspace].network_type
  # db_subnet_group_name   = module.vpc.
  # subnet_ids             = [module.vpc.public_subnets]
  vpc_security_group_ids = [aws_security_group.database.id]

  # Maintenance
  maintenance_window         = local.rds[terraform.workspace].maintenance_window
  auto_minor_version_upgrade = local.rds[terraform.workspace].auto_minor_version_upgrade

  # Monitoring
  enabled_cloudwatch_logs_exports       = local.rds[terraform.workspace].enabled_cloudwatch_logs_exports
  create_cloudwatch_log_group           = local.rds[terraform.workspace].create_cloudwatch_log_group
  performance_insights_enabled          = local.rds[terraform.workspace].performance_insights_enabled
  performance_insights_retention_period = local.rds[terraform.workspace].performance_insights_retention_period
  create_monitoring_role                = local.rds[terraform.workspace].create_monitoring_role
  monitoring_role_name                  = local.rds[terraform.workspace].monitoring_role_name
  monitoring_interval                   = local.rds[terraform.workspace].monitoring_interval

  parameters = [
    {
      name  = "autovacuum"
      value = 1
    },
    {
      name  = "client_encoding"
      value = "utf8"
    }
  ]
}
