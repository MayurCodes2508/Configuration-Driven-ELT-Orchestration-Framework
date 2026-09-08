from loguru import logger as log

from metadata_system.exceptions.exceptions import EXCEPTION_DESCRIPTIONS
from metadata_system.job_executors.dests.registries.dest_targets import DestType
from metadata_system.job_executors.exec_cmds.registries.exec_cmds import ExecCmdType


class Runner:
    def __init__(self, loader):

        self.job_cfg = loader.job_cfg

        self.metadata_cfg = self.job_cfg["metadata"]

        log.info("Obj: runner | Instance Initialized Successfully...")

        log.info("Runner Loading Completed...")

    def run_exec_cmd(self):

        try:
            self.exec_cfg = self.job_cfg["exec"]

            self.exec_type = self.exec_cfg["exec_type"]

            exec_cmd = ExecCmdType.get_exec_type(
                exec_type=self.exec_type,
                exec_cfg=self.exec_cfg,
                metadata_cfg=self.metadata_cfg,
            )

            self.data, self.job_metrics = exec_cmd.run()

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}",
            )

            raise

    def run_dest_target(self):

        try:
            self.dest_cfg = self.job_cfg.get("dest", {})

            self.dest_type = self.dest_cfg.get("dest_type", None)

            if not self.dest_type:
                log.info("Dest Not Provided, Skipping...")

                return

            dest = DestType.get_dest_type(
                dest_type=self.dest_type,
                dest_cfg=self.dest_cfg,
                metadata_cfg=self.metadata_cfg,
                data=self.data,
            )

            dest.run()

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}",
            )

            raise

    def runner_run(self):

        self.run_exec_cmd()

        self.run_dest_target()
