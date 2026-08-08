# Databricks notebook source
import json

# COMMAND ----------

tbl_name = dbutils.widgets.get("table_name")
src_schema = dbutils.widgets.get("source_schema")

# COMMAND ----------

df = spark.sql(f"""
SELECT 
    source_entity,
    watermark,
    target_container,
    target_path,
    target_entity_name,
    last_extraction_date,
    key
FROM ntuyendb.default.incremental_load_metadata 
WHERE source_schema = '{src_schema}' and source_entity = '{tbl_name}'
""")

# COMMAND ----------

config_info = df.first()
if config_info:
    return_values = {
        "table_name" : config_info["source_entity"],
        "target_container": config_info["target_container"],
        "target_path": config_info["target_path"],
        "target_entity_name": config_info["target_entity_name"],
        "last_extraction_date": config_info["last_extraction_date"],
        "watermark": config_info["watermark"],
        "key": config_info["key"]
    }

    json_output = json.dumps(return_values, default=str)
else:
    return_values = {
        "table_name" : None,
        "target_container": None,
        "target_path": None,
        "target_entity_name": None,
        "last_extraction_date": '1900-01-01 00:00:00.000',
        "watermark": None,
        "key": None
    }

    json_output = json.dumps(return_values, default=str)

dbutils.notebook.exit(json_output)