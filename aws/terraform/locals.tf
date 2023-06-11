# Defines global data that will be used for multiple resources
locals {
  default_region = "us-east-1"
  default_tags = {
    DRI         = "Samuel"
    Environment = terraform.workspace
    GithubRepo  = local.github_repo
    Terraform   = true
  }
  github_repo  = "Monitor-de-Umidade-de-Solo"
  project_name = "monitor-de-umidade-de-solo"
}
