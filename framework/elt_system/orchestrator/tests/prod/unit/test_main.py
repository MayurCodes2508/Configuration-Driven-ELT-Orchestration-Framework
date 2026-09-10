from unittest.mock import Mock, patch

import pytest
from el_system.orchestrator.main import Main


@patch(target="el_system.orchestrator.main.tpe")
@patch(target="el_system.orchestrator.main.Orchestrator")
@patch(target="el_system.orchestrator.main.JobCatalog")
def test_main_local_success(mock_JobCatalog, mock_Orchestrator, mock_tpe):

    mock_JobCatalog.return_value.job_catalog_run.return_value = "PROD"

    mock_JobCatalog.return_value.jobs = [
        {
            "path": "el_system/configs/job/coingecko_sources/prod/market_price.json",
            "job_name": "prod_coingecko_market_price",
        },
    ]

    mock_executor = mock_tpe.return_value.__enter__.return_value

    mock_future = Mock()

    mock_future.result.return_value = '{"status": "SUCCESS"}'

    mock_executor.submit.return_value = mock_future

    main = Main()

    main.main()

    mock_JobCatalog.assert_called_once()

    mock_JobCatalog.return_value.job_catalog_run.assert_called_once()

    mock_Orchestrator.assert_called_once_with(env="PROD")

    mock_executor.submit.assert_called_once_with(
        mock_Orchestrator.return_value.run_concurrent_jobs_local,
        "el_system/configs/job/coingecko_sources/prod/market_price.json",
        "prod_coingecko_market_price",
    )

    assert mock_executor.submit.call_count == 1


@patch(target="el_system.orchestrator.main.log")
@patch(target="el_system.orchestrator.main.JobCatalog")
def test_main_local_load_job_catalog_failed(mock_JobCatalog, mock_log):

    mock_JobCatalog.return_value.job_catalog_run.side_effect = Exception(
        "System: el | Failed to Load Job Catalog, Aborting Job Executions",
    )

    main = Main()

    with pytest.raises(
        Exception,
        match="System: el | Failed to Load Job Catalog, Aborting Job Executions",
    ):
        main.main()

    mock_JobCatalog.assert_called_once()

    mock_JobCatalog.return_value.job_catalog_run.assert_called_once()

    mock_log.opt.return_value.critical.assert_called_once_with(
        "System: el | Failed to Load Job Catalog, Aborting Job Executions",
    )


@patch(target="el_system.orchestrator.main.log")
@patch(target="el_system.orchestrator.main.tpe")
@patch(target="el_system.orchestrator.main.Orchestrator")
@patch(target="el_system.orchestrator.main.JobCatalog")
def test_main_local_start_tpe_failed(
    mock_JobCatalog, mock_Orchestrator, mock_tpe, mock_log,
):

    mock_JobCatalog.return_value.job_catalog_run.return_value = "PROD"

    mock_JobCatalog.return_value.jobs = [
        {
            "path": "el_system/configs/job/coingecko_sources/prod/market_price.json",
            "job_name": "prod_coingecko_market_price",
        },
    ]

    mock_executor = mock_tpe.return_value.__enter__.return_value

    mock_executor.submit.side_effect = Exception(
        "System: el | Failed to Start the Thread Pool Executor, Aborting Job Executions",
    )

    main = Main()

    with pytest.raises(
        Exception,
        match="System: el | Failed to Start the Thread Pool Executor, Aborting Job Executions",
    ):
        main.main()

    mock_JobCatalog.assert_called_once()

    mock_JobCatalog.return_value.job_catalog_run.assert_called_once()

    mock_Orchestrator.assert_called_once_with(env="PROD")

    mock_executor.submit.assert_called_once_with(
        mock_Orchestrator.return_value.run_concurrent_jobs_local,
        "el_system/configs/job/coingecko_sources/prod/market_price.json",
        "prod_coingecko_market_price",
    )

    assert mock_executor.submit.call_count == 1

    mock_log.opt.return_value.critical.assert_called_once_with(
        "System: el | Failed to Start the Thread Pool Executor, Aborting Job Executions",
    )


@patch(target="el_system.orchestrator.main.JobCatalog")
@patch(target="el_system.orchestrator.main.Orchestrator")
@patch(target="el_system.orchestrator.main.tpe")
@patch(target="el_system.orchestrator.main.log")
def test_main_local_job_failed(mock_log, mock_tpe, mock_Orchestrator, mock_JobCatalog):

    mock_JobCatalog.return_value.job_catalog_run.return_value = "PROD"

    mock_JobCatalog.return_value.jobs = [
        {
            "path": "el_system/configs/job/coingecko_sources/prod/market_price.json",
            "job_name": "prod_coingecko_market_price",
        },
    ]

    mock_executor = mock_tpe.return_value.__enter__.return_value

    mock_future = Mock()

    mock_future.result.side_effect = Exception("System: el | One or More Jobs Failed")

    mock_executor.submit.return_value = mock_future

    main = Main()

    with pytest.raises(Exception, match="System: el | One or More Jobs Failed"):
        main.main()

    mock_JobCatalog.assert_called_once()

    mock_JobCatalog.return_value.job_catalog_run.assert_called_once()

    mock_Orchestrator.assert_called_once_with(env="PROD")

    mock_executor.submit.assert_called_once_with(
        mock_Orchestrator.return_value.run_concurrent_jobs_local,
        "el_system/configs/job/coingecko_sources/prod/market_price.json",
        "prod_coingecko_market_price",
    )

    assert mock_executor.submit.call_count == 1

    mock_log.opt.return_value.critical.assert_called_once_with(
        "System: el | One or More Jobs Failed",
    )


@patch(target="el_system.orchestrator.main.tpe")
@patch(target="el_system.orchestrator.main.Orchestrator")
@patch(target="el_system.orchestrator.main.JobCatalog")
def test_main_success(mock_JobCatalog, mock_Orchestrator, mock_tpe):

    mock_JobCatalog.return_value.job_catalog_run.return_value = "DEV"

    mock_JobCatalog.return_value.jobs = [
        {
            "path": "el_system/configs/job/coingecko_sources/prod/market_price.json",
            "job_name": "prod_coingecko_market_price",
        },
    ]

    mock_executor = mock_tpe.return_value.__enter__.return_value

    mock_future = Mock()

    mock_future.result.return_value = '{"status": "SUCCESS"}'

    mock_executor.submit.return_value = mock_future

    main = Main()

    main.main()

    mock_JobCatalog.assert_called_once()

    mock_JobCatalog.return_value.job_catalog_run.assert_called_once()

    mock_Orchestrator.assert_called_once_with(env="DEV")

    mock_executor.submit.assert_called_once_with(
        mock_Orchestrator.return_value.run_concurrent_jobs,
        "el_system/configs/job/coingecko_sources/prod/market_price.json",
        "prod_coingecko_market_price",
    )

    assert mock_executor.submit.call_count == 1


@patch(target="el_system.orchestrator.main.log")
@patch(target="el_system.orchestrator.main.JobCatalog")
def test_main_load_job_catalog_failed(mock_JobCatalog, mock_log):

    mock_JobCatalog.return_value.job_catalog_run.side_effect = Exception(
        "System: el | Failed to Load Job Catalog, Aborting Job Executions",
    )

    main = Main()

    with pytest.raises(
        Exception,
        match="System: el | Failed to Load Job Catalog, Aborting Job Executions",
    ):
        main.main()

    mock_JobCatalog.assert_called_once()

    mock_JobCatalog.return_value.job_catalog_run.assert_called_once()

    mock_log.opt.return_value.critical.assert_called_once_with(
        "System: el | Failed to Load Job Catalog, Aborting Job Executions",
    )


@patch(target="el_system.orchestrator.main.log")
@patch(target="el_system.orchestrator.main.tpe")
@patch(target="el_system.orchestrator.main.Orchestrator")
@patch(target="el_system.orchestrator.main.JobCatalog")
def test_main_start_tpe_failed(mock_JobCatalog, mock_Orchestrator, mock_tpe, mock_log):

    mock_JobCatalog.return_value.job_catalog_run.return_value = "DEV"

    mock_JobCatalog.return_value.jobs = [
        {
            "path": "el_system/configs/job/coingecko_sources/prod/market_price.json",
            "job_name": "prod_coingecko_market_price",
        },
    ]

    mock_executor = mock_tpe.return_value.__enter__.return_value

    mock_executor.submit.side_effect = Exception(
        "System: el | Failed to Start the Thread Pool Executor, Aborting Job Executions",
    )

    main = Main()

    with pytest.raises(
        Exception,
        match="System: el | Failed to Start the Thread Pool Executor, Aborting Job Executions",
    ):
        main.main()

    mock_JobCatalog.assert_called_once()

    mock_JobCatalog.return_value.job_catalog_run.assert_called_once()

    mock_Orchestrator.assert_called_once_with(env="DEV")

    mock_executor.submit.assert_called_once_with(
        mock_Orchestrator.return_value.run_concurrent_jobs,
        "el_system/configs/job/coingecko_sources/prod/market_price.json",
        "prod_coingecko_market_price",
    )

    assert mock_executor.submit.call_count == 1

    mock_log.opt.return_value.critical.assert_called_once_with(
        "System: el | Failed to Start the Thread Pool Executor, Aborting Job Executions",
    )


@patch(target="el_system.orchestrator.main.JobCatalog")
@patch(target="el_system.orchestrator.main.Orchestrator")
@patch(target="el_system.orchestrator.main.tpe")
@patch(target="el_system.orchestrator.main.log")
def test_main_job_failed(mock_log, mock_tpe, mock_Orchestrator, mock_JobCatalog):

    mock_JobCatalog.return_value.job_catalog_run.return_value = "DEV"

    mock_JobCatalog.return_value.jobs = [
        {
            "path": "el_system/configs/job/coingecko_sources/prod/market_price.json",
            "job_name": "prod_coingecko_market_price",
        },
    ]

    mock_executor = mock_tpe.return_value.__enter__.return_value

    mock_future = Mock()

    mock_future.result.side_effect = Exception("System: el | One or More Jobs Failed")

    mock_executor.submit.return_value = mock_future

    main = Main()

    with pytest.raises(Exception, match="System: el | One or More Jobs Failed"):
        main.main()

    mock_JobCatalog.assert_called_once()

    mock_JobCatalog.return_value.job_catalog_run.assert_called_once()

    mock_Orchestrator.assert_called_once_with(env="DEV")

    mock_executor.submit.assert_called_once_with(
        mock_Orchestrator.return_value.run_concurrent_jobs,
        "el_system/configs/job/coingecko_sources/prod/market_price.json",
        "prod_coingecko_market_price",
    )

    assert mock_executor.submit.call_count == 1

    mock_log.opt.return_value.critical.assert_called_once_with(
        "System: el | One or More Jobs Failed",
    )
