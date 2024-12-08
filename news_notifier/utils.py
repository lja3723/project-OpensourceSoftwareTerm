import json


class JsonBeautifier:
    @staticmethod
    def toString(jsonObj):
        return json.dumps(jsonObj, indent=4)

    @staticmethod
    def printPretty(jsonObj):
        print(json.dumps(jsonObj, indent=4))


__all__ = ['JsonBeautifier']
