import os
import pandas as pd
from sqlalchemy import create_engine, text

# ✏️ EDIT THESE:
CSV_DIR = r"/workspaces/Market_Ontology/datasets"   # folder containing Campaign.csv, Product.csv, ...
CONN_STR = "postgresql+psycopg2://postgres:password@localhost:5432/marketing_db"

DDL = r"""
CREATE SCHEMA IF NOT EXISTS marketing;
SET search_path TO marketing, public;
CREATE TABLE IF NOT EXISTS campaign (campaign_id text PRIMARY KEY, campaign_name text NOT NULL, objective text, kind text, status text, start_date timestamp, end_date timestamp, budget numeric);
CREATE TABLE IF NOT EXISTS product (sku text PRIMARY KEY, product_name text NOT NULL, category text, tier text);
CREATE TABLE IF NOT EXISTS persona (persona_id text PRIMARY KEY, segment text, industry text, region text, role text);
CREATE TABLE IF NOT EXISTS channel (channel_id text PRIMARY KEY, kind text, cost_model text);
CREATE TABLE IF NOT EXISTS market (market_id text PRIMARY KEY, region text, competitors text, trend_index numeric);
CREATE TABLE IF NOT EXISTS content_asset (content_id text PRIMARY KEY, content_title text, content_kind text, topic text, url text);
CREATE TABLE IF NOT EXISTS date_dim (date_key text PRIMARY KEY, date_value timestamp NOT NULL, year int NOT NULL, month int NOT NULL, day int NOT NULL, week int, quarter int);
CREATE TABLE IF NOT EXISTS performance_daily (perf_id text PRIMARY KEY, as_of timestamp NOT NULL, currency text NOT NULL, impressions integer, clicks integer, spend numeric, leads integer, opps integer, customers integer, revenue numeric, ctr numeric, cpl numeric, cac numeric, roas numeric);
CREATE TABLE IF NOT EXISTS promotes (campaign_id text REFERENCES campaign(campaign_id), sku text REFERENCES product(sku), PRIMARY KEY (campaign_id, sku));
CREATE TABLE IF NOT EXISTS targets (campaign_id text REFERENCES campaign(campaign_id), persona_id text REFERENCES persona(persona_id), PRIMARY KEY (campaign_id, persona_id));
CREATE TABLE IF NOT EXISTS runs_on (campaign_id text REFERENCES campaign(campaign_id), channel_id text REFERENCES channel(channel_id), PRIMARY KEY (campaign_id, channel_id));
CREATE TABLE IF NOT EXISTS supported_by (campaign_id text REFERENCES campaign(campaign_id), content_id text REFERENCES content_asset(content_id), PRIMARY KEY (campaign_id, content_id));
CREATE TABLE IF NOT EXISTS in_market (sku text REFERENCES product(sku), market_id text REFERENCES market(market_id), PRIMARY KEY (sku, market_id));
CREATE TABLE IF NOT EXISTS persona_in_market (persona_id text REFERENCES persona(persona_id), market_id text REFERENCES market(market_id), PRIMARY KEY (persona_id, market_id));
CREATE TABLE IF NOT EXISTS perf_date (perf_id text REFERENCES performance_daily(perf_id) ON DELETE CASCADE, date_key text REFERENCES date_dim(date_key), PRIMARY KEY (perf_id, date_key));
CREATE TABLE IF NOT EXISTS perf_campaign (perf_id text REFERENCES performance_daily(perf_id) ON DELETE CASCADE, campaign_id text REFERENCES campaign(campaign_id), PRIMARY KEY (perf_id, campaign_id));
CREATE TABLE IF NOT EXISTS perf_product (perf_id text REFERENCES performance_daily(perf_id) ON DELETE CASCADE, sku text REFERENCES product(sku), PRIMARY KEY (perf_id, sku));
CREATE TABLE IF NOT EXISTS perf_persona (perf_id text REFERENCES performance_daily(perf_id) ON DELETE CASCADE, persona_id text REFERENCES persona(persona_id), PRIMARY KEY (perf_id, persona_id));
CREATE TABLE IF NOT EXISTS perf_channel (perf_id text REFERENCES performance_daily(perf_id) ON DELETE CASCADE, channel_id text REFERENCES channel(channel_id), PRIMARY KEY (perf_id, channel_id));
CREATE TABLE IF NOT EXISTS perf_market (perf_id text REFERENCES performance_daily(perf_id) ON DELETE CASCADE, market_id text REFERENCES market(market_id), PRIMARY KEY (perf_id, market_id));
CREATE TABLE IF NOT EXISTS perf_content (perf_id text REFERENCES performance_daily(perf_id) ON DELETE CASCADE, content_id text REFERENCES content_asset(content_id), PRIMARY KEY (perf_id, content_id));
"""

ORDER = [
    ("campaign",       "Campaign.csv"),
    ("product",        "Product.csv"),
    ("persona",        "Persona.csv"),
    ("channel",        "Channel.csv"),
    ("market",         "Market.csv"),
    ("content_asset",  "Content.csv"),
    ("date_dim",       "Date.csv"),
    ("performance_daily", "PerformanceDaily.csv"),
    ("promotes",       "PROMOTES.csv"),
    ("targets",        "TARGETS.csv"),
    ("runs_on",        "RUNS_ON.csv"),
    ("supported_by",   "SUPPORTED_BY.csv"),
    ("in_market",      "IN_MARKET.csv"),
    ("persona_in_market", "PERSONA_IN_MARKET.csv"),
    ("perf_date",      "PERF_DATE.csv"),
    ("perf_campaign",  "PERF_CAMPAIGN.csv"),
    ("perf_product",   "PERF_PRODUCT.csv"),
    ("perf_persona",   "PERF_PERSONA.csv"),
    ("perf_channel",   "PERF_CHANNEL.csv"),
    ("perf_market",    "PERF_MARKET.csv"),
    ("perf_content",   "PERF_CONTENT.csv"),
]

def load_csv(engine, table, filename):
    path = os.path.join(CSV_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    print(f"Loading {filename} -> {table}")
    df = pd.read_csv(path)
    # fast path: use COPY via psycopg2 if available; else to_sql
    with engine.begin() as conn:
        # create temp table and try COPY
        try:
            raw_conn = conn.connection
            with raw_conn.cursor() as cur, open(path, "r", encoding="utf-8") as f:
                cur.copy_expert(f"COPY marketing.{table} FROM STDIN WITH CSV HEADER", f)
            print(f"COPY ok: {filename}")
        except Exception as e:
            print(f"COPY failed ({e}); falling back to to_sql...")
            df.to_sql(table, conn, schema="marketing", if_exists="append", index=False)

def main():
    engine = create_engine(CONN_STR)
    with engine.begin() as conn:
        conn.execute(text("SET search_path TO marketing, public"))
        conn.execute(text(DDL))
    for table, file in ORDER:
        load_csv(engine, table, file)
    print("All done.")

if __name__ == "__main__":
    main()
