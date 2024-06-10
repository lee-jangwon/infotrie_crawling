from pydantic import BaseModel, Field
from typing import Optional, Dict
from google.cloud import bigquery


class AddressDataModel(BaseModel):
    Street: str
    City: str
    State: str
    Country: str
    ZIP: str


class ListingsModel(BaseModel):
    Code: str
    Exchange: str
    Name: str


class OfficersModel(BaseModel):
    Name: str
    Title: str
    YearBorn: Optional[str] = None


class CompanyDataModel(BaseModel):
    company_id: str
    symbol_name: str
    symbol_code: str
    symbol_type: str
    exchange_name: str
    exchange_code: str
    exchange: str
    currency_symbol: str
    country_name: str
    country_iso: str
    figi: str
    isin: str
    lei: str
    primary_ticker: str
    cusip: str
    cik: str
    ein: str
    fiscal_year_end: str
    ipo_date: str
    international_domestic: str
    sector: str
    industry: str
    gic_sector: str
    gic_group: str
    gic_industry: str
    gic_sub_industry: str
    home_category: str
    is_delisted: bool
    description: str
    address: str
    address_data: AddressDataModel
    listings: Dict[str, ListingsModel]
    officers: Dict[str, OfficersModel]
    phone: str
    web_url: str
    logo_url: str
    full_time_employees: Optional[int] = None


BIGQUERY_SCHEMA = [
    bigquery.SchemaField("company_id", "STRING"),
    bigquery.SchemaField("symbol_name", "STRING"),
    bigquery.SchemaField("symbol_code", "STRING"),
    bigquery.SchemaField("symbol_type", "STRING"),
    bigquery.SchemaField("exchange_name", "STRING"),
    bigquery.SchemaField("exchange", "STRING"),
    bigquery.SchemaField("currency_code", "STRING"),
    bigquery.SchemaField("currency_name", "STRING"),
    bigquery.SchemaField("currency_symbol", "STRING"),
    bigquery.SchemaField("country_name", "STRING"),
    bigquery.SchemaField("country_iso", "STRING"),
    bigquery.SchemaField("figi", "STRING"),
    bigquery.SchemaField("isin", "STRING"),
    bigquery.SchemaField("lei", "STRING"),
    bigquery.SchemaField("primary_ticker", "STRING"),
    bigquery.SchemaField("cusip", "STRING"),
    bigquery.SchemaField("cik", "STRING"),
    bigquery.SchemaField("ein", "STRING"),
    bigquery.SchemaField("fiscal_year_end", "STRING"),
    bigquery.SchemaField("ipo_date", "STRING"),
    bigquery.SchemaField("international_domestic", "STRING"),
    bigquery.SchemaField("sector", "STRING"),
    bigquery.SchemaField("industry", "STRING"),
    bigquery.SchemaField("gic_sector", "STRING"),
    bigquery.SchemaField("gic_sub_industry", "STRING"),
    bigquery.SchemaField("home_category", "STRING"),
    bigquery.SchemaField("is_delisted", "STRING"),
    bigquery.SchemaField("description", "STRING"),
    bigquery.SchemaField("address", "STRING"),
    bigquery.SchemaField(
        "address_data",
        "RECORD",
        fields=[
            bigquery.SchemaField("Street", "STRING"),
            bigquery.SchemaField("City", "STREET"),
            bigquery.SchemaField("State", "STRING"),
            bigquery.SchemaField("Country", "STRING"),
            bigquery.SchemaField("ZIP", "STRING"),
        ],
    ),
    bigquery.SchemaField(
        "listings",
        "RECORD",
        mode="REPEATED",
        fields=[
            bigquery.SchemaField("Code", "STRING"),
            bigquery.SchemaField("Exchange", "STRING"),
            bigquery.SchemaField("Name", "STRING"),
        ],
    ),
    bigquery.SchemaField(
        "officers",
        "RECORD",
        mode="REPEATED",
        fields=[
            bigquery.SchemaField("Name", "STRING"),
            bigquery.SchemaField("Title", "STRING"),
            bigquery.SchemaField("YearBorn", "STRING"),
        ],
    ),
    bigquery.SchemaField("phone", "STRING"),
    bigquery.SchemaField("web_url", "STRING"),
    bigquery.SchemaField("logo_url", "STRING"),
    bigquery.SchemaField("full_time_employees", "INTEGER"),
]
