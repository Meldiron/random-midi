#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import time
from datetime import datetime

from flask import Flask, request, jsonify, send_file

from masterpiece import Masterpiece

app = Flask(__name__)

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

@app.route('/', defaults={'u_path': ''}, methods = HTTP_METHODS)
@app.route('/<path:u_path>', methods = HTTP_METHODS)
def handler(u_path):
    dtime = datetime.now()
    ans_time = time.mktime(dtime.timetuple())
    params_file = open("song_settings.json", "r")
    params = json.load(params_file)
    params_file.close()
    my_masterpiece = Masterpiece(
        rules_path="rules.json",
        length=params["length"],
        tempo=params["tempo"])
    subfolder = "output"
    if not os.path.isdir(subfolder):
        os.mkdir(subfolder)
    file = "{folder}/midi_{suffix}.mid".format(
        folder=subfolder,
        suffix=ans_time)
    my_masterpiece.create_midi_file(file, True, False, True)

    name = "midi_{suffix}.mid".format(
        suffix=ans_time)
    return send_file(file)
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=3000)