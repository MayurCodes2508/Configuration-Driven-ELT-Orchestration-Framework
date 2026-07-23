from loguru import logger as log
import jsonschema_rs
from jsonschema.exceptions import ValidationError, SchemaError
from pathlib import Path


class Validator:
    def __init__(self, loader):

        self.job_cfg = loader.job_cfg

        self.schema_cfg = loader.schema_cfg

        self.schema_path = loader.schema_path

        log.info("Obj: validator | Instance Initialized Successfully...")

        log.info("Job & Schema Cfg Loading Completed...")

    def validate_job_cfg(self):

        try:
            base_uri = Path(self.schema_path).resolve().as_uri()

            validate_cfg = jsonschema_rs.validator_for(
                schema=self.schema_cfg, base_uri=base_uri
            )

            validate_cfg.validate(instance=self.job_cfg)

            log.info("Job Validation Against the Given Schema Completed...")

        except ValidationError:
            log.error(
                f"Validation Error: {self.job_cfg} | Provide a Valid Job Cfg"
            )

            raise

        except SchemaError:
            log.error(
                f"Schema Error: {self.schema_cfg} | Provide a Valid Schema"
            )

            raise

        except Exception:
            log.error(
                "Unknown Error Occured While Validating Job Cfg Againt Given Schema"
            )

            raise

    def validator_run(self):

        self.validate_job_cfg()
