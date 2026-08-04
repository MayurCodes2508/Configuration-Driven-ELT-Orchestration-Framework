from loguru import logger as log

from el_system.job_executors.dests.gcs import GCS


class GCSDest:
    @classmethod
    def run(cls, dest_cfg, metadata_cfg, data, job_run_id):

        return GCS(
            dest_cfg=dest_cfg,
            metadata_cfg=metadata_cfg,
            data=data,
            job_run_id=job_run_id,
        )


class DestType:
    registry = {"GCS": GCSDest}

    @classmethod
    def get_dest_type(cls, dest_type, *args, **kwargs):

        class_template = cls.registry[dest_type]

        log.info(
            f"Successfully Mapped the Dest Type: {dest_type} with Dest Registry..."
        )

        dest = class_template.run(*args, **kwargs)

        return dest
