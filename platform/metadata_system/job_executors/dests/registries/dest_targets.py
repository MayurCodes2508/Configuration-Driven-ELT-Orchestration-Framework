from loguru import logger as log

from metadata_system.job_executors.dests.bq_dest import BQ


class BQDest:
    @classmethod
    def run(cls, dest_cfg, data, metadata_cfg):

        return BQ(dest_cfg=dest_cfg, data=data)


class DestType:
    registry = {"BQ": BQDest}

    @classmethod
    def get_dest_type(cls, dest_type, *args, **kwargs):

        class_template = cls.registry[dest_type]

        log.info(
            f"Successfully Mapped the Dest Type: {dest_type} with Dest Registry..."
        )

        dest = class_template.run(*args, **kwargs)

        return dest
