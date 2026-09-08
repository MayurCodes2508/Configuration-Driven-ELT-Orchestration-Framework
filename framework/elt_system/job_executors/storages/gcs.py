import io
from datetime import datetime, timezone

import pandas as pd
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
        self.layer = storage_cfg["layer"]
        self.format = storage_cfg["format"]
        self.path_template = storage_cfg["path_template"]

        self.data = data

        self.jobRunID = jobRunID

        log.info("Obj: gcsdest | Instance Initialized Successfully...")

        log.info("Dest Metadata Loading Completed...")

    def build_path(self):

        now = datetime.now(tz=timezone.utc)

        try:
            path_context = {
                "layer": self.layer,
                "source": self.source,
                "dataset": self.dataset,
                "entity": self.entity,
                "jobRunID": self.jobRunID,
                "ingestionDT": now.strftime("%Y-%m-%d"),
                "ingestionTS": now.strftime("%Y%m%dT%H%M%SZ"),
                "format": self.format,
            }

            self.formatted_path = self.path_template.format(**path_context)

            log.info(f"Successfully created and formatted path: {self.formatted_path}")

            return self.formatted_path, now

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

            if not data:
                raise ValueError("No data received to upload")

            df = pd.DataFrame(data)

            df["ingestion_timestamp"] = now

            log.info(
                "Successfully converted the raw JSON data to Pandas DataFrame and added ingestion metadata(ingestion_timestamp)",
            )

            buffer = io.BytesIO()

            df.to_parquet(buffer, index=False, compression="snappy")

            log.info(
                "Successfully converted, compressed to Parquet & finished writing it to RAM buffer",
            )

            buffer.seek(0)

            blob.upload_from_file(buffer, content_type="application/octet-stream")

            log.info("Successfully uploaded the parquet data to GCS")

            return len(df), self.formatted_path

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}",
            )

            raise

    def run(self):

        path, now = self.build_path()

        rows_stored, bucket_path_stored = self.upload_to_gcs(path=path, data=self.data, now=now)

        job_metrics = {"rows_stored": rows_stored,
                       "bucket_path_stored": bucket_path_stored}

        return job_metrics