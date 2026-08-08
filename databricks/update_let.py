# Databricks notebook source
# MAGIC %skip
# MAGIC %sql
# MAGIC select * from ntuyendb.default.incremental_load_metadata

# COMMAND ----------

tgt_entity = dbutils.widgets.get("entity")

# COMMAND ----------

query = f"""
UPDATE ntuyendb.default.incremental_load_metadata
SET last_extraction_date = current_timestamp()
WHERE target_entity_name = '{tgt_entity}'
"""

spark.sql(query)