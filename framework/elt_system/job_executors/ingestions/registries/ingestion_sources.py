from loguru import logger as log

from elt_system.job_executors.ingestions.api import Api


class API:
    root_url_registry = {"coingecko": "https://api.coingecko.com/api/v3"}

    @classmethod
    def run(cls, ingestion_cfg, metadata_cfg, *args, **kwargs):

        source = metadata_cfg["source"]

        root_url = cls.root_url_registry[source]

        return Api(ingestion_cfg=ingestion_cfg, url=root_url)


class ingestionType:
    registry = {"API": API}

    @classmethod
    def get_ingestion_type(cls, ingestion_type, *args, **kwargs):

        class_template = cls.registry[ingestion_type]

        log.info(
            f"Successfully Mapped the Ingestion Type: {ingestion_type} with Ingestion Registry..."
        )

        ingestion_type = class_template.run(*args, **kwargs)

        return ingestion_type
