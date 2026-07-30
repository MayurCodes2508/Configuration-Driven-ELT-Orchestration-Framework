import argparse as arg
import json
import sys

from loguru import logger as log
from uuid6 import uuid7 as uid
from uuid import UUID

from el_system.orchestrator.loader import JobConfigLoader
from el_system.orchestrator.metadata import Metadata
from el_system.orchestrator.runner import Runner
from el_system.orchestrator.validator import Validator

log.remove()

log.add(
    sink=sys.stdout,
    filter=lambda record: (
        record["level"].name
        in {"INFO", "SUCCESS", "ERROR", "WARNING", "DEBUG", "TRACE"}
    ),
)

log.add(sink=sys.stderr, filter=lambda record: record["level"].name == "CRITICAL")


class Executor:
    def __init__(self):

        pass

    def execute_job(self, fp, job_name):

        log.info("Creating Job Run ID...")

        def build_run_id():

            run_id = str(uid())

            log.info("Job Run ID Created...")

            return run_id

        try:
            self.job_run_id = build_run_id()

            if not UUID(self.job_run_id):
                raise ValueError("Invalid UUID")

            job_cfg_loader = JobConfigLoader(fp=fp)

            job_cfg_loader.job_cfg_loader_run()

        except Exception as load_err:
            dump = {
                "job_run_id": self.job_run_id,
                "job_name": job_name,
                "system": "el",
                "job_type": None,
                "sub_jobtype": None,
                "status": "FAILED",
                "error_message": str(object=load_err),
                "job_metrics": None,
            }

            log.info(f"METADATA_DUMP: {json.dumps(obj=dump)}")

            log.opt(exception=True).error(
                f"Job: {job_name} | ID: {self.job_run_id} | System: el | Job Cfg Loading Failed"
            )

            raise

        log.info(f"Job: {job_name} | ID: {self.job_run_id} | System: el | CREATED...")

        try:
            validator = Validator(loader=job_cfg_loader)

            validator.validator_run()

        except Exception as valid_err:
            dump = {
                "job_run_id": self.job_run_id,
                "job_name": job_name,
                "system": "el",
                "job_type": None,
                "sub_jobtype": None,
                "status": "FAILED",
                "error_message": str(object=valid_err),
                "job_metrics": None,
            }

            log.info(f"METADATA_DUMP: {json.dumps(obj=dump)}")

            log.opt(exception=True).error(
                f"Job Execution: {job_name} | ID: {self.job_run_id} | System: el | Job Cfg Validation Failed"
            )

            raise

        log.info(
            f"Job Execution: {job_name} | ID: {self.job_run_id} | System: el | RUNNING..."
        )

        try:
            runner = Runner(loader=job_cfg_loader)

            runner.runner_run()

        except Exception as exec_err:
            metadata = Metadata(loader=job_cfg_loader)

            job_metadata_dump = metadata.build_job_metadata(
                job_run_id=self.job_run_id,
                job_name=job_name,
                status="FAILED",
                error_message=str(object=exec_err),
                job_metrics=getattr(runner, "job_metrics", None) if runner else None,
            )

            log.info(f"METADATA_DUMP: {json.dumps(obj=job_metadata_dump)}")

            log.opt(exception=True).error(
                f"Job Execution: {job_name} | ID: {self.job_run_id} | System: el | Job Type: {job_metadata_dump['job_type']} | Sub JobType: {job_metadata_dump['sub_jobtype']} | Status: FAILED"
            )

            raise

        else:
            metadata = Metadata(loader=job_cfg_loader)

            metadata.get_metadata()

            job_metadata_dump = metadata.build_job_metadata(
                job_run_id=self.job_run_id,
                job_name=job_name,
                status="SUCCESS",
                error_message=None,
                job_metrics=getattr(runner, "job_metrics", None) if runner else None,
            )

            log.info(f"METADATA_DUMP: {json.dumps(obj=job_metadata_dump)}")

            log.success(
                f"Job Execution: {job_name} | ID: {self.job_run_id} | System: el | Job Type: {job_metadata_dump['job_type']} | Sub JobType: {job_metadata_dump['sub_jobtype']} | Status: SUCCESS"
            )


if __name__ == "__main__":
    parser = arg.ArgumentParser()

    parser.add_argument("--job_name", type=str, help="Name of the Job", required=True)

    parser.add_argument(
        "--file_path", type=str, help="Path to the JSON Job Cfg File", required=True
    )

    args = parser.parse_args()

    executor = Executor()

    executor.execute_job(fp=args.file_path, job_name=args.job_name)
