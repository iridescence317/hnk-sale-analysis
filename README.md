# Side Project: Azure Data Engineering Pipeline
## 📝 Project Overview
This project is an automated, metadata-driven Data Engineering pipeline that performs incremental data extraction from an on-premises PostgreSQL database and processes it through a Medallion Architecture (Bronze to Silver) in Azure. It utilizes Azure Data Factory (ADF) for orchestration, Azure Databricks for data transformation (Delta Lake MERGE), and integrates automated pipeline monitoring with Microsoft Teams.

## 📖 Context
An FMCG enterprise (simulated with Heineken portfolio data) stores critical daily sales data—including orders, invoices, and customer channels—in an on-premises PostgreSQL database. This creates a data silo that prevents centralized, cloud-based analytics

## 🎯 Objectives
Build a fully automated, metadata-driven incremental pipeline that dynamically extracts only new or updated records, securely upserts them into an Azure Delta Lake (Medallion architecture), and provides real-time monitoring alerts via Microsoft Teams.

## 🏗️ Architecture & Tech Stack
- Source System: PostgreSQL (On-Premises / Localhost simulated)
- Data Ingestion & Orchestration: Azure Data Factory (ADF) with Self-Hosted Integration Runtime 
- Storage: Azure Data Lake Storage Gen2 (ADLS Gen2)
- Compute & Transformation: Azure Databricks (PySpark, Spark SQL, Unity Catalog)
- Security: Azure Key Vault (key-vault-scope) & ADF Managed Identity (MSI)
- Alerting: Microsoft Teams Webhook via Adaptive Cards
<img width="2226" height="601" alt="Architecture" src="https://github.com/user-attachments/assets/e4823b72-eb58-4912-9930-15bab0d0ad56" />


## 🗄️ Database & Source Setup
### Synthetic Data Generation
The project includes a robust Python script (generate_synthetic_data_and_seed()) utilizing the Faker and psycopg2 libraries to generate sample FMCG sales data.  
- Schema: sellout
- Tables: customers, products (Heineken portfolio), orders, and invoices.
Note: An automatic seed_heineken_data.sql backup is generated during the Python run

### Control Table (Unity Catalog)
The pipeline relies on a Databricks Delta table named incremental_load_metadata to track watermarks. It stores:
- Source schemas and entities
- Target storage paths
- last_extraction_date
- Primary keys for upsert logic

## ⚙️ Pipeline Workflow
- Master Orchestration (pl_sales_hnk_main): This is the parent controller. It triggers the actual data load process and waits to see if it succeeds or fails
- Dynamic Data Processing (pl_sales_hnk): This is the core engine. It automatically figures out which tables need to be moved. For each table, it extracts the new data, upserts it into your target storage, and updates the tracking metadata so it knows where to start next time
- Automated Alerting (pl_teams_notification & Teams Workflow): As soon as the data processing finishes (or if it crashes), a webhook is fired off. Microsoft Teams catches this webhook and immediately posts a color-coded summary card (green for success, red for failure) in your chat, complete with a direct link to the pipeline run logs

## 🔐 Security & Access Control
- ADF Authentication: ADF authenticates to Databricks using its System-Assigned Managed Identity (MSI).
- Databricks Authentication to ADLS: Databricks uses OAuth 2.0 with a Service Principal to read/write to ADLS Gen2. Credentials (client-id, tenant-id, client-secret) are securely retrieved from an Azure Key Vault secret scope (key-vault-scope).
- Unity Catalog Permissions: The ADF Managed Identity is explicitly granted USAGE on the catalog/schema and SELECT/MODIFY on the control tables via SQL GRANT statements





