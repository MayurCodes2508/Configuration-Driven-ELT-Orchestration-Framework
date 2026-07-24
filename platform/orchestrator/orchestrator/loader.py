import os
from pathlib import Path
from loguru import logger as log
import json
from json import JSONDecodeError


class PipelineLoader:
    def __init__(self):

        env = os.getenv(key="ENV", default="LOCAL")

        if env == "PROD":
            self.file_path = (
                Path(__file__).parent.parent
                / "configs"
                / "catalog"
                / "prod"
                / "config.json"
            )

        elif env in {"DEV", "LOCAL"}:
            self.file_path = (
                Path(__file__).parent.parent
                / "configs"
                / "catalog"
                / "dev"
                / "config.json"
            )

        else:
            raise ValueError(f"Unknown Env: {env} | Provide a Valid Env")

        self.schema_path = (
            Path(__file__).parent.parent / "schemas" / "pipeline_schema.json"
        )

        log.info("JSON Pipeline Catalog and Schema Cfg Paths Loading Completed...")

        log.info("Obj: pipeline_loader | Instance Initialized Successfully...")

    def load_pipeline_catalog(self):

        try:
            with open(file=self.file_path, mode="r") as f:
                self.pipeline_catalog = json.load(fp=f)

                log.info("Pipeline Catalog Loading Completed...")

        except FileNotFoundError:
            log.error(
                f"File Not Found Error: {self.file_path} | Provide a Valid JSON Pipeline Catalog File Path"
            )

            raise

        except JSONDecodeError as e:
            log.error(
                f"JSON Parsing/Decoding Error: {self.file_path} | Provide Valid JSON Format | Details: {e}"
            )

            raise

        except UnicodeDecodeError:
            log.error(f"Unicode Decoding Error: {self.file_path} | Expected UTF-8")

            raise

        except Exception:
            log.exception(
                f"Unknown Error Occured While Loading Pipeline Catalog: {self.file_path}"
            )

            raise

    def load_schema_cfg(self):

        try:
            with open(file=self.schema_path, mode="r") as f:
                self.schema_cfg = json.load(fp=f)

                log.info("Schema Cfg Loading Completed...")

        except FileNotFoundError:
            log.error(
                f"File Not Found Error: {self.schema_path} | Provide a Valid JSON Schema Cfg File Path"
            )

            raise

        except JSONDecodeError as e:
            log.error(
                f"JSON Parsing/Decoding Error: {self.schema_path} | Provide Valid JSON Format | Details: {e}"
            )

            raise

        except UnicodeDecodeError:
            log.error(f"Unicode Decoding Error: {self.schema_path} | Expected UTF-8")

            raise

        except Exception:
            log.exception(
                f"Unknown Error Occured While Loading Schema Cfg: {self.schema_path}"
            )

            raise

    def pipeline_loader_run(self):

        self.load_pipeline_catalog()

        self.load_schema_cfg()

    def load_db_creds(self):

        db_url = os.getenv("DB_URL")

        if not db_url:
            raise ValueError(
                f"Invalid or Missing db_url: {db_url} | Provide a valid DB URL"
            )

        self.db_url = db_url
