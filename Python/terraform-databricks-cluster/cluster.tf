terraform {
  required_providers {
    databricks= {
        source = "databricks/databricks"
        version = "1.48.2"
    }
  }
}

provider "databricks" {
  profile = "DEFAULT"
}

variable "cluster_name" {}
variable "cluster_autotermination_minutes" {}
variable "cluster_num_workers" {}
variable "cluster_data_security_mode" {}

data "databricks_node_type" "smallest" {
  local_disk = true
}

data "databricks_spark_version" "latest_lts" {
  long_term_support = true
}

resource "databricks_cluster" "this" {
    cluster_name = var.cluster_name
    node_type_id = data.databricks_node_type.smallest.id
    spark_version = data.databricks_spark_version.latest_lts.id
    autotermination_minutes = var.cluster_autotermination_minutes
    num_workers = var.cluster_num_workers
    data_security_mode = var.cluster_data_security_mode
    custom_tags = {
      "admin" = "pedrocj@gmail.com"
    }
  
}

output "cluster_url" {
  value = databricks_cluster.this.url
}



