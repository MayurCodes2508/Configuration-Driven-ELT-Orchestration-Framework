from el_system.orchestrator.main import Orchestrator

from unittest.mock import patch





def test_run_concurrent_jobs():

    orchestrator = Orchestrator(env="LOCAL")

    orchestrator.run_concurrent_jobs_local(
        path=""
    )