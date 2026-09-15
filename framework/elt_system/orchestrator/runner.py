from uuid import UUID

from loguru import logger as log

from elt_system.job_executors.ingestions.registries.ingestion_sources import (
    ingestionType,
)
from elt_system.job_executors.storages.registries.storage_destinations import (
    storageType,
)


class Runner:
    def __init__(self, metadata_cfg: dict, jobRunID: UUID) -> None:

        self.metadata_cfg: dict = metadata_cfg
        self.jobRunID: UUID = jobRunID

        log.info("Obj: runner | Instance Initialized Successfully...")

        log.info("Runner Loading Completed...")

    def run(self, layer: str, job_cfg: dict):

        if layer == "ingestion":
            self.data, self.job_metrics = self.run_ingestion_job(ingestion_cfg=job_cfg)

        elif layer == "storage":
            self.job_metrics = self.run_storage_job(storage_cfg=job_cfg, data=self.data)

    def run_ingestion_job(self, ingestion_cfg: dict):

        ingestion_type: ingestionType = ingestionType()

        ingestion = ingestion_type.get_ingestion_type(
            ingestion_type=ingestion_cfg["ingestion_type"],
            ingestion_cfg=ingestion_cfg,
            metadata_cfg=self.metadata_cfg,
        )

        data, job_metrics = ingestion.run()

        return data, job_metrics

    def run_storage_job(self, storage_cfg: dict, data):

        storage_type = storageType()

        storage = storage_type.get_storage_type(
            storage_type=storage_cfg["storage_type"],
            storage_cfg=storage_cfg,
            metadata_cfg=self.metadata_cfg,
            data=data,
            jobRunID=self.jobRunID,
        )

        job_metrics: dict = storage.run()

        return job_metrics
