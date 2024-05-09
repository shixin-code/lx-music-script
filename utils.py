# -*- coding: utf-8 -*-

import json
import os.path

def load_users_handle_result():
    result_file = os.path.join(os.path.dirname(__file__), 'users_handle_result.json')
    if os.path.exists(result_file):
        with open(result_file, 'r') as f:
            data = f.read()
            if data:
                return json.loads(data)
    return {} 

def save_users_handle_result(result):
    result_file = os.path.join(os.path.dirname(__file__), 'users_handle_result.json')
    with open(result_file, 'w') as f:
        f.write(json.dumps(result, ensure_ascii=False, indent=4))