import json


class JsonBeautifier:
    @staticmethod
    def toString(jsonObj):
        return json.dumps(jsonObj, indent=4)

    @staticmethod
    def printPretty(jsonObj):
        print(json.dumps(jsonObj, indent=4))


def dedent(text: str):
    return "\n".join(line.lstrip() for line in text.splitlines())


__all__ = ['JsonBeautifier', 'dedent']
