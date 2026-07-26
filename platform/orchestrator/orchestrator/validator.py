from pathlib import Path

import jsonschema_rs
from jsonschema.exceptions import SchemaError, ValidationError
from loguru import logger as log


class Validator:
    def __init__(self, pipeline_loader):

        self.pipeline_catalog = pipeline_loader.pipeline_catalog

        self.schema_cfg = pipeline_loader.schema_cfg

        self.schema_path = pipeline_loader.schema_path

        log.info("Values for Validation Loading Completed...")

        log.info("Obj: validator | Instance Initialized Successfully...")

    def validate_catalog(self):

        try:
            base_uri = Path(self.schema_path).resolve().as_uri()

            validate_cfg = jsonschema_rs.validator_for(
                schema=self.schema_cfg, base_uri=base_uri
            )

            validate_cfg.validate(instance=self.pipeline_catalog)

            log.info("Catalog Validation Against the Given Schema Completed...")

        except ValidationError as e:
            log.error(
                f"Validation Error: {self.pipeline_catalog} | Provide a Valid Pipeline Catalog | Details: {e}"
            )

            raise

        except SchemaError as e:
            log.error(
                f"Schema Error: {self.schema_cfg} | Provide a Valid Schema | Details: {e}"
            )

            raise

        except Exception:
            log.exception(
                "Unknown Error Occured While Validating Pipeline Catalog Againt Given Schema"
            )

            raise

    def validator_run(self):

        self.validate_catalog()
