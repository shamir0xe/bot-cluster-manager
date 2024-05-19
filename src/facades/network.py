from __future__ import annotations
from typing import Any, Dict, List, Optional
import time

from python_graphql_client import GraphqlClient
from src.actions.network.check_response_got_errors import CheckResponseGotErrors
from src.actions.network.check_response_need_login import CheckResponseNeedLogin
from src.actions.network.extract_response_errors import ExtractResponseErrors
from src.models.utility.credentials import Credentials
from src.models.network.login_resonse import LoginResponse
from src.helpers.builders.query_builder import QueryBuilder
from src.helpers.decorators.query_wrapper import QueryWrapper
from src.helpers.decorators.singleton import singleton
from src.facades.env import Env
from src.facades.network_config import NetworkConfig
from src.types.query_types import QueryTypes


@singleton
class Network:
    queries_stack: List[QueryWrapper]
    credentials: Credentials
    errors: List[str]

    def __init__(self):
        self.credentials = Env().api.credentials
        self.config = NetworkConfig()
        self.client = GraphqlClient(endpoint=str(Env().api.url))
        self.query_builder = QueryBuilder()
        print("Network instance!")

    @staticmethod
    def query(query_wrapper: QueryWrapper) -> Optional[Dict[str, Any]]:
        return Network().query_procedure(query_wrapper)

    @property
    def error(self) -> Optional[str]:
        if self.errors:
            return self.errors[-1]
        return None

    def query_procedure(self, query_wrapper: QueryWrapper) -> Optional[Dict]:
        self.errors = []
        self.retry_cnt = 0
        self.queries_stack = [query_wrapper]
        return self.try_query()

    def execute(self, query_wrapper: QueryWrapper) -> Dict:
        return self.client.execute(**query_wrapper.query)

    def increment_tries(self) -> Network:
        self.retry_cnt += 1
        return self

    @property
    def current_query(self) -> QueryWrapper:
        return self.queries_stack[-1]

    def try_query(self) -> Optional[Dict]:
        if self.retry_cnt > self.config.max_retries:
            ## bad condition
            return None
        current_query = self.increment_tries().current_query
        try:
            response = self.execute(current_query)
        except Exception as e:
            return self.add_errors(str(e)).sleep().try_query()

        if CheckResponseGotErrors.check(response):
            ## resolving the response
            self.add_errors(ExtractResponseErrors.extract(response))
            if CheckResponseNeedLogin.check(response):
                if current_query.name != QueryTypes.LOGIN:
                    ## add login if needed
                    self.queries_stack += [
                        self.query_builder.auth(
                            self.credentials.username, self.credentials.password
                        ).build()
                    ]
            return self.try_query()
        elif current_query.name == QueryTypes.LOGIN:
            self.new_client(
                headers={
                    "Authorization": LoginResponse(
                        **response["data"][current_query.response_field]
                    ).token
                }
            )
        ## poping the top element
        self.pop()
        if self.queries_stack:
            return self.try_query()
        return response["data"][current_query.response_field]

    def pop(self) -> Network:
        self.queries_stack = self.queries_stack[:-1]
        return self

    def new_client(self, headers: dict) -> Network:
        self.client = GraphqlClient(endpoint=str(Env().api.url), headers=headers)
        return self

    def sleep(self) -> Network:
        time.sleep(self.config.sleep_interval)
        return self

    def add_errors(self, error: str) -> Network:
        print(f"Error occured {error}")
        self.errors += [error]
        self.errors = self.errors[: self.config.max_errors]
        return self
