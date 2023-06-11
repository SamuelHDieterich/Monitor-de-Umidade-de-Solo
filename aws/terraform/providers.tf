# Configure the AWS Provider
provider "aws" {
  region                   = local.default_region
  profile                  = terraform.workspace
  shared_credentials_files = ["config/aws_credentials.conf"]

  default_tags {
    tags = local.default_tags
  }
}
