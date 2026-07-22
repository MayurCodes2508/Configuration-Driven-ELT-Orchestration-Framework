from loguru import logger as log


class Metadata:
    def __init__(self, loader):

        self.job_cfg = loader.job_cfg

        log.info("Obj: metadata | Instance Initialized Successfully...")

        log.info("Metadata Loading Completed...")

    def get_metadata(self):

        exec_cfg = self.job_cfg["exec"]

        dest_cfg = self.job_cfg.get("dest", {})

        self.job_type = "extraction"

        if dest_cfg:
            self.job_type = "ingestion"

        exec_type = exec_cfg["exec_type"]

        self.sub_jobtype = exec_type.split("ExecCmd", 1)[0]

    def build_job_metadata(
        self, job_run_id, job_name, status, error_message, job_metrics
    ):

        metadata_dump = {
            "job_run_id": job_run_id,
            "job_name": job_name,
            "system": "el",
            "job_type": self.job_type,
            "sub_jobtype": self.sub_jobtype,
            "status": status,
            "error_message": error_message,
            "job_metrics": job_metrics,
        }

        log.info("Metadata Building Completed...")

        return metadata_dump
