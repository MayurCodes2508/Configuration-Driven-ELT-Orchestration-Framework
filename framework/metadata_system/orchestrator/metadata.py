from loguru import logger as log

from metadata_system.exceptions.exceptions import EXCEPTION_DESCRIPTIONS


class Metadata:
    def __init__(self, loader):

        self.job_cfg = loader.job_cfg

        log.info("Obj: metadata | Instance Initialized Successfully...")

        log.info("Metadata Loading Completed...")

    def get_metadata(self):

        try:
            ingestion_cfg = self.job_cfg.get("ingestion", {})

            storage_cfg = self.job_cfg.get("storage", {})

            processing_cfg = self.job_cfg.get("processing", {})

            serving_cfg = self.job_cfg.get("serving", {})

            exec_type = ["exec_type"]

            self.sub_jobtype = exec_type.split("ExecCmd", 1)[0]

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}",
            )

            raise

    def build_job_metadata(
        self, job_run_id, job_name, status, error_message, job_metrics,
    ):

        try:
            metadata_dump = {
                "job_run_id": job_run_id,
                "job_name": job_name,
                "system": "metadata",
                "job_type": self.job_type,
                "sub_jobtype": self.sub_jobtype,
                "status": status,
                "error_message": error_message,
                "job_metrics": job_metrics,
            }

            log.info("Metadata Building Completed...")

            return metadata_dump

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}",
            )

            raise
