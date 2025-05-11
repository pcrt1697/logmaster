# log-master server

Main features:
* Endpoints to query log records;
* Endpoints to manage client applications;
* CLI to configure the Sink Connector.

## Set-Up local run
```bash
export LOGMASTER_KAFKA_CONNECT_URL="http:\\localhost\8083"
export LOGMASTER_KAFKA_BROKER_URL="http:\\localhost\29092"
export LOGMASTER_BACKEND_PORT=5050  # port used to expose rest APIs
export LOGMASTER_MONGO_URL="mongodb://logmaster:logmaster@localhost:27017/"
```

## Installation

```bash
pwd  # logmaster-server
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install setuptools
pip install -e .
```

## Initialization
To create the MongoDB Sink connector:
```bash
logmaster init
```

## Run
To start the FastAPI application:
```bash
logmaster run
```

Check out the swagger documentation at http://localhost:5050/api/v1/docs.
