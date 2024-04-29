from typing import Dict


class CheckResponseNeedLogin:
    @staticmethod
    def check(response: Dict) -> bool:
        message = str(response["errors"]).lower()
        return "login" in message or "token" in message
