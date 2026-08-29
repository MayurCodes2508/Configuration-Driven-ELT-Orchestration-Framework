import os
from datetime import datetime as dt

from loguru import logger as log
from uuid6 import uuid7 as uid

import uvicorn as uv


class Orchestrator:
    def __init__(self):

        pass

    def run_pipeline(self, catalog, url):

        return

        pipelines = catalog["pipelines"]

        for pipeline in pipelines:
            pipeline_name = pipeline["name"]

            jobs = pipeline["jobs"]

            start_metadata_dump = {}

            try:
                pipeline_run_id = str(uid())

                pipeline_metadata = Pipeline_Metadata(
                    run_id=pipeline_run_id,
                    name=pipeline_name,
                    status="RUNNING",
                    error_message=None,
                    totaL_jobs=None,
                    total_failed_count=None,
                    total_successful_count=None,
                )

                start_metadata_dump = pipeline_metadata.create_pipeline_start_metadata()

            except Exception as preparation_error:
                error_message = str(preparation_error)

                start_metadata_dump = {
                    "pipeline_run_id": start_metadata_dump.get(
                        "pipeline_run_id", pipeline_run_id
                    )
                    or str(uid()),
                    "pipeline_run_name": start_metadata_dump.get(
                        "pipeline_run_name", pipeline_name
                    ),
                    "pipeline_run_status": "FAILED",
                    "pipeline_run_start_time": start_metadata_dump.get(
                        "pipeline_run_start_time"
                    )
                    or dt.now().isoformat(),
                    "pipeline_run_end_time": dt.now().isoformat(),
                    "pipeline_run_created_at": start_metadata_dump.get(
                        "pipeline_run_created_at"
                    )
                    or dt.now().isoformat(),
                    "pipeline_run_triggered_by": start_metadata_dump.get(
                        "pipeline_run_triggered_by"
                    )
                    or os.getenv("TRIGGERED_BY", "manual"),
                    "pipeline_run_error_message": error_message,
                    "pipeline_run_job_counts": {
                        "total_jobs": None,
                        "successful_jobs": None,
                        "failed_jobs": None,
                    },
                }

                pipeline_logger = Pipeline_Logger(url=url, metadata=start_metadata_dump)

                pipeline_logger.log_pipeline_run_start(
                    url=url, metadata=start_metadata_dump
                )

                log.error(
                    f"Pipeline: {start_metadata_dump['pipeline_run_name']} | Triggered By: {start_metadata_dump['pipeline_run_triggered_by']} | Run ID: {start_metadata_dump['pipeline_run_id']} | Status: {start_metadata_dump['pipeline_run_status']} | Started At: {start_metadata_dump['pipeline_run_start_time']} | Ended At: {start_metadata_dump['pipeline_run_end_time']}"
                )

                log.error(f"Details: {error_message}")

                return

            else:
                pipeline_logger = Pipeline_Logger(url=url, metadata=start_metadata_dump)

                pipeline_logger.log_pipeline_run_start()

                log.info(
                    f"Pipeline: {start_metadata_dump['pipeline_run_name']} | Triggered By: {start_metadata_dump['pipeline_run_triggered_by']} | Run ID: {start_metadata_dump['pipeline_run_id']} | Status: {start_metadata_dump['pipeline_run_status']} | Started At: {start_metadata_dump['pipeline_run_start_time']}..."
                )

            is_pipeline_failed = False

            total_failed_count = 0
            total_successful_count = 0

            runner = None

            operation = None

            for job in jobs:
                run_name = job["name"]

                log.info(f"Executing Run: {run_name}...")

                try:
                    runner = Runner()

                    operation = runner.execute_run(run_job_name=run_name)

                except Exception as exec_err:
                    is_pipeline_failed = True

                    error_message = str(exec_err)

                    log.error(f"Run: {run_name} | Execution Failed")

                    log.error(f"Defails: {error_message}")

                    continue

                job_metadatas = []

                metadata = None

                try:
                    job_metadata = Job_Metadata(
                        operation=operation,
                        run_job_name=run_name,
                        pipeline_run_id=start_metadata_dump["pipeline_run_id"],
                    )

                    job_metadatas = job_metadata.create_job_metadata()

                    for metadata in job_metadatas:
                        try:
                            job_logger = Job_Logger(url=url, metadata=metadata)

                            job_logger.log_job_run_metadata()

                            job_status = metadata["job_status"]

                            failed_count, successful_count = (
                                pipeline_metadata.collect_jobs_count(status=job_status)
                            )

                            total_failed_count += failed_count
                            total_successful_count += successful_count

                        except Exception as log_err:
                            error_message = str(log_err)

                            log.error(
                                f"Job: {metadata.get('job_name', 'UNKNOWN')} | Run ID: {metadata.get('job_run_id', 'UNKNOWN')} | Pipeline Run ID: {metadata.get('pipeline_run_id', pipeline_run_id)} | Run Name: {run_name} | Metadata Logging Failed"
                            )

                            log.error(f"Details: {error_message}")

                            continue

                        else:
                            log.info(
                                f"Job: {metadata['job_name']} | Run ID: {metadata['job_run_id']} | Pipeline Run ID: {metadata['pipeline_run_id']} | System: {metadata['system']} | Job Type: {metadata['job_type']} | Sub JobType: {metadata['sub_jobtype']} | Status: {metadata['job_status']} | Started At: {metadata['start_time']} | Ended At: {metadata['end_time']}..."
                            )

                except Exception as meta_err:
                    is_pipeline_failed = True

                    error_message = str(meta_err)

                    log.error(
                        f"Job: {metadata.get('job_name', 'UNKNOWN')} | Run ID: {metadata.get('job_run_id', 'UNKNOWN')} | Pipeline Run ID: {metadata.get('pipeline_run_id', pipeline_run_id)} | Run Name: {run_name} | Metadata Retrieval Failed"
                    )

                    log.error(f"Details: {error_message}")

                    continue

            if is_pipeline_failed:
                pipeline_metadata = Pipeline_Metadata(
                    run_id=pipeline_run_id,
                    name=pipeline_name,
                    status="FAILED",
                    error_message=(
                        f"{run_name} \n"
                        f"{metadata.get('job_name', 'UNKNOWN')} \n"
                        f"{error_message}"
                    ),
                    totaL_jobs=len(job_metadatas),
                    total_failed_count=total_failed_count,
                    total_successful_count=total_successful_count,
                )

                end_metadata_dump = pipeline_metadata.create_pipeline_end_metadata()

                pipeline_logger = Pipeline_Logger(url=url, metadata=end_metadata_dump)

                pipeline_logger.log_pipeline_run_end()

                log.error(
                    f"Pipeline: {start_metadata_dump['pipeline_run_name']} | Triggered By: {start_metadata_dump['pipeline_run_triggered_by']} | Run ID: {start_metadata_dump['pipeline_run_id']} | Status: {end_metadata_dump['pipeline_run_status']} | Started At: {start_metadata_dump['pipeline_run_start_time']} | Ended At: {end_metadata_dump['pipeline_run_end_time']} | Total Jobs: {end_metadata_dump['pipeline_run_job_counts']['total_jobs']} | Successful Jobs: {end_metadata_dump['pipeline_run_job_counts']['successful_jobs']} | Failed Jobs: {end_metadata_dump['pipeline_run_job_counts']['failed_jobs']}"
                )

                log.error(f"Details: {end_metadata_dump['pipeline_run_error_message']}")

            else:
                pipeline_metadata = Pipeline_Metadata(
                    run_id=pipeline_run_id,
                    name=pipeline_name,
                    status="SUCCESS",
                    error_message=None,
                    totaL_jobs=len(job_metadatas),
                    total_failed_count=total_failed_count,
                    total_successful_count=total_successful_count,
                )

                end_metadata_dump = pipeline_metadata.create_pipeline_end_metadata()

                pipeline_logger = Pipeline_Logger(url=url, metadata=end_metadata_dump)

                pipeline_logger.log_pipeline_run_end()

                log.info(
                    f"Pipeline: {start_metadata_dump['pipeline_run_name']} | Triggered By: {start_metadata_dump['pipeline_run_triggered_by']} | Run ID: {start_metadata_dump['pipeline_run_id']} | Status: {end_metadata_dump['pipeline_run_status']} | Started At: {start_metadata_dump['pipeline_run_start_time']} | Ended At: {end_metadata_dump['pipeline_run_end_time']} | Total Jobs: {end_metadata_dump['pipeline_run_job_counts']['total_jobs']} | Successful Jobs: {end_metadata_dump['pipeline_run_job_counts']['successful_jobs']} | Failed Jobs: {end_metadata_dump['pipeline_run_job_counts']['failed_jobs']}..."
                )


class Main:
    def __init__(self):
        pass

    def main(self):

        log.info("Hey!")



if __name__ == "__main__":

    pass