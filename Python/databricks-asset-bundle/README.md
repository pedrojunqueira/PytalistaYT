# DAB

What are Databricks Asset Bundles

Databricks Asset Bundles are a tool to facilitate the adoption of software engineering best practices, including source control, code review, testing, and continuous integration and delivery (CI/CD), for your data and AI projects. Bundles make it possible to describe Databricks resources such as jobs, pipelines, and notebooks as source files.

[documentation](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/)

### Main Settings reference

[Main settings reference](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/settings) for Databricks Asset Bundles

### Pre-requisites to follow this tutorial

1. Azure Databricks Workspace Account
2. Install databricks-cli -> [databricks-cli](https://docs.databricks.com/en/dev-tools/cli/install.html)
3. Python 3.8 or higher
4. Git
6. VS Code

#### git init

```bash
git init
```
#### create .gitignore file

```bash
.databricks/
build/
dist/
__pycache__/
*.egg-info
.venv/
scratch/**
!scratch/README.md
```

#### login to databricks

```bash
databricks auth login --host https://adb-3304201807713135.15.azuredatabricks.net
```

#### set configuration

```bash
databricks configure --token
```
-   Create a token if you do not have one 
-   Enter workspace url and token

#### location of databricks configuration file

cat ~/.databrickscfg

#### databricks bundle workflow

create bundle

```bash
databricks bundle init
```

-   Chose only job, not python package or pipeline
-   Change directory to your project

```bash
cd dab_project/
``` 

#### structure of the initial project

```bash
.
├── README.md
├── databricks.yml
├── fixtures
├── resources
│   └── dab_project_job.yml
├── scratch
│   ├── README.md
│   └── exploration.ipynb
└── src
    └── notebook.ipynb
```

deploy the bundle

```bash
databricks bundle validate
```

- on validation a `.databricks` folder is created
- files are pushed to the workspace
- if no target are specified, the default target, which is development, is used

```bash
databricks bundle deploy -t dev
```
- terraform files are created with state and resources
- the resources are pushed to the workspace
- the dev jobs comes with a prefix [dev_user_name]
- on the jobs there is a warning that the job job was created by a bundle and should not be edited

```bash
databricks bundle run -t dev dab_project_job
```

- the job is run

### deploying to production

```bash
databricks bundle validate -t prod
databricks bundle deploy -t prod
```

## destroy bundle

```bash
databricks bundle destroy
```

```bash
databricks bundle destroy -t prod --auto-approvecd 
```

### Minimal project structure to create a bundle from scratch

```bash
.
├── databricks.yml
├── resources
│   └── first_job.yml
└── src
    └── first_project
        └── notebook.ipynb
```

### databricks.yml

```yaml
bundle:
  name: dab_project
  
include:
  - ./resources/first_job.yml

targets:
  dev:
    default: true
    mode: development
    workspace:
      host: https://<workspace-url>.azuredatabricks.net
  prod:
    mode: production
    run_as:
      user_name: pedro.junqueira@agile-analytics.com.au
    workspace:
      host: https://<workspace-url>.azuredatabricks.net
```

### first_job.yml

```yaml
resources:
  jobs:
      first_job:
        name: first_job
        tasks:
          - task_key: notebook_task
            new_cluster:
              spark_version: 13.3.x-scala2.12
              node_type_id: Standard_DS3_v2
              num_workers: 1
            notebook_task:
              notebook_path: ../src/first_project/notebook.ipynb
```

### navigating the databricks API to write bundle

#### Example with job create API -> YML https://docs.databricks.com/api/azure/workspace/jobs/create

