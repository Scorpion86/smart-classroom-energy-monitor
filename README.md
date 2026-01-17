# Smart Classroom Energy Monitor (GCP PoC)

Proof-of-concept IoT application for CPC357 Assignment 2.

## Architecture
- Device simulator runs on a GCP Compute Engine VM and publishes sensor data to Pub/Sub.
- Cloud Function validates/enriches messages and writes to BigQuery.
- Looker Studio connects to BigQuery for dashboards.

## Components
- `simulator/`: Python script to simulate sensors and publish JSON.
- `functions/ingest/`: Cloud Function for ingestion and validation.
- `data/`: Sample payloads and BigQuery schema.
- `docs/`: Design notes and diagrams description.
- `scripts/`: Helper scripts to set up GCP resources and deploy functions.

## Quick Start (Local Simulator)
1. Install Python 3.10+.
2. `pip install -r simulator/requirements.txt`
3. Copy `.env.example` and set `GCP_PROJECT_ID`.
4. Set env vars: `GCP_PROJECT_ID`, `PUBSUB_TOPIC`.
5. `python simulator/simulate_device.py`

## Setup Helpers
- Create GCP resources:
  - `scripts/setup_gcp.ps1 -ProjectId <your-project-id>`
- Deploy Cloud Function:
  - `scripts/deploy_function.ps1 -ProjectId <your-project-id>`
- Create VM for simulator:
  - `scripts/create_vm.ps1 -ProjectId <your-project-id>`

## Notes
- BigQuery dataset/table must exist before ingestion.
- See `docs/architecture.md` for data flow and design decisions.
