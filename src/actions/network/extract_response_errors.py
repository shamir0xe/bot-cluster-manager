from typing import Dict


class ExtractResponseErrors:
    @staticmethod
    def extract(response: Dict) -> str:
        if "errors" in response:
            return str(response["errors"]).lower()
        return ""
