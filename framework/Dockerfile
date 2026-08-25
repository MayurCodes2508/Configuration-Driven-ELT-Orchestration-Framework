FROM python:3.12.3-slim

WORKDIR /framework

COPY requirements.txt .

ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN dbt deps --project-dir ./metadata_system/dbt/

ENTRYPOINT [ "python", "-u", "-m" ]
