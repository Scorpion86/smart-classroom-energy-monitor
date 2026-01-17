# Smart Classroom Energy Monitor - Development Guide

## Prerequisites
- GCP project with billing enabled
- Python 3.10+
- gcloud CLI installed and authenticated

## Setup
1. Create Pub/Sub topic:
   - `gcloud pubsub topics create classroom-sensors`
2. Create BigQuery dataset and table:
   - Dataset: `iot_classroom`
   - Table: `sensor_readings`
   - Schema: `data/bigquery_schema.json`
3. Deploy Cloud Function:
   - Name: `ingest_pubsub`
   - Trigger: Pub/Sub topic `classroom-sensors`
   - Env vars: `BQ_DATASET=iot_classroom`, `BQ_TABLE=sensor_readings`
4. Create Compute Engine VM to run the simulator:
   - See `docs/vm_setup.md`

## Run Simulator (on VM)
- Set env vars:
  - `GCP_PROJECT_ID=<your-project-id>`
  - `PUBSUB_TOPIC=classroom-sensors`
  - `CLASSROOM_ID=B-201`
- `pip install -r simulator/requirements.txt`
- `python simulator/simulate_device.py`

## Looker Studio
1. Connect Looker Studio to BigQuery table.
2. Build charts:
   - Time series of temperature, light, occupancy.
   - KPI for energy_estimate_w.
   - Filter for alert_flag = true.
3. Capture screenshots for report.

## Security Notes
- Use least-privilege service accounts for publisher and function.
- Restrict BigQuery dataset permissions to group members.
