# Smart Classroom Energy Monitor (GCP PoC)

Proof-of-concept IoT application for CPC357 Assignment 2. The device layer is a GCP Compute Engine VM running a simulator that publishes classroom sensor readings to Pub/Sub. A Cloud Function processes the messages and writes them to BigQuery. Looker Studio visualizes the data.

## Architecture (High Level)
- Compute Engine VM (device simulator) -> Pub/Sub -> Cloud Function -> BigQuery -> Looker Studio

## Repository Structure
- `simulator/`: Device simulator that publishes JSON messages.
- `functions/ingest/`: Pub/Sub-triggered Cloud Function that validates/enriches and writes to BigQuery.
- `data/`: BigQuery schema and sample payload.
- `scripts/`: Helper scripts for VM setup and Cloud Function deployment.
- `docs/`: Architecture notes and setup guides.

## Prerequisites
- GCP project with billing enabled.
- `gcloud` and `bq` CLI installed and authenticated.
- Python 3.10+ on the VM (Debian 12).

## GCP Services Enabled (Used in This Project)
```powershell
# Run on local machine
gcloud services enable pubsub.googleapis.com --project <PROJECT_ID>
gcloud services enable bigquery.googleapis.com --project <PROJECT_ID>
gcloud services enable cloudfunctions.googleapis.com --project <PROJECT_ID>
gcloud services enable cloudbuild.googleapis.com --project <PROJECT_ID>
gcloud services enable artifactregistry.googleapis.com --project <PROJECT_ID>
```

## GCP Setup (Commands Actually Used)
```powershell
# Set active project
gcloud config set project <PROJECT_ID>

# Create Pub/Sub topic
gcloud pubsub topics create classroom-sensors --project <PROJECT_ID>

# Create BigQuery dataset and table
bq --location=US mk --dataset <PROJECT_ID>:iot_classroom
bq mk --table <PROJECT_ID>:iot_classroom.sensor_readings data/bigquery_schema.json
```

## VM (Device Simulator)
Create the VM from the repo root:
```powershell
.\scripts\create_vm.ps1 -ProjectId <PROJECT_ID>
```

SSH into the VM and install dependencies:
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv git
```

Clone the repo and run the simulator:
```bash
git clone https://github.com/Scorpion86/smart-classroom-energy-monitor.git
cd smart-classroom-energy-monitor
python3 -m venv .venv
source .venv/bin/activate
pip install -r simulator/requirements.txt

export GCP_PROJECT_ID=<PROJECT_ID>
export PUBSUB_TOPIC=classroom-sensors
export CLASSROOM_ID=B-201

python simulator/simulate_device.py
```

## Cloud Function Deployment
Deploy the function from the repo root:
```powershell
.\scripts\deploy_function.ps1 -ProjectId <PROJECT_ID>
```

## IAM Permissions (Applied)
These were required for successful deployment and runtime:
- `roles/pubsub.publisher` for the VM service account.
- `roles/run.invoker` for the function's Cloud Run service.
- `roles/bigquery.dataEditor` and `roles/bigquery.jobUser` for the function service account.
- `roles/storage.objectViewer` on `gcf-v2-sources-<PROJECT_NUMBER>-us-central1` bucket.
- `roles/cloudbuild.builds.builder`, `roles/storage.admin`, `roles/artifactregistry.writer` for Cloud Build deployment.

## Verify Data in BigQuery
```powershell
bq query --use_legacy_sql=false "SELECT * FROM `<PROJECT_ID>.iot_classroom.sensor_readings` ORDER BY timestamp_utc DESC LIMIT 5"
```

## Looker Studio Dashboard
1. Create a report in Looker Studio.
2. Add BigQuery as data source: `<PROJECT_ID>` -> `iot_classroom` -> `sensor_readings`.
3. Build charts (KPI scorecards, time series, alerts table).

## Notes
- If the BigQuery dataset already exists, the `bq mk` command will return an "already exists" message.
- Simulator publishes every 5 seconds by default (configurable via `PUBLISH_INTERVAL_SEC`).

## Clean Submission Checklist
- Repo contains only used code and setup guides (no secrets, no local artifacts).
- `.env` is excluded; only `.env.example` is included.
- Cloud Function deploy script uses correct env var formatting.
- BigQuery dataset/table exist in US region and are populated.
- VM simulator publishes to `classroom-sensors` and BigQuery shows rows.
- Looker Studio dashboard is created and screenshots are captured.

## Docs
- `docs/architecture.md`: architecture details.
- `docs/development_guide.md`: development steps.
- `docs/vm_setup.md`: VM-specific setup.
- `docs/report_outline.md`: report skeleton aligned with rubric.
