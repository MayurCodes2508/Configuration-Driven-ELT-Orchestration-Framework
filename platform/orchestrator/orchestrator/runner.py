from google.api_core.exceptions import GoogleAPIError, InvalidArgument, NotFound
from google.cloud.run_v2 import JobsClient
from loguru import logger as log


class Runner:
    def __init__(self):

        log.info("Obj: runner | Instance Initialized Successfully...")

    def execute_run(self, run_job_name):

        try:
            jobs_client = JobsClient()

            base_path = "projects/instant-medium-491107-t6/locations/asia-south1/jobs"

            operation = jobs_client.run_job(name=(f"{base_path}/{run_job_name}"))

            log.info(f"Execution of Job: {run_job_name} | Started...")

            return operation

        except GoogleAPIError:
            log.exception("API Error Occured")

        except NotFound:
            log.exception(f"Job Not Found Error Occured: {run_job_name}")

        except InvalidArgument:
            log.exception(f"Invalid Argument Error Occured: {operation}")

        except Exception:
            log.exception("Error Occured While Executing Job")
