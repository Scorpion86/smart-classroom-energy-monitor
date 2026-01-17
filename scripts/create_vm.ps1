# PowerShell helper to create a Compute Engine VM for the simulator
param(
  [Parameter(Mandatory=$true)][string]$ProjectId,
  [string]$VmName = "classroom-sim-vm",
  [string]$Zone = "us-central1-a",
  [string]$MachineType = "e2-micro"
)

gcloud config set project $ProjectId

gcloud compute instances create $VmName `
  --zone $Zone `
  --machine-type $MachineType `
  --image-family debian-12 `
  --image-project debian-cloud `
  --tags classroom-sim
