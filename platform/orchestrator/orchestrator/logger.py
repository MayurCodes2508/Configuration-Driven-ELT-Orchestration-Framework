import psycopg2
from loguru import logger as log
from psycopg2.errors import DatabaseError, InterfaceError, OperationalError
from psycopg2.extras import Json


class Pipeline_Logger:
    def __init__(self, url, metadata):

        self.url = url

        self.metadata = metadata

        log.info("Pipeline Metadata & DB URL Loading Completed...")

        log.info("Obj: pipeline logger | Instance Initialized Successfully...")

    def log_pipeline_run_start(self):

        try:
            with psycopg2.connect(self.url) as conn:
                with conn.cursor() as cursor:
                    insert_query = """

                    INSERT INTO pipeline_runs(
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

                    query_values = (
                        self.metadata["pipeline_run_id"],
                        self.metadata["pipeline_run_name"],
                        self.metadata["pipeline_run_status"],
                        self.metadata["pipeline_run_start_time"],
                        self.metadata["pipeline_run_end_time"],
                        self.metadata["pipeline_run_created_at"],
                        self.metadata["pipeline_run_triggered_by"],
                        self.metadata["pipeline_run_error_message"],
                        Json(self.metadata["pipeline_run_job_counts"]),
                    )

                    cursor.execute(insert_query, query_values)

                    log.info("Successfully Inserted Pipeline Run...")

        except (OperationalError, InterfaceError):
            log.exception("Network/Connection Error Occured")

        except DatabaseError:
            log.exception("SQL Syntax/DB Constraint Error Occured")

        except Exception:
            log.exception("Unexpected Error Occured")

    def log_pipeline_run_end(self):

        try:
            with psycopg2.connect(self.url) as conn:
                with conn.cursor() as cursor:
                    update_query = """

                    UPDATE  pipeline_runs

                    SET status = %s,
                        error_message = %s,
                        end_time = %s,
                        job_counts = %s

                    WHERE run_id = %s

                """

                    query_values = (
                        self.metadata["pipeline_run_status"],
                        self.metadata["pipeline_run_error_message"],
                        self.metadata["pipeline_run_end_time"],
                        Json(self.metadata["pipeline_run_job_counts"]),
                        self.metadata["pipeline_run_id"],
                    )

                    cursor.execute(update_query, query_values)

        except (OperationalError, InterfaceError):
            log.exception("Network/Connection Error Occured")

        except DatabaseError:
            log.exception("SQL Syntax/DB Constraint Error Occured")

        except Exception:
            log.exception("Unexpected Error Occured")


class Job_Logger:
    def __init__(self, url, metadata):

        self.url = url

        self.metadata = metadata

    def log_job_run_metadata(self):

        try:
            with psycopg2.connect(self.url) as conn:
                with conn.cursor() as cursor:
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
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )

                """

                    query_values = (
                        self.metadata["job_run_id"],
                        self.metadata["pipeline_run_id"],
                        self.metadata["job_name"],
                        self.metadata["system"],
                        self.metadata["job_type"],
                        self.metadata["sub_jobtype"],
                        self.metadata["job_status"],
                        self.metadata["start_time"],
                        self.metadata["end_time"],
                        self.metadata["created_at"],
                        self.metadata["error_message"],
                        Json(self.metadata["job_metrics"]),
                        Json(self.metadata["extra_metadata"]),
                    )

                    cursor.execute(insert_query, query_values)

        except (OperationalError, InterfaceError):
            log.exception("Network/Connection Error Occured")

        except DatabaseError:
            log.exception("SQL Syntax/DB Constraint Error Occured")

        except Exception:
            log.exception("Unexpected Error Occured")
