from typing import Dict


class CheckResponseGotErrors:
    @staticmethod
    def check(response: Dict) -> bool:
        return "errors" in response
