FROM python:3.6.2-alpine
RUN pip install --upgrade pip
COPY requirements/app.txt /requirements
RUN pip install -r /requirements
WORKDIR /app
COPY smacc_email /app/smacc_email
COPY common /app/common
COPY swagger/email.yml /app/swagger/email.yml
COPY setup.py /app/setup.py
RUN pip install --editable /app
ENV FLASK_APP smacc_email.app:api
EXPOSE 80
CMD ["gunicorn", "-c", "/app/common/gunicorn_config.py", "smacc_email.app:api"]

