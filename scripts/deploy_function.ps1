# PowerShell helper to deploy Cloud Function
param(
  [Parameter(Mandatory=$true)][string]$ProjectId,
  [string]$TopicName = "classroom-sensors",
  [string]$FunctionName = "ingest_pubsub",
  [string]$Region = "us-central1",
  [string]$Dataset = "iot_classroom",
  [string]$Table = "sensor_readings"
)

gcloud config set project $ProjectId

gcloud functions deploy $FunctionName `
  --region $Region `
  --runtime python310 `
  --trigger-topic $TopicName `
  --entry-point ingest_pubsub `
  --set-env-vars "BQ_DATASET=$Dataset,BQ_TABLE=$Table" `
  --source functions/ingest
