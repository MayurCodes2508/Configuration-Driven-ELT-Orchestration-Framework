from uuid import UUID

from loguru import logger as log


class Metadata:
    def __init__(
        self,
        jobRunID: UUID,
        pipelineRunID: UUID,
        jobName: str,
    ) -> None:

        self.jobRunID: UUID = jobRunID
        self.pipelineRunID: UUID = pipelineRunID
        self.jobName: str = jobName

        log.info("Obj: metadata | Instance Initialized Successfully...")

        log.info("Metadata Loading Completed...")

    def build_job_metadata(
        self,
        jobType: str,
        status: str,
        created_at=None,
        start_time=None,
        end_time=None,
        errMsg=None,
        jobMetrics=None,
    ) -> dict:

        metadata_dump: dict = {
            "run_id": self.jobRunID,
            "pipeline_run_id": self.pipelineRunID,
            "job_name": self.jobName,
            "job_type": jobType,
            "status": status,
            "created_at": created_at,
            "start_time": start_time,
            "end_time": end_time,
            "error_message": errMsg,
            "job_metrics": jobMetrics,
        }

        log.info("Metadata Building Completed...")

        return metadata_dump
