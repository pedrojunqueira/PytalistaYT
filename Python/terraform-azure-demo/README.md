# Login to your Azure account
```bash
az login
```

# Set the subscription you want to use
```bash
DEFAULT_SUBSCRIPTION_ID=$(az account show --query id --output tsv)
az account set --subscription $DEFAULT_SUBSCRIPTION_ID
```
# Create the service principal
```bash
az ad sp create-for-rbac --name terraform-principal --role Contributor --scopes /subscriptions/$DEFAULT_SUBSCRIPTION_ID
```
# setup .env file with the variables

```txt
ARM_SUBSCRIPTION_ID=
ARM_CLIENT_ID=
ARM_CLIENT_SECRET=
ARM_TENANT_ID=
ARM_SERVICE_PRINCIPAL_NAME=
```

## terraform cli basic

# Initialize the working directory
```bash
terraform init
```
# Generate and show an execution plan
```bash
terraform plan
``` 
# Builds or changes infrastructure

```bash
terraform apply
```
# Build with auto approve i.e. not prompting for confirmation

```bash
terraform apply -auto-approve
```

# if you need to import any resource to your current state file
example for a resource group
```bash
terraform import azurerm_resource_group.appgrp /subscriptions/$DEFAULT_SUBSCRIPTION_ID/resourceGroups/terraform-rg
```

# Destroy the Terraform-managed infrastructure

```bash
terraform plan -destroy
terraform destroy
```
