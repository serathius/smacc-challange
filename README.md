# SMACC Email
Flask microservice to handle sending email

Tools used tools: docker, docker-compose, pip-tools, flake8, isort

# Setup

Install requirements locally:
```
pip install pip-tools
pip-sync requirements/*.txt
```

# Run

Run:
```
docker-compose up
```

# Static analysis

Perform static analysis:
```
flake8
```

# Test

Run tests:
```
pytest
```