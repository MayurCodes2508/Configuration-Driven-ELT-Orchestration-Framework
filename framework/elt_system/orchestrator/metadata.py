from loguru import logger as log

from elt_system.exceptions.exceptions import EXCEPTION_DESCRIPTIONS


class Metadata:
    def __init__(self, loader):

        self.job_cfg = loader.job_cfg

        log.info("Obj: metadata | Instance Initialized Successfully...")

        log.info("Metadata Loading Completed...")

    def get_metadata(self, key):

        self.jobType = key

    def build_job_metadata(
        self, jobRunID, jobName, status, errMsg, jobMetrics,
    ):

        try:
            metadata_dump = {
                "job_run_id": jobRunID,
                "job_name": jobName,
                "system": "elt",
                "job_type": self.jobType,
                "status": status,
                "error_message": errMsg,
                "job_metrics": jobMetrics,
            }

            log.info("Metadata Building Completed...")

            return metadata_dump

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}",
            )

            raise
