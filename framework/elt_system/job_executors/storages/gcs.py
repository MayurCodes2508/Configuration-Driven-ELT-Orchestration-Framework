import io
import json
from datetime import datetime as dt
from datetime import timezone as tz

from google.cloud import storage
from loguru import logger as log

from elt_system.exceptions.exceptions import EXCEPTION_DESCRIPTIONS


class Gcs:
    def __init__(self, storage_cfg, metadata_cfg, data, jobRunID):

        self.metadata_cfg = metadata_cfg
        self.source = metadata_cfg["source"]
        self.dataset = metadata_cfg["dataset"]
        self.entity = metadata_cfg["entity"]

        self.destination_cfg = storage_cfg
        self.bucket = storage_cfg["bucket"]
        self.format = storage_cfg["format"]
        self.path_template = storage_cfg["path_template"]

        self.data = data

        self.jobRunID = jobRunID

        log.info("Obj: gcsdest | Instance Initialized Successfully...")

        log.info("Dest Metadata Loading Completed...")

    def build_path(self):

        try:
            path_context = {
                "source": self.source,
                "dataset": self.dataset,
                "entity": self.entity,
                "jobRunID": self.jobRunID,
                "ingestionDT": dt.now(tz=tz.utc).date(),
                "ingestionTS": dt.now(tz=tz.utc).isoformat(sep="|"),
                "format": self.format,
            }

            self.formatted_path = self.path_template.format(**path_context)

            log.info(f"Successfully created and formatted path: {self.formatted_path}")

            return self.formatted_path, path_context["ingestionTS"]

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}",
            )

            raise

    def upload_to_gcs(self, path, data, now):

        try:
            storage_client = storage.Client()

            bucket = storage_client.bucket(self.bucket)

            blob = bucket.blob(path)

            for record in data:
                record["ingestion_timestamp"] = now

            log.info(
                "Successfully Added the ingestion_timestamp column to all records",
            )

            blob.upload_from_file(
                io.BytesIO(json.dumps(obj=data, default=str).encode("utf-8")),
                content_type="application/json",
            )

            log.info("Successfully uploaded the data to GCS")

            return len(data), self.formatted_path

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}",
            )

            raise

    def run(self):

        path, now = self.build_path()

        rows_stored, bucket_path_stored = self.upload_to_gcs(
            path=path,
            data=self.data,
            now=now,
        )

        job_metrics = {
            "rows_stored": rows_stored,
            "bucket_path_stored": bucket_path_stored,
        }

        return job_metrics
