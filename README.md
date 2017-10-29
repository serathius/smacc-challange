# SMACC Email
Flask microservice to handle sending email.
I have 1 year of experience with flask.

Supported email services:
* Sendgrid (To test I created trial account, but after first request account was suspended.)

Tools used tools: docker, docker-compose, pip-tools, flake8, isort

# Setup

Install requirements locally:
```
pip install pip-tools
pip-sync requirements/*.txt
```

# Run

Configuration is available in file `docker-compose.yml` in environment of api service
Variables to configure:
* `SENDGRID_API_KEY`


Run:
```
docker-compose up
```

# Validate
```
curl -H "Content-Type: application/json" -X POST -d '{"from_email": "a@a@.pl", "to_email": "b@b.pl", "subject": "Test", "content": "Hello World"}' localhost/api/v1/email/
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
