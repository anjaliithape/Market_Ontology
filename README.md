# Marketing Ontology Dataset

## Dimension Tables

| **File** | **Entity** | **Description** |
|-----------|-------------|-----------------|
| **Campaign.csv** | Marketing campaign | Defines campaigns with ID, name, objectives, start/end dates, budget, and status. |
| **Product.csv** | Product or service | Lists SKUs, names, categories, and tiers of promoted products. |
| **Persona.csv** | Customer persona | Represents target audience segments (industry, role, region, buyer type). |
| **Channel.csv** | Marketing channel | Communication medium such as Email, Search, Social, Event, or Paid Media. |
| **Market.csv** | Geographic or business market | Contains regional info, competitors, and trend index. |
| **Content.csv** | Marketing assets | Ads, blogs, whitepapers, webinars, and other collateral used in campaigns. |
| **Date.csv** | Time dimension | Provides `date_key`, `year`, `month`, `quarter`, and `day` for time-based analysis. |

---

## Fact Table — PerformanceDaily.csv

| **Metric Group** | **Metrics** | **Meaning & Business Insight** |
|------------------|-------------|--------------------------------|
| **Engagement Volume** | `impressions`, `clicks` | Measure visibility and audience engagement.<br>• **Impressions** — how many times ads or posts were displayed.<br>• **Clicks** — number of user interactions.<br>High impressions but low clicks may indicate weak ad creatives or poor targeting. |
| **Funnel Conversions** | `leads`, `opps`, `customers` | Track progress through the funnel.<br>• **Leads** — prospects showing interest.<br>• **Opportunities** — qualified potential buyers.<br>• **Customers** — converted paying clients.<br>Helps pinpoint where prospects drop off. |
| **Financial Metrics** | `spend`, `revenue` | Capture cost vs. return.<br>• **Spend** — total marketing investment.<br>• **Revenue** — income attributed to that campaign.<br>Indicates profitability and efficiency. |
| **Derived KPIs (Efficiency Ratios)** | `ctr`, `cpl`, `cac`, `roas` | Computed from the base metrics:<br>• **CTR (Click-Through Rate)** = `clicks ÷ impressions` — engagement strength.<br>• **CPL (Cost per Lead)** = `spend ÷ leads` — efficiency of lead generation.<br>• **CAC (Customer Acquisition Cost)** = `spend ÷ customers` — cost per conversion.<br>• **ROAS (Return on Ad Spend)** = `revenue ÷ spend` — revenue generated per ₹1 spent.<br>Reveal ROI and performance efficiency across campaigns. |

---

## Link (Relationship) Tables

### Campaign-Centric Relationships

| **File** | **Relation** | **Description** |
|-----------|--------------|-----------------|
| **PROMOTES.csv** | Campaign → Product | Defines which products each campaign promotes. |
| **TARGETS.csv** | Campaign → Persona | Specifies which personas are targeted by the campaign. |
| **RUNS_ON.csv** | Campaign → Channel | Lists which channels deliver each campaign. |
| **SUPPORTED_BY.csv** | Campaign → Content | Links campaigns to the supporting marketing assets. |

---

### Market Relationships

| **File** | **Relation** | **Description** |
|-----------|--------------|-----------------|
| **IN_MARKET.csv** | Product → Market | Indicates where each product is sold or promoted. |
| **PERSONA_IN_MARKET.csv** | Persona → Market | Shows where each persona is active or relevant. |

---

### Fact-to-Dimension Relationships

| **File** | **Relation** | **Description** |
|-----------|--------------|-----------------|
| **PERF_DATE.csv** | Performance → Date | Links each performance record to a calendar date. |
| **PERF_CAMPAIGN.csv** | Performance → Campaign | Identifies which campaign generated the metrics. |
| **PERF_PRODUCT.csv** | Performance → Product | Associates performance with the promoted product. |
| **PERF_PERSONA.csv** | Performance → Persona | Maps metrics to audience segments. |
| **PERF_CHANNEL.csv** | Performance → Channel | Tracks which channel delivered the results. |
| **PERF_MARKET.csv** | Performance → Market | Connects metrics to a geographic or business market. |
| **PERF_CONTENT.csv** | Performance → Content | Associates performance data with specific content assets. |
