locals {
  recovery_window_in_days = {
    dev = 0
  }
}

# Create the secret string
# The resource generates a random permutation of alphanumeric characters and optionally special characters.

# Creates a random password for RDS (admin user)
resource "random_password" "database" {
  length           = 20
  special          = true
  min_special      = 5
  override_special = "!#&*()-_=+[]{}<>:?"
}
