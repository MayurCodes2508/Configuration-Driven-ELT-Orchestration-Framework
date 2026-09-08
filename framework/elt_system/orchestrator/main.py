import os
import sys
from uuid import UUID

from fastapi import APIRouter as apir
from loguru import logger as log
from uuid6 import uuid7 as uid

from elt_system.orchestrator.loader import JobConfigLoader
from elt_system.orchestrator.metadata import Metadata
from elt_system.orchestrator.runner import Runner
from elt_system.orchestrator.validator import Validator

log.remove()

log.add(
    sink=sys.stdout,
    filter=lambda record: (
        record["level"].name
        in {"INFO", "SUCCESS", "ERROR", "WARNING", "DEBUG", "TRACE"}
    ),
)

log.add(sink=sys.stderr, filter=lambda record: record["level"].name == "CRITICAL")


class Main:
    def __init__(self):

        pass

    ##### Helper Functions :3 #####

    def build_run_id(self):

        runID = str(uid())

        log.info("Job Run ID Created...")

        return runID

    ##### End #####

    def execute_job(self, fp, job_name):

        log.info("Creating Job Run ID...")

        self.jobRunID = self.build_run_id()

        if not UUID(self.jobRunID):
            raise ValueError("Invalid UUID")

        job_cfg_loader = JobConfigLoader(fp=fp)

        job_cfg_loader.job_cfg_loader_run()

        log.info(f"Job: {job_name} | ID: {self.jobRunID} | System: ELT | CREATED...")

        validator = Validator(loader=job_cfg_loader)

        validator.validator_run()

        log.info(
            f"Job Execution: {job_name} | ID: {self.jobRunID} | System: ELT | RUNNING...",
        )

        runner = Runner(loader=job_cfg_loader, jobRunID=self.jobRunID)

        runner.run()

        for key in job_cfg_loader.job_cfg["layer"]:
            try:
                runner.run_layers(key=key)

            except Exception as job_err:
                metadata = Metadata(loader=job_cfg_loader)

                metadata.get_metadata(key=key)

                metadata.build_job_metadata(
                    jobRunID=self.jobRunID,
                    jobName=job_name,
                    status="FAILED",
                    errMsg=job_err,
                    jobMetrics=None,
                )

                log.error(
                    f"Job Execution: {job_name} | ID: {self.jobRunID} | System: ELT | FAILED...",
                )

                log.error(f"Error = {job_err}")

                raise

            else:
                metadata = Metadata(loader=job_cfg_loader)

                metadata.get_metadata(key=key)

                metadata.build_job_metadata(
                    jobRunID=self.jobRunID,
                    jobName=job_name,
                    status="SUCCESS",
                    errMsg=None,
                    jobMetrics=runner.job_metrics,
                )

                log.success(
                    f"Job Execution: {job_name} | ID: {self.jobRunID} | System: ELT | jobType: {metadata.jobType} | jobMetrics: {runner.job_metrics} | SUCCESS...",
                )


if __name__ == "__main__":
    router = apir()

    @router.post("/elt_execute")
    async def execute(payload: dict):

        job_name = payload["job_name"]

        file_path = payload["path"]

        main = Main()

        main.execute_job(fp=file_path, job_name=job_name)

    if str(os.getenv(key="ENV")) == "DEV":
        main = Main()

        main.execute_job(
            fp="elt_system/configs/job/coingecko_sources/dev/market_price.json",
            job_name="dev_coingecko_market_price",
        )
