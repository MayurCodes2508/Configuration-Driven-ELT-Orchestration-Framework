import os
import sys
from datetime import datetime as dt
from datetime import timezone as tz
from uuid import UUID

import psycopg2 as pg2
from fastapi import APIRouter as apir
from loguru import logger as log
from psycopg2.extras import register_uuid
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


##### Helper Functions :3 #####

def build_run_id() -> UUID:

    runID: UUID = UUID(str(uid()))

    log.info("Pipeline Run ID Created...")

    return runID

def write_to_db(query: str, values: tuple, auth: str) -> None:

    register_uuid()

    with pg2.connect(str(auth)) as conn, conn.cursor() as csr:
        csr.execute(query, values)

    log.info("Successfully logged pipeline metadata into DB")

##### End #####


router = apir()

@router.post("/pipeline_start_metadata")
async def pipeline_start_metadata(payload: dict) -> dict:

    runID = build_run_id()

    pipeline_start_metadata_payload: dict = {
        "run_id": runID,
        "pipeline_name": str(payload["pipeline_name"]),
        "status": "RUNNING",
        "created_at": dt.now(tz=tz.utc),
        "start_time": dt.now(tz=tz.utc),
        "end_time": None,
        "triggered_by": str(os.environ["triggeredBy"]) or "manual",
        "error_message": None,
    }

    log.info("Successfully created pipeline start metadata")

    insert_query: str = """
            INSERT INTO public.pipeline_runs(
                run_id,
                pipeline_name,
                status,
                created_at,
                start_time,
                end_time,
                triggered_by,
                error_message
            )

            VALUES(
                %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

    insert_query_values: tuple = (
        pipeline_start_metadata_payload["run_id"],
        pipeline_start_metadata_payload["pipeline_name"],
        pipeline_start_metadata_payload["status"],
        pipeline_start_metadata_payload["created_at"],
        pipeline_start_metadata_payload["start_time"],
        pipeline_start_metadata_payload["end_time"],
        pipeline_start_metadata_payload["triggered_by"],
        pipeline_start_metadata_payload["error_message"],
    )

    write_to_db(query=insert_query, values=insert_query_values, auth=payload["neonDBURL"])

    return pipeline_start_metadata_payload


@router.post("/pipeline_end_metadata")
async def pipeline_end_metadata(payload: dict) -> None:

    pipeline_end_metadata_payload: dict = {
        "run_id": payload["pipeline_start_metadata_payload"]["run_id"],
        "pipeline_name": payload["pipeline_start_metadata_payload"]["pipeline_name"],
        "status": payload["status"],
        "end_time": dt.now(tz=tz.utc),
        "error_message": payload.get("error_message") or None,
    }

    log.info("Successfully created pipeline start metadata")

    update_query: str = """
            UPDATE public.pipeline_runs
            SET status=%s,
                end_time=%s,
                error_message=%s
            WHERE run_id=%s
                AND pipeline_name=%s
        """

    update_query_values: tuple = (
        pipeline_end_metadata_payload["status"],
        pipeline_end_metadata_payload["end_time"],
        pipeline_end_metadata_payload["error_message"],
        pipeline_end_metadata_payload["run_id"],
        pipeline_end_metadata_payload["pipeline_name"],
    )

    write_to_db(query=update_query, values=update_query_values, auth=payload["neonDBURL"])
