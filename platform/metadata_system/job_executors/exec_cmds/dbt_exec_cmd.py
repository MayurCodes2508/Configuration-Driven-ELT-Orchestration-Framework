from loguru import logger as log
from subprocess import Popen as sp
import subprocess
from pathlib import Path
import shlex
import json


class dbtExecCommand:
    def __init__(self, exec_cfg):

        self.exec_cfg = exec_cfg

        self._cmd = exec_cfg["command"]

        self.cmd = shlex.split(s=self._cmd)

        log.info("Obj: dbtexeccmd | Instance Initialization Completed...")

        log.info("Exec Metadata Loading Completed...")

    def run_dbt(self):

        processes = []

        process = sp(
            [
                "dbt",
                *self.cmd,
                "--fail-fast",
                "--project-dir",
                str(Path(__file__).parent.parent.parent / "dbt/"),
                "--profiles-dir",
                str(Path(__file__).parent.parent.parent / "dbt/"),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        processes.append(process)

        for process in processes:
            for line in process.stdout:
                log.info(line.rstrip())

            process.wait()

            if process.returncode != 0:
                for line in process.stderr:
                    log.error(line.rstrip())

        log.info("Execution of dbt Completed...")

        artifact_path = (
            Path(__file__).parent.parent.parent / "dbt/target/run_results.json"
        )

        with open(file=artifact_path, mode="+r") as f:
            data = json.load(fp=f)

        nodes = {}

        for result in data["results"]:
            node = result["unique_id"]

            nodes[node] = {
                "status": result["status"],
                "execution_time": result["execution_time"],
                "message": result["message"],
                "failures": result["failures"],
                "rows_affected": result["adapter_response"].get("rows_affected"),
                "bytes_billed": result["adapter_response"].get("bytes_billed"),
                "job_id": result["adapter_response"].get("job_id"),
                "slot_ms": result["adapter_response"].get("slot_ms"),
            }

        return nodes

    def run(self):

        job_metrics = self.run_dbt()

        data = None

        return data, job_metrics
