import json
import os
import random
import time
from datetime import datetime, timezone

from google.cloud import pubsub_v1

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
TOPIC_ID = os.getenv("PUBSUB_TOPIC")
CLASSROOM_ID = os.getenv("CLASSROOM_ID", "B-201")
PUBLISH_INTERVAL_SEC = int(os.getenv("PUBLISH_INTERVAL_SEC", "5"))


def build_payload():
    now = datetime.now(timezone.utc).isoformat()
    temperature_c = round(random.uniform(23.0, 30.0), 1)
    light_lux = round(random.uniform(50.0, 600.0), 1)
    occupancy = random.randint(0, 30)
    return {
        "timestamp_utc": now,
        "classroom_id": CLASSROOM_ID,
        "temperature_c": temperature_c,
        "light_lux": light_lux,
        "occupancy": occupancy,
    }


def main():
    if not PROJECT_ID or not TOPIC_ID:
        raise SystemExit("GCP_PROJECT_ID and PUBSUB_TOPIC are required")

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

    while True:
        payload = build_payload()
        data = json.dumps(payload).encode("utf-8")
        future = publisher.publish(topic_path, data)
        future.result()
        print(f"Published: {payload}")
        time.sleep(PUBLISH_INTERVAL_SEC)


if __name__ == "__main__":
    main()
