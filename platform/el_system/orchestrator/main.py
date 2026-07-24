from loguru import logger as log
from concurrent.futures import ThreadPoolExecutor as tpe
from subprocess import run as sp, CalledProcessError as sperr
from uuid6 import uuid7 as uid
import json
import sys
import time
from google.cloud.run_v2 import JobsClient, RunJobRequest, ExecutionsClient
from google.cloud import logging_v2 as lv2
from el_system.orchestrator.loader import JobCatalog


log.remove()

log.add(
    sink=sys.stdout,
    filter=lambda record: (
        record["level"].name
        in {"INFO", "SUCCESS", "ERROR", "WARNING", "DEBUG", "TRACE"}
    ),
)

log.add(sink=sys.stderr, filter=lambda record: record["level"].name == "CRITICAL")


class Orchestrator:
    def __init__(self, env):

        self.env = env

    def run_concurrent_jobs(self, path, job_name):

        try:

            jobs_client = JobsClient()

            executions_client = ExecutionsClient()

            logging_client = lv2.Client(project="instant-medium-491107-t6")

            run_job_name = "dev-el-system-run"

            base_path = "projects/instant-medium-491107-t6/locations/asia-south1/jobs"

            if self.env == "PROD":

                run_job_name = "prod-el-system-run"

            request = RunJobRequest(
                name=(f"{base_path}/{run_job_name}"),
                overrides=RunJobRequest.Overrides(
                    container_overrides=[
                        RunJobRequest.Overrides.ContainerOverride(
                            args=[
                                "el_system.orchestrator.executor",
                                "--job_name", str(object=job_name),
                                "--file_path", str(object=path)
                            ]
                        )
                    ]
                )
            )

            operation = jobs_client.run_job(request=request)

            execution_name = operation.metadata.name

            log.info(f"Job Execution Name: {execution_name}...")

            while True:

                execution = executions_client.get_execution(name=execution_name)

                if execution.completion_time:

                    log.info("Successfully Got Final Job Execution...")

                    break

                time.sleep(1)

            exec_name = execution_name.rsplit("/", 1)[-1]

            job_filter = f'''

                resource.labels.job_name="{run_job_name}"
                resource.labels.location="asia-south1"
                labels."run.googleapis.com/execution_name"="{exec_name}"
                textPayload:"METADATA_DUMP"

            '''

            metadata = None

            while True:

                entries = logging_client.list_entries(filter_=job_filter)

                for entry in entries:

                    txt_log = entry.payload

                    dump = txt_log.rsplit("METADATA_DUMP: ", 1)[-1]

                    break

                if metadata is not None:

                    break
                
                time.sleep(1)

            return dump

        except Exception:

            log.exception("Error Occured: While Calling Run Jobs")

            raise

    def run_concurrent_jobs_local(self, path, job_name):

        try:

            process = sp(
                [
                    "docker",
                    "run",
                    "--rm",
                    "-e",
                    "COINGECKO_API_KEY",
                    "platform-job:latest",
                    "el_system.orchestrator.executor",
                    "--job_name",
                    str(object=job_name),
                    "--file_path",
                    str(object=path)
                ],
                capture_output=True,
                check=True,
                text=True,
            )

            output = process.stdout
            
            dump = output.rsplit("METADATA_DUMP: ", 1)[-1]

            decoder = json.JSONDecoder()

            obj, end = decoder.raw_decode(dump)

            return json.dumps(obj=obj)
        
        except sperr as err:

            log.exception("Error Occured: While Executing Job")

            log.error(f"{err.stderr}")

            raise


if __name__ == "__main__":

    try:
        job_catalog_loader = JobCatalog()

        env = job_catalog_loader.job_catalog_run()

    except Exception:
        log.opt(exception=True).critical("System: el | Failed to Load Job Catalog, Aborting Job Executions")

        raise

    try:

        orchestrator = Orchestrator(env=env)

        log.info("All Job Executions Started...")

        futures = []

        with tpe(max_workers=5) as executor:
            for job in job_catalog_loader.jobs:

                if env == "LOCAL":
                    futures.append(executor.submit(
                        orchestrator.run_concurrent_jobs_local,
                        job["path"],
                        job["job_name"],
                        )
                    )

                elif env in {"DEV", "PROD"}:
                    futures.append(executor.submit(
                        orchestrator.run_concurrent_jobs, job["path"], job["job_name"]
                        )
                    )

        results = []

        for future in futures:

            results.append(future.result())

        log.info("All Job Executions Completed...")

        log.info(f"ALL_METADATA_DUMPS: {results}")

    except Exception as strt_err:

        results = []

        for job in job_catalog_loader.jobs:
            dump = {
                "job_run_id": str(object=uid()),
                "job_name": job.get("job_name"),
                "system": "el",
                "job_type": None,
                "sub_jobtype": None,
                "status": "FAILED",
                "error_message": str(object=strt_err),
                "job_metrics": None,
            }

            results.append(json.dumps(obj=dump))

        log.opt(exception=True).critical(
            "System: el | Failed to Start the Thread Pool Executor, Aborting Job Executions"
        )

        log.info(f"ALL_METADATA_DUMPS: {results}")

        raise
