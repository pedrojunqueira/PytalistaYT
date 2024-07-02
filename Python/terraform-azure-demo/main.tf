terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.110.0"
    }
  
  }
}

provider "azurerm" {
  features {
    
  }
}

resource "azurerm_resource_group" "terraform-rg" {
  name     = "terraform-rg"
  location = "australiasoutheast"
}

resource "azurerm_storage_account" "storageaccount" {
  name                     = "stgpedrojunqueiraio42"
  resource_group_name      = azurerm_resource_group.terraform-rg.name
  location                 = azurerm_resource_group.terraform-rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

}