# Architecture Notes

## Data Flow
1. Device simulator runs on a GCP Compute Engine VM and publishes JSON messages to Pub/Sub.
2. Cloud Function validates payload, computes energy estimate, and writes to BigQuery.
3. Looker Studio reads from BigQuery and visualizes trends and alerts.

## Message Format (JSON)
- timestamp_utc (ISO 8601)
- classroom_id (string)
- temperature_c (float)
- light_lux (float)
- occupancy (int)

## BigQuery Table (sensor_readings)
- timestamp_utc (TIMESTAMP)
- classroom_id (STRING)
- temperature_c (FLOAT)
- light_lux (FLOAT)
- occupancy (INTEGER)
- energy_estimate_w (FLOAT)
- alert_flag (BOOLEAN)

## Energy Estimate (simple)
- Base load 50 W
- Add 10 W per occupant
- Add 0.05 W per lux

## Alert Logic
- If occupancy == 0 and light_lux > 200 then alert_flag = true
