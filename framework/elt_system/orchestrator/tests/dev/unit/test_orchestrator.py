import pytest
from unittest.mock import patch, MagicMock, call

from elt_system.orchestrator.main import Orchestrator


@pytest.mark.parametrize(
    "mock_path, mock_job_name",
    [
        (
            "elt_system.configs.job.coingecko_sources.dev.market_price.json",
            "dev_coingecko_market_price",
        )
    ],
)
@patch(target="elt_system.orchestrator.main.JobsClient")
@patch(target="elt_system.orchestrator.main.ExecutionsClient")
@patch(target="elt_system.orchestrator.main.lv2")
@patch(
    target="elt_system.orchestrator.main.Orchestrator.get_run_job_name_and_base_path"
)
@patch(target="elt_system.orchestrator.main.RunJobRequest")
@patch(target="elt_system.orchestrator.main.log")
@patch(target="elt_system.orchestrator.main.time")
def test_run_concurrent_jobs_success(
    mock_time,
    mock_log,
    mock_RunJobRequest,
    mock_get_run_job_name_and_base_path,
    mock_lv2,
    mock_ExecutionsClient,
    mock_JobsClient,
    mock_path,
    mock_job_name,
):

    mock_get_run_job_name_and_base_path.return_value = (
        "dev-elt-system-run",
        "projects/instant-medium-491107-t6/locations/asia-south1/jobs",
    )

    mock_logging_client = MagicMock()

    mock_lv2.return_value = mock_logging_client

    mock_request = MagicMock()

    mock_RunJobRequest.return_value = mock_request

    mock_operation = MagicMock()

    mock_JobsClient.return_value.run_job.return_value = mock_operation

    mock_execution_name = "some/execution/some-exec-name"

    mock_operation.metadata.name = mock_execution_name

    mock_execution_running = MagicMock()

    mock_execution_running.completion_time = None

    mock_execution_completed = MagicMock()

    mock_execution_completed.completion_time = "any-completion-time"

    mock_ExecutionsClient.return_value.get_execution.side_effect = [
        mock_execution_running,
        mock_execution_completed,
    ]

    mock_logging_client.return_value.list_entries.side_effect = []

    orchestrator = Orchestrator(env="LOCAL")

    orchestrator.run_concurrent_jobs(path=mock_path, job_name=mock_job_name)

    mock_JobsClient.assert_called_once()

    mock_ExecutionsClient.assert_called_once()

    mock_lv2.Client.assert_called_once_with(project="instant-medium-491107-t6")

    mock_get_run_job_name_and_base_path.assert_called_once_with(env="LOCAL")

    mock_RunJobRequest.assert_called_once_with(
        name=(
            "projects/instant-medium-491107-t6/locations/asia-south1/jobs/dev-elt-system-run"
        ),
        overrides=mock_RunJobRequest.Overrides(
            container_overrides=[
                mock_RunJobRequest.Overrides.ContainerOverride(
                    args=[
                        "elt_system.orchestrator.executor",
                        "--job_name",
                        str(object=mock_job_name),
                        "--file_path",
                        str(object=mock_path),
                    ]
                )
            ]
        ),
    )

    mock_JobsClient.return_value.run_job.assert_called_once_with(request=mock_request)

    mock_log.info.assert_any_call(f"Job Execution Name: {mock_execution_name}...")

    mock_ExecutionsClient.return_value.get_execution.assert_has_calls(
        [call(name=mock_execution_name), call(name=mock_execution_name)]
    )

    assert mock_ExecutionsClient.return_value.get_execution.call_count == 2

    mock_log.info.assert_any_call("Successfully Got Final Job Execution...")

    mock_time.sleep.assert_called_with(3)

    mock_job_filter = """

        resource.labels.job_name="dev-elt-system-run"
        resource.labels.location="asia-south1"
        labels."run.googleapis.com/execution_name"="some-execution-name"
        textPayload:"METADATA_DUMP"

    """

    mock_logging_client.return_value.list_entries.assert_called_once_with(
        filter_=mock_job_filter
    )
