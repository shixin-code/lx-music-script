# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import argparse
import sys
import shutil
import log
import json
from pypinyin import lazy_pinyin

parser = argparse.ArgumentParser('Usage: %s' % sys.argv[0])
parser.add_argument('-f', '--file', required=True, help='lx-music snapshot file path')
args = parser.parse_args()


def get_name(item):
    name = item['name']
    s = ''.join(lazy_pinyin(name))
    # log.i(name + '=' +s)
    return s.lower()

def sort(file_path):
    '''
    加载json文件 file_path，对‘defaultList’ 列表，按照‘name’字段排序
    '''
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        default_list = data['defaultList']
        sorted_list = sorted(default_list, key=get_name)
        data['defaultList'] = sorted_list
        # log.i(json.dumps(data, indent=4))

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

import os
import datetime

def backup_file(file_path):
    '''
    备份文件
    '''
    backup_path = os.path.dirname(file_path) + os.sep + 'backup'
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)
    backup_file_name = os.path.basename(file_path) + '.' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    backup_file_path = backup_path + os.sep + backup_file_name
    log.i('backup file: %s --> %s' % (file_path, backup_file_path))
    shutil.copy(file_path, backup_file_path)
    

if __name__ == '__main__':
    backup_file(args.file)
    sort(args.file)