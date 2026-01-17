# VM Setup for Simulator (Compute Engine)

## Create VM
- `scripts/create_vm.ps1 -ProjectId <your-project-id>`

## SSH into VM
- `gcloud compute ssh classroom-sim-vm --zone us-central1-a`

## Install Python and dependencies
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip git
```

## Copy project to VM
Option A (recommended): clone your repo
```bash
git clone <your-repo-url>
cd smart-classroom-energy-monitor
```

Option B: upload just the simulator folder
```bash
gcloud compute scp --recurse simulator classroom-sim-vm:~/simulator --zone us-central1-a
```

## Run simulator on VM
```bash
export GCP_PROJECT_ID=<your-project-id>
export PUBSUB_TOPIC=classroom-sensors
export CLASSROOM_ID=B-201
pip install -r simulator/requirements.txt
python simulator/simulate_device.py
```

## Notes
- Ensure the VM service account has Pub/Sub Publisher role.
- Keep the simulator running while you collect dashboard screenshots.
