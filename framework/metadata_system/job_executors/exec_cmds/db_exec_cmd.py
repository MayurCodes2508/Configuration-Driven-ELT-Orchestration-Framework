import psycopg2
from loguru import logger as log

from metadata_system.exceptions.exceptions import EXCEPTION_DESCRIPTIONS
from metadata_system.job_executors.auth.auth import Auth


class DBExecCommand:
    def __init__(self, exec_cfg, metadata_cfg):

        self.metadata_cfg = metadata_cfg

        self.source = self.metadata_cfg["source"]

        self.dataset = self.metadata_cfg["dataset"]

        self.entity = self.metadata_cfg["entity"]

        self.exec_cfg = exec_cfg

        table = exec_cfg["table"]

        self.table = table.format(dataset=self.dataset)

        query = exec_cfg["query"]

        self.query = query.format(table=self.table)

        self.auth_cfg = exec_cfg["auth"]

        self.auth_type = self.auth_cfg["auth_type"]

        self.secret = Auth.get_auth(auth_cfg=self.auth_cfg, auth_type=self.auth_type)

        log.info("Obj: dbexeccmd | Instance Initialization Completed...")

        log.info("Exec Metadata Loading Completed...")

    def query_db(self):

        try:
            with psycopg2.connect(self.secret) as conn:
                with conn.cursor() as cursor:
                    select_query = f"{self.query}"

                    cursor.execute(query=select_query)

                    log.info("Extraction From DB Completed...")

                    self.data = cursor.fetchall()

                    self.rows_processed = len(self.data)

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}",
            )

            raise

    def run(self):

        self.query_db()

        job_metrics = {"rows_processed": self.rows_processed}

        return self.data, job_metrics
