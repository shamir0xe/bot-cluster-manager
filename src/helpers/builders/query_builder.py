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

    def build(self, *args, **kwargs) -> QueryWrapper:
        return QueryWrapper(
            name=self.name,
            response_field=self.response_field,
            query={"query": self.query, "variables": self.vars},
        )
