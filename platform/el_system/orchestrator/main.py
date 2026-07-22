from loguru import logger as log
from uuid6 import uuid7 as uid
import subprocess
from subprocess import Popen as sp
import json
import sys
from concurrent.futures import ThreadPoolExecutor as tpe
from google.cloud.run_v2 import JobsClient, RunJobRequest
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

            client = JobsClient()

            run_job_name = "dev-el-system-run"

            if self.env == "PROD":

                run_job_name = "prod-el-system-run"

            request = RunJobRequest(
                name=run_job_name,
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

            operation = client.run_job(request=request)

        except Exception:

            log.error("Error Occured: While Calling Run Jobs")

            return

    def run_concurrent_jobs_local(self, path, job_name):

        processes = []

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
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        processes.append(process)

        for process in processes:
            for line in process.stdout:
                log.info(line.rstrip())

            process.wait()

            if process.returncode != 0:
                for line in process.stderr:

                    log.error(line.rstrip())

                return


if __name__ == "__main__":
    job_catalog_loader = None

    try:
        job_catalog_loader = JobCatalog()

        env = job_catalog_loader.job_catalog_run()

    except Exception as load_err:
        log.critical("System: el | Failed to Load Job Catalog, Aborting Job Executions")

        log.error(f"Details: {str(object=load_err)}")

        raise

    try:

        orchestrator = Orchestrator(env=env)

        log.info("All Job Executions Started...")

        with tpe(max_workers=5) as executor:
            for job in job_catalog_loader.jobs:

                if env == "LOCAL":
                    future = executor.submit(
                        orchestrator.run_concurrent_jobs_local,
                        job["path"],
                        job["job_name"],
                    )

                elif env in {"DEV", "PROD"}:
                    future = executor.submit(
                        orchestrator.run_concurrent_jobs, job["path"], job["job_name"]
                    )

        log.info("All Job Executions Completed...")

    except Exception as strt_err:
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

            log.info(f"METADATA_DUMP: {json.dumps(obj=dump)}")

        log.critical(
            "System: el | Failed to Start the Thread Pool Executor, Aborting Job Executions"
        )

        log.error(f"Details: {str(object=strt_err)}")

        raise
