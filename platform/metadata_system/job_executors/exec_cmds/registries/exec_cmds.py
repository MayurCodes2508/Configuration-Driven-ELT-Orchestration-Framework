from loguru import logger as log
from metadata_system.job_executors.exec_cmds.db_exec_cmd import DBExecCommand
from metadata_system.job_executors.exec_cmds.dbt_exec_cmd import dbtExecCommand


class DBExec:
    @classmethod
    def run(cls, exec_cfg, metadata_cfg):

        return DBExecCommand(exec_cfg=exec_cfg, metadata_cfg=metadata_cfg)


class dbtExec:
    @classmethod
    def run(cls, exec_cfg, *args, **kwargs):

        return dbtExecCommand(exec_cfg=exec_cfg)


class ExecCmdType:
    registry = {"DBExecCmd": DBExec, "dbtExecCmd": dbtExec}

    @classmethod
    def get_exec_type(cls, exec_type, *args, **kwargs):

        class_template = cls.registry[exec_type]

        log.info(
            f"Successfully Mapped the Exec Type: {exec_type} with Exec Registry..."
        )

        exec_cmd = class_template.run(*args, **kwargs)

        return exec_cmd
