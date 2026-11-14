# Terra Analog Atlas

A runnable regional terrain-analog explorer built from real NASA-derived elevation data. It ranks **42 non-overlapping Earth patches** against fixed **lunar south-pole and Jezero crater windows**. Every footprint is 20 × 20 km and each main analysis grid is 500 m.

**This is a complete terrain-first hackathon MVP, not a validated global analog-discovery system.** Mineralogy, atmosphere, gravity, radiation, ground mechanics and base suitability are not scored. No model accuracy or match probability is claimed.

## Run the finished explorer (no installation beyond Python)

Unzip the project and open a terminal in the extracted `Terra_Analog_Atlas` directory:

```sh
python run.py
```

The launcher opens **http://localhost:8000**. The measured feature snapshot, hillshades, country outline map and ranking work offline. Optional OpenStreetMap tiles and external source links need internet. Do not double-click `index.html`; browsers block its local JSON requests.

Windows users can use `py` instead of `python` if necessary. No GPU, cloud subscription, Earthdata password or AI API key is needed to run the included app.

## Python pipeline and optional API

Python 3.11 or later is recommended; the build was tested on Python 3.12.14 on Linux. Create a virtual environment, activate it, then:

```sh
python -m pip install -e .
python -m pytest -q
python -m uvicorn analog_atlas.api:app --host 127.0.0.1 --port 8001
```

API documentation: **http://localhost:8001/docs**. The deployed web app is static and uses the same tested scoring formula locally; the optional FastAPI service is supplied for backend integration, not running in the static deployment.

Example request:

```sh
curl -X POST http://localhost:8001/rank -H "Content-Type: application/json" -d '{"target_id":"jezero","limit":5,"weights":{"slope":1,"relief":1,"roughness":1}}'
```

For PowerShell, use the interactive `/docs` page or `Invoke-RestMethod` rather than relying on shell-specific quote escaping.

## Reproduce from source rasters

The archive includes compact processed 500 m GeoTIFFs. Full original rasters are approximately 190 MB and are intentionally downloaded separately:

```sh
python -m scripts.download_data --output data/raw
python -m scripts.build_dataset --raw data/raw
python -m scripts.build_overlays
python -m pytest -q
```

Public NASA/PDS and USGS archives provide the Moon and Mars products. NASADEM is retrieved from Microsoft's public Planetary Computer mirror using a temporary anonymous SAS token kept only in memory. Upstream services may change or be unavailable; the released snapshot remains runnable. `data/provenance.json` records the original build's checksums; compare these to a new acquisition before replacing evidence. A mirror COG has different bytes from an Earthdata HGT ZIP even when its elevation samples agree.

## What is included

| Path | Purpose |
|---|---|
| `dist/` | Complete static explorer with vendored map library and data |
| `analog_atlas/features.py` | Slope, relief, local plane-detrended RMS roughness |
| `analog_atlas/preprocess.py` | Metric reprojection and area averaging |
| `analog_atlas/ranking.py` | Frozen-IQR, family-weighted distance |
| `analog_atlas/api.py` | Validated FastAPI adapter |
| `scripts/` | Source acquisition, preprocessing, display overlays and packaging |
| `data/processed/` | Actual 500 m grids, body CRS and nodata preserved |
| `data/provenance.json` | Input checksums, sizes and source links |
| `dist/data/atlas.json` | Features, geometry, scaler, PCA coordinates and measured checks |
| `Quickstart.ipynb` | Notebook for inspecting data and ranking in Jupyter or Colab |
| `tests/` | Analytic terrain, missing-data, API and browser/Python parity tests |
| `docs/` | Method, integration contract, scientific validation plan and demo script |
| `presentation/` | Editable presentation deck |

## Use the explorer

1. Choose Mars or Moon. The map focuses on the region containing the closest candidate.
2. Compare the five feature measurements and the separately scaled hillshades.
3. Filter a region or adjust family weights. The Earth scaling reference stays fixed.
4. Select another row or map footprint; export its evidence JSON, all ranked CSV rows, or GeoJSON.
5. Read the method and evidence sections. PCA is an exploratory learned projection, not a proven ranking improvement.

The top candidate is only best **among these 42 patches, for the selected target, scale, descriptors and weights**. Four lunar descriptors exceed the Earth reference range; the interface explicitly flags this. Never describe a distance as “% Mars” or “% Moon.”

## Measured build results

Default equal-family weights put Atacama 09 first for the Jezero window (distance approximately 0.064) and Hawaiʻi 11 first for the lunar window (approximately 0.859). These values are computed distances, not independently validated relevance. Their numerical sizes should not be compared between targets as a universal quality measure.

All six single-family ±20% weight perturbations for each target preserve the top-ten set. The 1 km joint scale/grid test also preserves the top-ten sets; it changes neighbourhood sizes and may shift target footprints by up to 500 m. PCA retaining >=95% variance needs three components and produces a top-ten Jaccard overlap of 9/11 with the baseline. This does **not** establish that PCA is better or worse scientifically. See the exact machine-readable results and limitations in `docs/validation_results.json`.

## Extension priorities

First obtain dimension-specific expert relevance labels and region-held-out evaluation. Then add documented geology units and appropriate quality-controlled climate/context products. Only evaluate image embeddings after assembling cross-body imagery with comparable physical scale, illumination/registration controls and held-out evaluation. Deep learning on 42 unlabeled patches is not justified.

## Attribution and reuse

This is an independent project, not a NASA product or endorsement. NASADEM (NASA MEaSUREs), LRO LOLA (NASA PDS), and Mars 2020 CTX terrain (NASA/JPL, USGS archive) retain their source attribution. Leaflet's BSD license is included. Natural Earth map data are public domain. Optional OpenStreetMap tiles retain their attribution. Source data terms remain with the original providers. See `THIRD_PARTY_NOTICES.md`.

The original feasibility plan is provided as research context. Its “not yet implemented” statements describe the earlier planning stage; this README and technical report describe the released build. Full challenge-specific detailed rules and submission limits could not be independently recovered, so this package does not assert formal submission compliance.
