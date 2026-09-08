from datetime import datetime

from google.cloud import bigquery as bqcl
from loguru import logger as log


class BQ:
    def __init__(self, dest_cfg, data):

        self.dest_cfg = dest_cfg

        self.schema = dest_cfg["schema"]

        self.table = dest_cfg["table"]

        self.table_id = f"{self.schema}.{self.table}"

        self.data = data

        log.info("Obj: bqdest | Instance Initialized Successfully...")

        log.info("Dest Metadata Loading Completed...")

    def write_to_dest(self):

        try:
            ingestion_ts = datetime.now().isoformat()

            self.data = [row + (ingestion_ts,) for row in self.data]

            bq_client = bqcl.Client(
                location="asia-south1", project="instant-medium-491107-t6",
            )

            self.table = bq_client.get_table(table=self.table_id)

            bq_client.insert_rows(table=self.table, rows=self.data)

            log.info("Writing to BQ Dest Completed...")

        except Exception:
            log.exception("Unknown BigQuery Client Error Occured")

    def run(self):

        self.write_to_dest()
