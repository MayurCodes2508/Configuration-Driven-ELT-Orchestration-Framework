import json
import os
from pathlib import Path

from loguru import logger as log

from elt_system.exceptions.exceptions import EXCEPTION_DESCRIPTIONS


class JobCatalog:
    def __init__(self):

        self.env = os.getenv(key="ENV", default="LOCAL")

        if self.env == "PROD":
            self.file_path = (
                Path(__file__).parent.parent
                / "configs"
                / "catalog"
                / "prod"
                / "config.json"
            )

        elif self.env in {"LOCAL", "DEV"}:
            self.file_path = (
                Path(__file__).parent.parent
                / "configs"
                / "catalog"
                / "dev"
                / "config.json"
            )

        else:
            raise ValueError(f"Unknown Env: {self.env} | Provide a Valid Env")

        log.info("Obj: job_catalog | Instance Initialized Successfully...")

        log.info("JSON Job Catalog Path Loading Completed...")

    def load_job_catalog(self):

        try:
            with open(file=self.file_path) as f:
                self.job_catalog = json.load(fp=f)

                self.jobs = self.job_catalog["jobs"]

                log.info("Job Catalog Loading Completed...")

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}",
            )

            raise

    def job_catalog_run(self):

        self.load_job_catalog()

        return self.env


class JobConfigLoader:
    def __init__(self, fp):

        self.file_path = fp

        self.schema_path = Path(__file__).parent.parent / "schemas" / "root_schema.json"

        log.info("Obj: job_cfg_loader | Instance Initialized Successfully...")

        log.info("JSON Job & Schema Cfg Paths Loading Completed...")

    def load_job_cfg(self):

        try:
            with open(file=self.file_path) as f:
                self.job_cfg = json.load(fp=f)

                log.info("Job Cfg Loading Completed...")

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}",
            )

            raise

    def load_schema_cfg(self):

        try:
            with open(file=self.schema_path) as f:
                self.schema_cfg = json.load(fp=f)

                log.info("Schema Cfg Loading Completed...")

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}",
            )

            raise

    def job_cfg_loader_run(self):

        self.load_job_cfg()

        self.load_schema_cfg()
