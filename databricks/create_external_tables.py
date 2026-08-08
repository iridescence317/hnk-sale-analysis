# Databricks notebook source
# MAGIC %sql
# MAGIC create schema ntuyendb.sales

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS ntuyensa_silver
# MAGIC URL 'abfss://dls@ntuyensa.dfs.core.windows.net/silver'
# MAGIC WITH (STORAGE CREDENTIAL adls_access);

# COMMAND ----------

# DBTITLE 1,customers
# MAGIC %sql
# MAGIC CREATE TABLE ntuyendb.sales.customers
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://dls@ntuyensa.dfs.core.windows.net/silver/sales/customers'
# MAGIC COMMENT 'Customers data';

# COMMAND ----------

# DBTITLE 1,products
# MAGIC %sql
# MAGIC CREATE TABLE ntuyendb.sales.products
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://dls@ntuyensa.dfs.core.windows.net/silver/sales/products'
# MAGIC COMMENT 'Products data';

# COMMAND ----------

# DBTITLE 1,orders
# MAGIC %sql
# MAGIC CREATE TABLE ntuyendb.sales.orders
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://dls@ntuyensa.dfs.core.windows.net/silver/sales/orders'
# MAGIC COMMENT 'Orders data';

# COMMAND ----------

# DBTITLE 1,invoices
# MAGIC %sql
# MAGIC CREATE TABLE ntuyendb.sales.invoices
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://dls@ntuyensa.dfs.core.windows.net/silver/sales/invoices'
# MAGIC COMMENT 'Invoices data';