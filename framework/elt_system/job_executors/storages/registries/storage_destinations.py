from loguru import logger as log

from elt_system.job_executors.storages.gcs import Gcs


class GCS:
    @classmethod
    def run(cls, storage_cfg, metadata_cfg, data, jobRunID):

        return Gcs(
            storage_cfg=storage_cfg,
            metadata_cfg=metadata_cfg,
            data=data,
            jobRunID=jobRunID,
        )


class storageType:
    registry = {"GCS": GCS}

    @classmethod
    def get_storage_type(cls, storage_type, *args, **kwargs):

        class_template = cls.registry[storage_type]

        log.info(
            f"Successfully Mapped the Storage Type: {storage_type} with Storage Type Registry...",
        )

        storage_type = class_template.run(*args, **kwargs)

        return storage_type
