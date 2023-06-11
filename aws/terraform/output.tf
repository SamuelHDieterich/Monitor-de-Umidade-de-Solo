output "db_instance_address" {
  description = "The address of the RDS instance"
  value       = module.db.db_instance_address
}

output "db_instance_username" {
  description = "The username for the database"
  value       = nonsensitive(module.db.db_instance_username)
}

output "database_password" {
  description = "The password for the database"
  value       = nonsensitive(random_password.database.result)
}
