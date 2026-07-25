from loguru import logger as log

from pathlib import Path

import jsonschema_rs

from el_system.exceptions.exceptions import EXCEPTION_DESCRIPTIONS


class Validator:
    def __init__(self, loader):

        self.job_cfg = loader.job_cfg

        self.schema_cfg = loader.schema_cfg

        self.schema_path = loader.schema_path

        log.info("Obj: validator | Instance Initialized Successfully...")

        log.info("Validation Requirements Loading Completed...")

    def validate_job_cfg(self):

        try:
            base_uri = Path(self.schema_path).resolve().as_uri()

            validate_cfg = jsonschema_rs.validator_for(
                schema=self.schema_cfg, base_uri=base_uri
            )

            validate_cfg.validate(instance=self.job_cfg)

            log.info("Job Validation Against the Given Schema Completed...")

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}"
            )

            raise

    def validator_run(self):

        self.validate_job_cfg()
