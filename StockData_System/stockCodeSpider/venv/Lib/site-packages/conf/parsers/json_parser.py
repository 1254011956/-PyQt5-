import json


def parse(file_stream):
    # Parse the given file stream of json format to a dict.
    return json.load(file_stream)
