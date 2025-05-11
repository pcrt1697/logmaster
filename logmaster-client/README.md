# logmaster-client

## Installation

```bash
pwd  # logmaster-client
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install setuptools
pip install -e .
```

## Usage
The main utility is [`KafkaLogHandler`](../src/logmaster/client/logger.py) which is the log handler that send log messages to Kafka.
The client application is created when the handler is created for the first time.

A few examples [here](scripts/sample_client.py).
