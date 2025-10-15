
MarketingGraph **Realistic Company-Sized** Dataset
==================================================
Master sizes:
- Campaigns: 650
- Products:  75
- Personas:  60
- Channels:  10
- Markets:   12
- Content:   900
- Date rows: 640 (2024-01-01 .. 2025-10-01)
Facts:
- PerformanceDaily: 3351 rows (~monthly snapshots per campaign; multiple channels if applicable).

All relationships are plausible:
- Campaigns map to 1 product, 1 persona, 1–3 channels, 1–5 content assets.
- Persona→Market aligns to persona.region; Product→Market has 1–3 markets each.
- Metrics are channel/region/category aware (CTR, CPL, CAC, ROAS consistent).

Load order:
Vertices → taxonomy edges → PERF_* link edges.
