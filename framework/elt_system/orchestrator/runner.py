from loguru import logger as log

from elt_system.job_executors.ingestions.registries.ingestion_sources import (
    ingestionType,
)
from elt_system.job_executors.storages.registries.storage_destinations import (
    storageType,
)


class Runner:
    def __init__(self, loader, jobRunID):

        self.job_cfg = loader.job_cfg

        self.metadata_cfg = self.job_cfg["metadata"]

        self.layer_cfg = self.job_cfg["layer"]

        self.jobRunID = jobRunID

        log.info("Obj: runner | Instance Initialized Successfully...")

        log.info("Runner Loading Completed...")

    def run(self):

        self.ingestion_cfg = None
        self.storage_cfg = None

        for key, val in self.layer_cfg.items():
            if not self.ingestion_cfg and key == "ingestion":
                self.ingestion_cfg = val

            if not self.storage_cfg and key == "storage":
                self.storage_cfg = val

    def run_layers(self, key):

        if key == "ingestion":
            self.run_ingestion_job()

        elif key == "storage":
            self.run_storage_job()

    def run_ingestion_job(self):

        ingestion_type = ingestionType()

        ingestion = ingestion_type.get_ingestion_type(
            ingestion_type=self.ingestion_cfg["ingestion_type"],
            ingestion_cfg=self.ingestion_cfg,
            metadata_cfg=self.metadata_cfg,
        )

        self.data, self.job_metrics = ingestion.run()

    def run_storage_job(self):

        storage_type = storageType()

        storage = storage_type.get_storage_type(
            storage_type=self.storage_cfg["storage_type"],
            storage_cfg=self.storage_cfg,
            metadata_cfg=self.metadata_cfg,
            data=self.data,
            jobRunID=self.jobRunID,
        )

        self.job_metrics = storage.run()
