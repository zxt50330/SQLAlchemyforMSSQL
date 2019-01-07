# -*- coding: utf-8 -*-
# © 2018 QYT Technology
# Authored by: Zhao Xingtao (zxt50330@gmail.com)

from flask import jsonify


def  call_procedure_sql_return(res, data='', status=True):
    if data:
        return jsonify(
            {
                "data": data,
                "status": status
            }
        )
    if not res:
        return jsonify(
            {
                "data": [],
                "status": True
            }
        )
    if res[0][0].get('Return Value') == 0:
        return jsonify(
            {
                "data": data or "success",
                "status": True
            }
        )
    else:
        return jsonify(
            {
                "data": data or "failure",
                "status": False
            }
        )


def call_procedure_with_output_return(res):
    while isinstance(res, list):
       res = res[0]
    the_output = res.get('the_output', '')
    if the_output:
        return jsonify({
            "data": the_output,
            "status": True
        })
    else:
        return jsonify({
            "data": "something wrong",
            "status": False
        })
