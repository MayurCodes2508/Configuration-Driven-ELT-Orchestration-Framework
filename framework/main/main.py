import os
import sys
from datetime import datetime as dt
from datetime import timezone as tz

import psycopg2 as psg2
from fastapi import APIRouter as apir
from loguru import logger as log
from psycopg2.extras import Json
from uuid6 import uuid7 as uid

log.remove()

log.add(
    sink=sys.stdout,
    filter=lambda record: (
        record["level"].name
        in {"INFO", "SUCCESS", "ERROR", "WARNING", "DEBUG", "TRACE"}
    ),
)

log.add(sink=sys.stderr, filter=lambda record: record["level"].name == "CRITICAL")


def pipeline_end_logger(self, payload: dict) -> None:

    pass


def job_logger(self, payload: dict) -> None:

    with psg2.connect(payload["NeonDBURLSecret"]) as conn, conn.cursor() as cursor:
        insert_query = """
                INSERT INTO job_runs(
                    run_id,
                    pipeline_run_id,
                    job_name,
                    system,
                    job_type,
                    sub_jobtype,
                    status,
                    start_time,
                    end_time,
                    created_at,
                    error_message,
                    job_metrics,
                    extra_metadata
                )

                VALUES(
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """

        query_values: tuple = (
            payload["job_start_metadata_result"]["job_run_id"],
            payload["job_start_metadata_result"]["pipeline_run_id"],
            payload["job_start_metadata_result"]["job_name"],
            payload["job_start_metadata_result"]["system"],
            payload["job_start_metadata_result"]["job_type"],
            payload["job_start_metadata_result"]["sub_jobtype"],
            payload["job_start_metadata_result"]["job_status"],
            payload["job_start_metadata_result"]["job_start_time"],
            payload["job_start_metadata_result"]["job_end_time"],
            payload["job_start_metadata_result"]["job_created_at"],
            payload["job_start_metadata_result"]["job_error_message"],
            Json(payload["pipeline_start_metadata_result"]["job_metrics"]),
            Json(payload["pipeline_start_metadata_result"]["extra_metadata"]),
        )

        cursor.execute(insert_query, query_values)

    log.info("Successfully logged job start metadata into DB")


def pipeline_end_metadata(self, payload: dict) -> dict:

    pipeline_end_metadata_payload: dict = {
        "pipeline_run_id": payload["pipeline_start_metadata_result"]["pipeline_run_id"],
        "pipeline_name": payload["pipeline_start_metadata_result"]["pipeline_name"],
        "pipeline_status": payload["pipeline_status"],
        "pipeline_end_time": dt.now(tz=tz.utc).isoformat(sep="|"),
        "pipeline_error_message": payload["pipeline_error_message"],
        "job_counts": {
            "total_jobs": payload["job_counts"]["total_jobs"],
            "failed_jobs": payload["job_counts"]["failed_jobs"],
            "successful_jobs": payload["job_counts"]["successful_jobs"],
        },
    }

    log.info("Successfully created pipeline end metadata")

    return pipeline_end_metadata_payload


router = apir()


@router.post("/execute_jobs")
async def execute_jobs(payload: dict) -> None:

    pass


@router.post("/pipeline_start_metadata")
async def pipeline_start_metadata(payload: dict) -> dict:

    pipeline_start_metadata_payload: dict = {
        "pipeline_run_id": str(uid()),
        "pipeline_name": payload["pipeline_name"],
        "pipeline_status": "RUNNING",
        "pipeline_created_at": dt.now(tz=tz.utc),
        "pipeline_start_time": dt.now(tz=tz.utc),
        "pipeline_end_time": None,
        "triggered_by": str(os.getenv(key="triggeredBy")) or "manual",
        "pipeline_error_message": None,
        "job_counts": {
            "total_jobs": None,
            "failed_jobs": None,
            "successful_jobs": None,
        },
    }

    log.info("Successfully created pipeline start metadata")

    with psg2.connect(payload["neonDBURLSecret"]) as conn, conn.cursor() as cursor:
        insert_query = """
                INSERT INTO public.pipeline_runs(
                    run_id,
                    pipeline_name,
                    status,
                    start_time,
                    end_time,
                    created_at,
                    triggered_by,
                    error_message,
                    job_counts
                )

                VALUES(
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """

        query_values: tuple = (
            pipeline_start_metadata_payload["pipeline_run_id"],
            pipeline_start_metadata_payload["pipeline_name"],
            pipeline_start_metadata_payload["pipeline_status"],
            pipeline_start_metadata_payload["pipeline_start_time"],
            pipeline_start_metadata_payload["pipeline_end_time"],
            pipeline_start_metadata_payload["pipeline_created_at"],
            pipeline_start_metadata_payload["triggered_by"],
            pipeline_start_metadata_payload["pipeline_error_message"],
            Json(pipeline_start_metadata_payload["job_counts"]),
        )

        cursor.execute(insert_query, query_values)

    log.info("Successfully logged pipeline start metadata into DB")

    return pipeline_start_metadata_payload
