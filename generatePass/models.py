from django.db import models
import json


class validate:
    def validateJSON(self, jsonData):
        try:
            json.loads(jsonData.read().decode())
        except ValueError as err:
            return False
        return True
