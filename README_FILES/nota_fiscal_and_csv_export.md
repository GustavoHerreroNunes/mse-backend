# Nota Fiscal Module & CSV Export Feature

## Summary

This document describes the new `nota_fiscal` module and CSV export functionality added to the MSE-API.

## 1. Nota Fiscal Module

A new module has been created to manage the `tbl_nota_fiscal` table, following the same pattern as the `medicoes` module.

### File Structure
```
app/routes/financeiro/nota_fiscal/
├── __init__.py          # Blueprint setup and CORS configuration
├── schema.py            # Marshmallow schema for data validation
├── get_nota_fiscal.py   # GET endpoints for retrieving data
├── options.py           # OPTIONS handler for CORS preflight
└── export_csv.py        # CSV export endpoint
```

### API Endpoints

#### GET /nota_fiscal/
Get all notas fiscais within a date range.

**Query Parameters:**
- `data_inicial` (required): Start date (YYYY-MM-DD)
- `data_final` (required): End date (YYYY-MM-DD)

**Example:**
```
GET /nota_fiscal/?data_inicial=2025-01-01&data_final=2025-12-31
```

#### GET /nota_fiscal/by_id/<int:nota_id>
Get a specific nota fiscal by ID.

**Example:**
```
GET /nota_fiscal/by_id/123
```

#### GET /nota_fiscal/by_etl/<int:etl_id>
Get all notas fiscais for a specific ETL ID.

**Example:**
```
GET /nota_fiscal/by_etl/456
```

#### GET /nota_fiscal/export_csv
Export notas fiscais to CSV file within a date range.

**Query Parameters:**
- `data_inicial` (required): Start date (YYYY-MM-DD)
- `data_final` (required): End date (YYYY-MM-DD)

**Example:**
```
GET /nota_fiscal/export_csv?data_inicial=2025-01-01&data_final=2025-12-31
```

**Response:** CSV file download with filename pattern: `notas_fiscais_YYYY-MM-DD_to_YYYY-MM-DD_YYYYMMDD_HHMMSS.csv`

### Database Schema
The module manages the following fields from `tbl_nota_fiscal`:
- `id_nota` (PK) - Integer
- `tipo_nota` - Varchar(10)
- `nota_url` - Text
- `etl_id` - Integer
- `numero_nota` - Numeric
- `dt_emissao` - Date
- `dt_vencimento` - Date
- `valor_bruto` - Numeric(10,2)
- `valor_liquido` - Numeric(10,2)
- `descricao` - Text
- `valor_real` - Numeric(10,2)
- `valor_cotacao` - Numeric(10,2)
- `vlor_final` - Numeric(10,2)
- `dt_pagamento` - Date
- `status` - Varchar(10)

## 2. CSV Export Feature for Medicoes

A new CSV export endpoint has been added to the existing `medicoes` module.

### New Endpoint

#### GET /medicoes/export_csv
Export medicoes to CSV file within a date range.

**Query Parameters:**
- `data_inicial` (required): Start date (YYYY-MM-DD)
- `data_final` (required): End date (YYYY-MM-DD)

**Example:**
```
GET /medicoes/export_csv?data_inicial=2025-01-01&data_final=2025-12-31
```

**Response:** CSV file download with filename pattern: `medicoes_YYYY-MM-DD_to_YYYY-MM-DD_YYYYMMDD_HHMMSS.csv`

### CSV Columns (Medicoes)
- etl_id
- id_medicao
- id_demanda
- dt_medicao
- descricao
- valor_acordado
- total_medicao
- versao
- status
- numero
- ref_mse (nome_demanda from tbl_demandas)
- tipo_cobranca

### CSV Columns (Nota Fiscal)
- id_nota
- tipo_nota
- nota_url
- etl_id
- numero_nota
- dt_emissao
- dt_vencimento
- valor_bruto
- valor_liquido
- descricao
- valor_real
- valor_cotacao
- vlor_final
- dt_pagamento
- status

## 3. Integration

The `nota_fiscal` module has been integrated into the application:

1. **Blueprint Registration:** Added to `app/routes/__init__.py`
2. **App Registration:** Registered in `app/__init__.py` with all other blueprints
3. **URL Prefix:** `/nota_fiscal`

## 4. Features

Both modules now support:
- ✅ Date range filtering
- ✅ JSON API responses
- ✅ CSV export functionality
- ✅ CORS configuration
- ✅ Error handling and logging
- ✅ Data validation via Marshmallow schemas

## 5. Usage Examples

### Get Notas Fiscais as JSON
```bash
curl "http://localhost:5000/nota_fiscal/?data_inicial=2025-01-01&data_final=2025-12-31"
```

### Export Notas Fiscais as CSV
```bash
curl "http://localhost:5000/nota_fiscal/export_csv?data_inicial=2025-01-01&data_final=2025-12-31" -O -J
```

### Export Medicoes as CSV
```bash
curl "http://localhost:5000/medicoes/export_csv?data_inicial=2025-01-01&data_final=2025-12-31" -O -J
```

## 6. Notes

- CSV files are generated in memory (no temporary files)
- Filenames include timestamps for uniqueness
- Date filtering uses `dt_emissao` for nota_fiscal and `dt_medicao` for medicoes
- All responses include proper CORS headers
- CSV export returns 404 if no data found in the specified date range
- Date parameters are required for all endpoints
