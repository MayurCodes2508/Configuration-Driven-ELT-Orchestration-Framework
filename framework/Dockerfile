FROM python:3.12.3-slim

WORKDIR /framework

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN dbt deps --project-dir ./metadata_system/dbt/

ENTRYPOINT [ "python", "-u", "-m" ]
