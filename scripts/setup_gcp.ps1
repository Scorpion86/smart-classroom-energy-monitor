# PowerShell helper to create GCP resources
param(
  [Parameter(Mandatory=$true)][string]$ProjectId,
  [string]$TopicName = "classroom-sensors",
  [string]$Dataset = "iot_classroom",
  [string]$Table = "sensor_readings"
)

gcloud config set project $ProjectId

gcloud pubsub topics create $TopicName

bq --location=US mk --dataset "$ProjectId:$Dataset"

bq mk --table "$ProjectId:$Dataset.$Table" "data/bigquery_schema.json"
