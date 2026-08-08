# Databricks notebook source
from delta.tables import DeltaTable

# COMMAND ----------

tgt_container = dbutils.widgets.get("container")
tgt_path = dbutils.widgets.get("path")
tgt_entity = dbutils.widgets.get("entity")
key = dbutils.widgets.get("key")

# COMMAND ----------

scope_name = "key-vault-scope"
client_id = dbutils.secrets.get(scope=scope_name, key="client-id")
tenant_id = dbutils.secrets.get(scope=scope_name, key="tenant-id")
client_secret = dbutils.secrets.get(scope=scope_name, key="client-secret")

storage_account = "ntuyensa"

spark.conf.set(f"fs.azure.account.auth.type.{storage_account}.dfs.core.windows.net", "OAuth")
spark.conf.set(f"fs.azure.account.oauth.provider.type.{storage_account}.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set(f"fs.azure.account.oauth2.client.id.{storage_account}.dfs.core.windows.net", client_id)
spark.conf.set(f"fs.azure.account.oauth2.client.secret.{storage_account}.dfs.core.windows.net", client_secret)
spark.conf.set(f"fs.azure.account.oauth2.client.endpoint.{storage_account}.dfs.core.windows.net", f"https://login.microsoftonline.com/{tenant_id}/oauth2/token")

# COMMAND ----------

bronze_path = f"abfss://{tgt_container}@{storage_account}.dfs.core.windows.net/{tgt_path}{tgt_entity}.parquet"
silver_path = bronze_path.replace("bronze", "silver").replace(".parquet", "")

try:
    df = spark.read.format("parquet").load(bronze_path)
    
    if DeltaTable.isDeltaTable(spark, bronze_path):
        print(f"Upsert data for table {tgt_entity}")

        df.createOrReplaceTempVIew(tgt_entity)

        query = f"""
            MERGE INTO delta.`{silver_path}` as dest
            USING `{tgt_entity}` as src
            ON dest.{key} = src.{key}
            WHEN MATCHED THEN
                UPDATE SET *
            WHEN NOT MATCHED
                THEN INSERT *
        """
        spark.sql(query)
    else:
        print(f"Write data for table {tgt_entity}")
        df.write.format("delta").mode("overwrite").save(silver_path)

except Exception as e:
    print(e)