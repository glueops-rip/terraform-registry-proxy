terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
    # azurerm = {
    #   source = "localhost:8432/hashicorp/azurerm"
    # }
    # cloudflare = {
    #   source = "cloudflare/cloudflare"
    # }
  }
  
}

resource "aws_ssm_parameter" "foo" {
  name  = "foo"
  type  = "String"
  value = "bar"
}
