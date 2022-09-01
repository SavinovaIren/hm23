import os

from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
import re

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def do_cmd(cmd: str, value: str, data: list) -> list[str]:
    if cmd == 'filter':
        cmd_result = list(filter(lambda record: value in record, data))
    elif cmd == 'map':
        column = int(value)
        if column == 0:
            cmd_result = list(map(lambda record: record.split()[column], data))
        elif column == 1:
            cmd_result = list(map(lambda record: record.split()[3:5], data))
        elif column == 2:
            cmd_result = list(map(lambda record: " ".join(record.split()[5:]), data))
    elif cmd == 'unique':
        cmd_result = list(set(data))
    elif cmd == 'sort':
        cmd_result = sorted(data, reverse=True)
    elif cmd == 'regexp':
        png_list = list(filter(lambda rec: re.findall(value, rec), data))
        cmd_result = list(map(lambda record: " ".join(record.split()[:9]), png_list))

    return cmd_result


def do_query(params: dict) -> list[str]:
    with open(os.path.join(DATA_DIR, params["file_name"])) as f:
        file_data = f.readlines()

    res = file_data
    if "cmd1" in params.keys():
        result = do_cmd(params["cmd1"], params["value1"], res)
    elif "cmd2" in params.keys():
        result = do_cmd(params["cmd2"], params["value2"], res)
    elif "cmd3" in params.keys():
        result = do_cmd(params["cmd3"], params["value3"], res)
    elif "cmd4" in params.keys():
        result = do_cmd(params["cmd4"], params["value4"], res)
    elif "cmd5" in params.keys():
        result = do_cmd(params["cmd5"], params["value5"], res)
    return result


@app.route("/perform_query", methods=["POST"])
def perform_query():
    data = request.json
    file_name = data["file_name"]
    if not os.path.exists(os.path.join(DATA_DIR, file_name)):
        raise BadRequest

    return jsonify(do_query(data))


if __name__ == "__main__":
    app.run()
