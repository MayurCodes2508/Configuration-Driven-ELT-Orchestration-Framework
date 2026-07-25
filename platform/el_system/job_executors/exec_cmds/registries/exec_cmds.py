from loguru import logger as log

from el_system.job_executors.exec_cmds.api_exec import ApiExecCommand


class APIExec:
    root_url_registry = {"coingecko": "https://api.coingecko.com/api/v3"}

    @classmethod
    def run(cls, exec_cfg, metadata_cfg, *args, **kwargs):

        source = metadata_cfg["source"]

        root_url = cls.root_url_registry[source]

        return ApiExecCommand(exec_cfg=exec_cfg, url=root_url)


class ExecCmdType:
    registry = {"ApiExecCmd": APIExec}

    @classmethod
    def get_exec_type(cls, exec_type, *args, **kwargs):

        class_template = cls.registry[exec_type]

        log.info(
            f"Successfully Mapped the Exec Type: {exec_type} with Exec Registry..."
        )

        exec_cmd = class_template.run(*args, **kwargs)

        return exec_cmd
