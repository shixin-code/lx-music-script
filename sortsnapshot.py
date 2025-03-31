# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import argparse
import sys
import shutil
import log
import json
from pypinyin import lazy_pinyin


def get_name(item):
    name = item['name']
    s = ''.join(lazy_pinyin(name))
    # log.i(name + '=' +s)
    return s.lower()

def sort(file_path):
    '''
    加载json文件 file_path，对‘defaultList’ 列表，按照‘name’字段排序。文件格式：
    {
        "defaultList":[    ## 【试听列表】
            {}, {}         ## 歌曲列表
        ],
        "loveList":[       ## 【我的收藏】
            {}, {}         ## 歌曲列表
        ],     
        "userList":[       ## 其他用户创建的列表
            {
                "id":"userlist_1702347341784",
                "name":"我的收藏已下载",
                "list":[]  ## 歌曲列表
            },
            {
                "id":"userlist_1706452473261",
                "name":"不喜欢",
                "list":[]  ## 歌曲列表
            }
        ]
    }
    '''

    ## 加载json文件，对指定列表按照‘name’字段排序
    sorting_list_names = ['defaultList', 'loveList']
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

        ## 加载不喜欢的歌曲id列表
        unlike_song_ids = load_unlike_song_ids(data)

        for list_name in sorting_list_names:
            if list_name not in data:
                continue
            song_list = data[list_name]
            ## 移除不喜欢的歌曲
            if unlike_song_ids:
                song_list = [song for song in song_list if song['id'] not in unlike_song_ids]

            ## 按照‘name’字段排序
            sorted_list = sorted(song_list, key=get_name)
            data[list_name] = sorted_list

    ## 保存排序后的数据
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_unlike_song_ids(data):
    '''
    加载不喜欢的歌曲id列表
    '''
    ## 不喜欢的列表名称，用于移除不喜欢的歌曲
    unlike_list_name = '不喜欢'

    unlike_son_ids = {}

    user_list = data['userList']
    for item in user_list:
        if item['name'] == unlike_list_name:
            unlike_son_ids = { song["id"] for song in item['list'] }
            return unlike_son_ids
    return None

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
    
def sort_snapshot_file(file_path):
    backup_file(file_path)
    sort(file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Usage: %s' % sys.argv[0])
    parser.add_argument('-f', '--file', required=True, help='lx-music snapshot file path')
    args = parser.parse_args()
    sort_snapshot_file(args.file)
