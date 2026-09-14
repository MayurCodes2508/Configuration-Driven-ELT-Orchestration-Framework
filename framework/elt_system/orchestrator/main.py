import argparse as arg
import os
import sys
from datetime import datetime as dt
from datetime import timezone as tz
from uuid import UUID

import psycopg2 as pg2
from loguru import logger as log
from psycopg2.extras import Json, register_uuid
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
    def __init__(self) -> None:

        pass

    ##### Helper Functions :3 #####

    def build_run_id(self) -> UUID:

        runID: UUID = UUID(str(uid()))

        log.info("Job Run ID Created...")

        return runID

    def write_to_db(self, query: str, values: tuple) -> None:

        register_uuid()

        with pg2.connect(str(os.environ["neonDBURL"])) as conn, conn.cursor() as csr:
            csr.execute(query, values)

        log.info("Successfully logged job metadata into DB")

    ##### End #####

    def execute_job(self, fp: str, job_name: str) -> None:

        pipelineRunID: UUID = UUID(os.environ["pipelineRunID"])

        log.info("Creating Job Run ID...")

        jobRunID: UUID = self.build_run_id()

        log.info(
            f"Job Execution: {job_name} | runID: {jobRunID} | PipelineRunID: {pipelineRunID} | RUNNING...",
        )

        metadata: Metadata = Metadata(
            jobRunID=jobRunID,
            pipelineRunID=pipelineRunID,
            jobName=job_name,
        )

        job_cfg_loader: JobConfigLoader = JobConfigLoader(fp=fp)

        job_cfg_loader.job_cfg_loader_run()

        validator: Validator = Validator(loader=job_cfg_loader)

        validator.validator_run()

        runner: Runner = Runner(
            metadata_cfg=job_cfg_loader.job_cfg["metadata"],
            jobRunID=jobRunID,
        )

        for key, val in job_cfg_loader.job_cfg["layer"].items():
            running_metadata_dump = metadata.build_job_metadata(
                jobType=key,
                status="RUNNING",
                created_at=dt.now(tz=tz.utc),
                start_time=dt.now(tz=tz.utc),
            )

            insert_running_query: str = """
                INSERT INTO public.job_runs(
                    run_id,
                    pipeline_run_id,
                    job_name,
                    job_type,
                    status,
                    created_at,
                    start_time,
                    end_time,
                    error_message,
                    job_metrics
                )

                VALUES(
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s
                )
            """

            running_query_values: tuple = (
                running_metadata_dump["run_id"],
                running_metadata_dump["pipeline_run_id"],
                running_metadata_dump["job_name"],
                running_metadata_dump["job_type"],
                running_metadata_dump["status"],
                running_metadata_dump["created_at"],
                running_metadata_dump["start_time"],
                running_metadata_dump["end_time"],
                running_metadata_dump["error_message"],
                running_metadata_dump["job_metrics"],
            )

            self.write_to_db(query=insert_running_query, values=running_query_values)

            try:
                runner.run(layer=key, job_cfg=val)

            except Exception as job_err:
                failed_metadata_dump: dict = metadata.build_job_metadata(
                    jobType=key,
                    status="FAILED",
                    end_time=dt.now(tz=tz.utc),
                    errMsg=job_err,
                )

                update_failed_query: str = """
                    UPDATE public.job_runs
                    SET status=%s,
                        end_time=%s,
                        error_message=%s
                    WHERE run_id=%s
                        AND pipeline_run_id=%s
                        AND job_name=%s
                        AND job_type=%s
                """

                failed_query_values: tuple = (
                    failed_metadata_dump["status"],
                    failed_metadata_dump["end_time"],
                    failed_metadata_dump["error_message"],
                    failed_metadata_dump["run_id"],
                    failed_metadata_dump["pipeline_run_id"],
                    failed_metadata_dump["job_name"],
                    failed_metadata_dump["job_type"],
                )

                self.write_to_db(query=update_failed_query, values=failed_query_values)

                log.error(
                    f"Job Execution: {job_name} | runID: {jobRunID} | PipelineRunID: {pipelineRunID} | FAILED...",
                )

                log.error(f"Error = {job_err}")

                raise

            else:
                successful_metadata_dump: dict = metadata.build_job_metadata(
                    jobType=key,
                    status="SUCCESS",
                    end_time=dt.now(tz=tz.utc),
                    jobMetrics=runner.job_metrics,
                )

                update_successful_query: str = """
                    UPDATE public.job_runs
                    SET status=%s,
                        end_time=%s,
                        job_metrics=%s
                    WHERE run_id=%s
                        AND pipeline_run_id=%s
                        AND job_name=%s
                        AND job_type=%s
                """

                successful_query_values: tuple = (
                    successful_metadata_dump["status"],
                    successful_metadata_dump["end_time"],
                    Json(successful_metadata_dump["job_metrics"]),
                    successful_metadata_dump["run_id"],
                    successful_metadata_dump["pipeline_run_id"],
                    successful_metadata_dump["job_name"],
                    successful_metadata_dump["job_type"],
                )

                self.write_to_db(
                    query=update_successful_query,
                    values=successful_query_values,
                )

                log.success(
                    f"Job Execution: {job_name} | runID: {jobRunID} | PipelineRunID: {pipelineRunID} | jobType: {key} | jobMetrics: {runner.job_metrics} | SUCCESS...",
                )


if __name__ == "__main__":
    parser = arg.ArgumentParser(
        description="Job Name and Job Config File Path for Job Executions",
    )

    parser.add_argument(
        "--job_name",
        help="--job_name jobName",
        required=True,
    )

    parser.add_argument(
        "--file_path",
        help="--file_path filePath",
        required=True,
    )

    args = parser.parse_args()

    main: Main = Main()

    main.execute_job(
        fp=args.file_path,
        job_name=args.job_name,
    )
