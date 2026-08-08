```SQL
CREATE TABLE IF NOT EXISTS incremental_load_metadata (
    source_name STRING COMMENT 'Name of the source system (e.g., ERP, CRM)',
    source_schema STRING COMMENT 'Schema of the source database',
    source_entity STRING COMMENT 'Name of the source table or view',
    watermark STRING COMMENT 'Incremental logic (e.g., where created_at >= <<last_ext_date>>)',
    source_type STRING COMMENT 'Type of source (e.g., sql_server, postgres, api)',
    is_active BOOLEAN COMMENT 'Flag to easily toggle loads on/off',
    target_container STRING COMMENT 'Target storage container/bucket',
    target_path STRING COMMENT 'Path within the target container',
    target_entity_name STRING COMMENT 'Name of the target table or file',
    last_extraction_date TIMESTAMP COMMENT 'last date ingesting this table',
    key STRING COMMENT 'Unique key used for upsert data'
)
USING DELTA
COMMENT 'Control table storing metadata and watermarks for incremental data pipelines.';
```

```SQL
INSERT INTO incremental_load_metadata (
    source_name,
    source_schema,
    source_entity,
    watermark,
    source_type,
    is_active,
    target_container,
    target_path,
    target_entity_name,
    last_extraction_date,
    key
) VALUES
    ('heineken_sellout_db', 'sellout', 'customers', 'where created_at >= <<last_ext_date>> or updated_at >= <<last_ext_date>>', 'postgre', true, 'dls', 'bronze/sales/', 'customers', '1900-01-01 00:00:00', 'customer_id'),
    ('heineken_sellout_db', 'sellout', 'invoices', 'where created_at >= <<last_ext_date>> or updated_at >= <<last_ext_date>>', 'postgre', true, 'dls', 'bronze/sales/', 'invoices', '1900-01-01 00:00:00', 'invoice_id'),
    ('heineken_sellout_db', 'sellout', 'orders', 'where created_at >= <<last_ext_date>> or updated_at >= <<last_ext_date>>', 'postgre', true, 'dls', 'bronze/sales/', 'orders', '1900-01-01 00:00:00', 'order_id'),
    ('heineken_sellout_db', 'sellout', 'products', 'where created_at >= <<last_ext_date>> or updated_at >= <<last_ext_date>>', 'postgre', true, 'dls', 'bronze/sales/', 'products', '1900-01-01 00:00:00', 'product_id');
```

```SQL
-- 1. Allow the SPN to see the catalog
GRANT USAGE ON CATALOG ntuyendb TO `Managed Identity Application ID of ADF`;

-- 2. Allow the SPN to see the schema (database)
GRANT USAGE ON SCHEMA ntuyendb.default TO `Managed Identity Application ID of ADF`;

-- 3. Allow the SPN to read your metadata table
GRANT SELECT ON TABLE ntuyendb.default.incremental_load_metadata TO `Managed Identity Application ID of ADF`;

-- 4. Allow the SPN to modify metadata table
GRANT MODIFY ON TABLE ntuyendb.default.your_target_table TO `Managed Identity Application ID of ADF`;
```
