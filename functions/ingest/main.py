import base64
import json
import os
from datetime import datetime, timezone

from google.cloud import bigquery

BQ_DATASET = os.getenv("BQ_DATASET", "iot_classroom")
BQ_TABLE = os.getenv("BQ_TABLE", "sensor_readings")
DEFAULT_CLASSROOM_ID = os.getenv("DEFAULT_CLASSROOM_ID", "B-201")

REQUIRED_FIELDS = [
    "classroom_id",
    "temperature_c",
    "light_lux",
    "occupancy",
]


def _parse_message(event):
    if "data" not in event:
        raise ValueError("Missing data field")
    payload = base64.b64decode(event["data"]).decode("utf-8")
    return json.loads(payload)


def _coerce_float(value, field_name):
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid float for {field_name}")


def _coerce_int(value, field_name):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid int for {field_name}")


def _energy_estimate_w(occupancy, light_lux):
    base_load = 50.0
    return base_load + (10.0 * occupancy) + (0.05 * light_lux)


def _alert_flag(occupancy, light_lux):
    return occupancy == 0 and light_lux > 200.0


def ingest_pubsub(event, context):
    message = _parse_message(event)

    missing = [field for field in REQUIRED_FIELDS if field not in message]
    if missing:
        raise ValueError(f"Missing fields: {', '.join(missing)}")

    timestamp = message.get("timestamp_utc") or datetime.now(timezone.utc).isoformat()
    classroom_id = message.get("classroom_id") or DEFAULT_CLASSROOM_ID

    temperature_c = _coerce_float(message.get("temperature_c"), "temperature_c")
    light_lux = _coerce_float(message.get("light_lux"), "light_lux")
    occupancy = _coerce_int(message.get("occupancy"), "occupancy")

    if occupancy < 0:
        raise ValueError("Occupancy must be >= 0")

    row = {
        "timestamp_utc": timestamp,
        "classroom_id": classroom_id,
        "temperature_c": temperature_c,
        "light_lux": light_lux,
        "occupancy": occupancy,
        "energy_estimate_w": _energy_estimate_w(occupancy, light_lux),
        "alert_flag": _alert_flag(occupancy, light_lux),
    }

    client = bigquery.Client()
    table_id = f"{client.project}.{BQ_DATASET}.{BQ_TABLE}"
    errors = client.insert_rows_json(table_id, [row])
    if errors:
        raise RuntimeError(f"BigQuery insert errors: {errors}")

    return "ok"
