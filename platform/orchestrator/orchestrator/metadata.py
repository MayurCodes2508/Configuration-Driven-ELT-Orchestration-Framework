import json
import os
import time
from ast import literal_eval as le
from datetime import datetime as dt

from google.api_core.exceptions import (GoogleAPIError, InvalidArgument,
                                        NotFound)
from google.cloud import logging_v2 as lv2
from google.cloud.run_v2 import ExecutionsClient
from loguru import logger as log


class Pipeline_Metadata:
    def __init__(
        self,
        run_id,
        name,
        status,
        error_message,
        totaL_jobs,
        total_failed_count,
        total_successful_count,
    ):

        self.pipeline_run_id = run_id

        self.pipeline_run_name = name

        self.status = status

        self.error_message = error_message

        self.total_jobs = totaL_jobs

        self.total_failed_count = total_failed_count

        self.total_successful_count = total_successful_count

        log.info("Pipeline Metadata Loading Completed...")

        log.info("Obj: pipeline metadata | Instance Initialized Successfully...")

    def create_pipeline_start_metadata(self):

        try:
            pipeline_start_metadata_dump = {
                "pipeline_run_id": self.pipeline_run_id,
                "pipeline_run_name": self.pipeline_run_name,
                "pipeline_run_status": self.status,
                "pipeline_run_created_at": dt.now().isoformat(),
                "pipeline_run_end_time": None,
                "pipeline_run_start_time": dt.now().isoformat(),
                "pipeline_run_triggered_by": os.getenv("TRIGGERED_BY", "manual"),
                "pipeline_run_error_message": self.error_message,
                "pipeline_run_job_counts": {
                    "total_jobs": self.total_jobs,
                    "successful_jobs": self.total_successful_count,
                    "failed_jobs": self.total_failed_count,
                },
            }

            log.info("Pipeline Start Metadata Creation Completed...")

            return pipeline_start_metadata_dump

        except Exception:
            log.exception(
                "Unexpected Error Occured While Creating Pipeline End Metadata"
            )

    def create_pipeline_end_metadata(self):

        try:
            pipeline_end_metadata_dump = {
                "pipeline_run_id": self.pipeline_run_id,
                "pipeline_run_status": self.status,
                "pipeline_run_error_message": self.error_message,
                "pipeline_run_end_time": dt.now().isoformat(),
                "pipeline_run_job_counts": {
                    "total_jobs": self.total_jobs,
                    "successful_jobs": self.total_successful_count,
                    "failed_jobs": self.total_failed_count,
                },
            }

            log.info("Pipeline End Metadata Creation Completed...")

            return pipeline_end_metadata_dump

        except Exception:
            log.exception(
                "Unexpected Error Occured While Creating Pipeline End Metadata"
            )

    def collect_jobs_count(self, status):

        try:
            if status == "FAILED":
                failed_count = 1
                successful_count = 0

            elif status == "SUCCESS":
                successful_count = 1
                failed_count = 0

            return failed_count, successful_count

        except Exception:
            log.error("Unexpected Error Occured While Collecting Jobs Count")


class Job_Metadata:
    def __init__(self, operation, run_job_name, pipeline_run_id):

        self.operation = operation

        self.run_job_name = run_job_name

        self.pipeline_run_id = pipeline_run_id

        log.info("Job Metadata Loading Completed...")

        log.info("Obj: job metadata | Instance Initialized Successfully...")

    def create_job_metadata(self):

        executions_client = ExecutionsClient()

        try:
            execution_name = self.operation.metadata.name

            log.info(f"Job Execution Name: {execution_name}...")

            while True:
                execution = executions_client.get_execution(name=execution_name)

                if execution.completion_time:
                    log.info("Successfully Got Final Job Execution...")

                    break

                time.sleep(1)

            start_time = execution.start_time

            end_time = execution.completion_time

            created_at = execution.create_time

            cloud_run_job_id = execution.uid

            cloud_run_job_name = execution.job

            log_uri = execution.log_uri

            max_retries = execution.template.max_retries

            timeout = execution.template.timeout.seconds

            is_retry = bool(execution.retried_count)

            logging_client = lv2.Client(project="instant-medium-491107-t6")

            exec_name = execution_name.rsplit("/", 1)[-1]

            job_filter = f'''

                resource.labels.job_name="{self.run_job_name}"
                resource.labels.location="asia-south1"
                labels."run.googleapis.com/execution_name"="{exec_name}"
                textPayload:"METADATA_DUMP"

                '''

            all_metadata_dump = None

            while True:
                entries = logging_client.list_entries(filter_=job_filter)

                for entry in entries:
                    log_text = entry.payload

                    all_metadata_dump = log_text.rsplit("ALL_METADATA_DUMPS: ", 1)[-1]

                    break

                if all_metadata_dump is not None:
                    break

                time.sleep(1)

            all_metadata_dump = le(all_metadata_dump)

        except GoogleAPIError:
            log.exception("API Error Occured, Affecting Job Metadata")

        except NotFound:
            log.exception("Execution Not Found Error Occured, Affecting Job Metadata")

        except InvalidArgument:
            log.exception("Invalid Argument Error Occured, Affecting Job Metadata")

        except Exception:
            log.exception("Unexpected Error Occured, Affecting Job Metadata")

        job_metadatas = []

        try:
            for metadata_dump in all_metadata_dump:
                metadata = json.loads(metadata_dump)

                log.info(metadata)

                dump = {
                    "job_run_id": metadata["job_run_id"],
                    "pipeline_run_id": self.pipeline_run_id,
                    "job_name": metadata["job_name"],
                    "system": metadata["system"],
                    "job_type": metadata["job_type"],
                    "sub_jobtype": metadata["sub_jobtype"],
                    "job_status": metadata["status"],
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "created_at": created_at.isoformat(),
                    "error_message": metadata["error_message"],
                    "job_metrics": metadata["job_metrics"],
                    "extra_metadata": {
                        "cloud_run_job_id": cloud_run_job_id,
                        "cloud_run_job_name": cloud_run_job_name,
                        "log_uri": log_uri,
                        "max_retries": max_retries,
                        "timeout": timeout,
                        "is_retry": is_retry,
                    },
                }

                job_metadatas.append(dump)

            log.info("Job Metadata Created")

            return job_metadatas

        except Exception:
            log.exception("Unexpected Error Occured, Affecting Job Metadata")
