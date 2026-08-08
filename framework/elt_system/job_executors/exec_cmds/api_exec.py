import requests
from loguru import logger as log

from elt_system.exceptions.exceptions import EXCEPTION_DESCRIPTIONS
from elt_system.job_executors.auth.auth import Auth


class ApiExecCommand:
    def __init__(self, exec_cfg, url):

        self.exec_cfg = exec_cfg

        self.root_url = url

        pagination_config = exec_cfg["pagination"]
        self.pagination_strategy = pagination_config["strategy"]
        self.page_param = pagination_config.get("page_param", "page")

        page_size_config = exec_cfg["page_size"]
        self.page_size_param = page_size_config["param"]
        self.page_size_value = page_size_config["value"]

        query_params_config = exec_cfg["query_params"]
        self.vs_currency = query_params_config["vs_currency"]
        self.custom_query_params = {
            k: v for k, v in query_params_config.items() if k != "vs_currency"
        }

        auth_cfg = exec_cfg.get("auth")

        auth_type = auth_cfg.get("auth_type")

        if not auth_cfg and auth_type:
            log.info("Auth not Provided, Skipping...")

            log.info("Obj: apiexeccmd | Instance Initialization Completed...")

            log.info("Exec Metadata Loading Completed...")

            return

        self.auth_cfg = exec_cfg["auth"]

        self.auth_type = self.auth_cfg["auth_type"]

        self.location = self.auth_cfg["location"]

        self.name = self.auth_cfg["name"]

        self.secret = Auth.get_auth(auth_cfg=self.auth_cfg, auth_type=self.auth_type)

        log.info("Obj: apiexeccmd | Instance Initialization Completed...")

        log.info("Exec Metadata Loading Completed...")

    def build_url(self):

        try:
            full_url = f"{self.root_url}{self.exec_cfg['path']}"

            log.info(f"Built URL: {full_url}")

            return full_url

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}"
            )

            raise

    def build_headers(self):

        try:
            headers = {}

            if not self.secret:
                log.info("Auth Not Provided, Skipping....")

                return headers

            if self.secret:
                if self.location == "header":
                    headers[self.name] = self.secret

                    log.info("Added Secret to headers")

                else:
                    log.warning(
                        f"Unsupported auth location: {self.location}. API key will not be included in headers."
                    )

            return headers

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}"
            )

            raise

    def build_params(self):

        try:
            params = {
                self.page_size_param: self.page_size_value,
                "vs_currency": self.vs_currency,
            }

            params.update(self.custom_query_params)

            log.info(f"Built query params: {params}")

            return params

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}"
            )

            raise

    def make_request(self, url, headers, params):

        log.info(
            f"Making request started with: url={url} | headers=Headers | params={params}"
        )

        try:
            response = requests.get(url=url, headers=headers, params=params)

            log.info(f"Request made: {response}")

            return response

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}"
            )

            raise

    def handle_response(self, response):

        try:
            data = response.json()

            log.info("Successfully fetched & stored the data")

            rows_processed = len(data)

            log.info(f"rows processed fetched: {rows_processed}")

            return data, rows_processed

        except Exception as excp:
            log.error(
                f"{EXCEPTION_DESCRIPTIONS.get(type(excp), 'Unexpected Error Occured')}"
            )

            raise

    def run(self):

        url = self.build_url()

        headers = self.build_headers()

        params = self.build_params()

        response = self.make_request(url=url, headers=headers, params=params)

        data, rows_processed = self.handle_response(response=response)

        job_metrics = {"rows_processed": rows_processed}

        return data, job_metrics
