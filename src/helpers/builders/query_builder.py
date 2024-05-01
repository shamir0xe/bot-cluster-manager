from __future__ import annotations
from typing import Dict, Optional
from src.helpers.builders.base_builder import BaseBuilder
from src.helpers.decorators.query_wrapper import QueryWrapper
from src.types.query_types import QueryTypes


class QueryBuilder(BaseBuilder):
    name: QueryTypes
    query: str
    response_field: str
    vars: Optional[Dict] = None

    @staticmethod
    def bot_info(bot_id: int) -> QueryBuilder:
        builder = QueryBuilder()
        builder.name = QueryTypes.BOT_INFO
        builder.response_field = "botInfo"
        builder.query = """
            query BotInfoAdminPermission($bot_id: String!) {
                botInfo(botId: $bot_id) {
                    id
                    token
                    name
                }
            }
        """
        builder.vars = {"bot_id": str(bot_id)}
        return builder

    @staticmethod
    def auth(username: str, password: str) -> QueryBuilder:
        builder = QueryBuilder()
        builder.name = QueryTypes.LOGIN
        builder.response_field = "login"
        builder.query = """
            mutation Login($username: String!) {
                login(telegramId: $username) {
                    id
                    token
                }
            } 
        """
        builder.vars = {"username": username}
        return builder

    @staticmethod
    def get_pages(bot_id: int) -> QueryBuilder:
        builder = QueryBuilder()
        builder.name = QueryTypes.GET_PAGES
        builder.response_field = "botInfo"
        builder.query = """
            query BotInfoAdminPermission($bot_id: String!) {
                botInfo(botId: $bot_id) {
                    pages
                }
            }
        """
        builder.vars = {"bot_id": str(bot_id)}
        return builder

    @staticmethod
    def request_session(bot_id: int, telegram_id: str) -> QueryBuilder:
        builder = QueryBuilder()
        builder.name = QueryTypes.REQUEST_SESSION
        builder.response_field = "requestBotSession"
        builder.query = """
        mutation RequestBotSession($bot_id: String!, $telegram_id: String!) {
          requestBotSession(botId: $bot_id, telegramId: $telegram_id) {
            id
          }
        }
        """
        builder.vars = {"bot_id": str(bot_id), "telegram_id": telegram_id}
        return builder

    @staticmethod
    def update_session(session_id: str, data: str) -> QueryBuilder:
        builder = QueryBuilder()
        builder.name = QueryTypes.UPDATE_SESSION
        builder.response_field = "updateBotSession"
        builder.query = """
            mutation UpdateSession($data: String!, $session_id: String!) {
              updateBotSession(
                data: $data
                sessionId: $session_id
              ) {
                id
                data
              }
            }
        """
        builder.vars = {"data": data, "session_id": session_id}
        return builder

    def build(self, *args, **kwargs) -> QueryWrapper:
        return QueryWrapper(
            name=self.name,
            response_field=self.response_field,
            query={"query": self.query, "variables": self.vars},
        )
