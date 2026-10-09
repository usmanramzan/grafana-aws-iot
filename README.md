# AWS IoT Shadow to InfluxDB and Grafana example

This repository contains two small Python scripts showing an AWS IoT Device Shadow workflow and a local time-series visualization path:

- `IoT_Pub.py` connects to AWS IoT Core and sends a reported-state shadow update.
- `grafana-sub.py` repeatedly requests a named shadow, reads reported state fields, writes them to InfluxDB, and prints the received payload.

Grafana is not configured by these scripts. They only illustrate the data path; you must set up AWS IoT Core, InfluxDB, and Grafana separately.

## Requirements

- Python 3 and pip
- The AWS IoT Python SDK (`AWSIoTPythonSDK`)
- The InfluxDB Python client (`influxdb`) for `grafana-sub.py`
- An AWS IoT Thing with a Device Shadow and certificates authorized to connect and read or update that shadow
- A reachable InfluxDB instance and a Grafana instance configured to query it

The repository does not pin Python or package versions, provide a dependency lockfile, or configure Grafana dashboards or data sources.

## Configure and run

1. In both scripts, replace the AWS IoT endpoint, certificate paths, and Thing Shadow name with values for your AWS account. Keep the private key and certificates outside the repository; do not commit credentials.
2. Configure the InfluxDB connection and database used by `grafana-sub.py` for your environment. The checked-in script currently contains a database password in source; treat it as exposed, rotate it if it was ever valid, and move connection settings to a secure configuration mechanism before use.
3. Install the Python dependencies in your environment. For example:

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install AWSIoTPythonSDK influxdb
   ```

4. Start `grafana-sub.py` to poll the configured shadow and write readings. Run `IoT_Pub.py` to send a shadow update. Configure Grafana separately to use the InfluxDB database and measurement.

## Data shape and limitations

The publisher currently sends placeholder `key1`–`key4` values. The subscriber expects `red`, `blue`, `green`, and `color` under `state.reported`, so the sample payloads do not match without editing. The publisher also calls `time.sleep` without importing `time`, and its interrupt cleanup refers to `GPIO` without defining or importing it. The subscriber uses a broad exception handler and polls every two seconds; it has no retry policy, schema validation, or graceful shutdown logic beyond process interruption.

There is no automated setup for AWS resources, InfluxDB, Grafana, or deployment. Runtime compatibility has not been tested as part of this documentation refresh.
