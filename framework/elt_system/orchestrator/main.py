import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor as tpe
from subprocess import CalledProcessError as sperr
from subprocess import run as sp

from google.cloud import logging_v2 as lv2
from google.cloud.run_v2 import ExecutionsClient, JobsClient, RunJobRequest
from loguru import logger as log
from uuid6 import uuid7 as uid

from elt_system.exceptions.exceptions import EXCEPTION_DESCRIPTIONS
from elt_system.orchestrator.loader import JobCatalog

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

        def get_run_job_name_and_base_path(env):

            run_job_name = "dev-elt-system-run"

            if env == "PROD":
                run_job_name = "prod-elt-system-run"

            base_path = "projects/instant-medium-491107-t6/locations/asia-south1/jobs"

            return run_job_name, base_path

        try:
            jobs_client = JobsClient()

            executions_client = ExecutionsClient()

            logging_client = lv2.Client(project="instant-medium-491107-t6")

            run_job_name, base_path = get_run_job_name_and_base_path(env=self.env)

            request = RunJobRequest(
                name=(f"{base_path}/{run_job_name}"),
                overrides=RunJobRequest.Overrides(
                    container_overrides=[
                        RunJobRequest.Overrides.ContainerOverride(
                            args=[
                                "elt_system.orchestrator.executor",
                                "--job_name",
                                str(object=job_name),
                                "--file_path",
                                str(object=path),
                            ]
                        )
                    ]
                ),
            )

            operation = jobs_client.run_job(request=request)

            execution_name = operation.metadata.name

            log.info(f"Job Execution Name: {execution_name}...")

            while True:
                execution = executions_client.get_execution(name=execution_name)

                if execution.completion_time:
                    log.info("Successfully Got Final Job Execution...")

                    break

                time.sleep(3)

            exec_name = execution_name.rsplit("/", 1)[-1]

            job_filter = f'''

                resource.labels.job_name="{run_job_name}"
                resource.labels.location="asia-south1"
                labels."run.googleapis.com/execution_name"="{exec_name}"
                textPayload:"METADATA_DUMP"

            '''

            dump = None

            for sec in range(100):
                entries = logging_client.list_entries(filter_=job_filter)

                for entry in entries:
                    txt_log = entry.payload

                    dump = txt_log.rsplit("METADATA_DUMP: ", 1)[-1]

                    break

                if dump is not None:
                    break

                time.sleep(3)

            else:
                raise TimeoutError("TImeout Hit | Couldnt Fetch Metadata Dump")

            return dump

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}"
            )

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
                    "framework:latest",
                    "elt_system.orchestrator.executor",
                    "--job_name",
                    str(object=job_name),
                    "--file_path",
                    str(object=path),
                ],
                capture_output=True,
                check=True,
                text=True,
            )

            output = process.stdout

            log.info(output)

            dump = output.rsplit("METADATA_DUMP: ", 1)[-1]

            decoder = json.JSONDecoder()

            obj, _end = decoder.raw_decode(dump)

            return json.dumps(obj=obj)

        except sperr as err:
            log.exception("Error Occured: While Executing Job")

            log.error(f"{err.stderr}")

            raise


class Main:
    def __init__(self):

        pass

    def main(self):

        def getenv(job_catalog_loader):

            env = job_catalog_loader.job_catalog_run()

            if not env:
                raise ValueError(f"Invalid or Missing Env: {env}")

            return env

        try:
            job_catalog_loader = JobCatalog()

            env = getenv(job_catalog_loader=job_catalog_loader)

            log.info(f"Successfully Loaded the Env: {env}...")

        except Exception:
            log.opt(exception=True).critical(
                "System: el | Failed to Load Job Catalog, Aborting Job Executions"
            )

            raise

        try:
            orchestrator = Orchestrator(env=env)

            log.info("All Job Executions Started...")

            futures = []

            with tpe(max_workers=5) as executor:
                for job in job_catalog_loader.jobs:
                    if env == "LOCAL":
                        futures.append(
                            executor.submit(
                                orchestrator.run_concurrent_jobs_local,
                                job["path"],
                                job["job_name"],
                            )
                        )

                    elif env in {"DEV", "PROD"}:
                        futures.append(
                            executor.submit(
                                orchestrator.run_concurrent_jobs,
                                job["path"],
                                job["job_name"],
                            )
                        )

            log.info("All Job Executions Completed...")

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

        results = []

        try:
            for future in futures:
                results.append(future.result())

            log.info(f"ALL_METADATA_DUMPS: {results}")

        except Exception as job_err:
            for job in job_catalog_loader.jobs:
                dump = {
                    "job_run_id": str(object=uid()),
                    "job_name": job.get("job_name"),
                    "system": "el",
                    "job_type": None,
                    "sub_jobtype": None,
                    "status": "FAILED",
                    "error_message": str(object=job_err),
                    "job_metrics": None,
                }

                results.append(json.dumps(obj=dump))

            log.opt(exception=True).critical("System: el | One or More Jobs Failed")

            log.info(f"ALL_METADATA_DUMPS: {results}")

            if job_err:
                raise


if __name__ == "__main__":
    main = Main()

    main.main()
