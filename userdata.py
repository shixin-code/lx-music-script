import json
from typing import Tuple

# -*- coding: utf-8 -*-
import os.path

class UserData:
    def __init__(self, lx_music_data_root_dir, user_name):
        self.user_name = user_name
        self.user_dir = os.path.join(lx_music_data_root_dir, 'users', user_name)
        self.list_dir = os.path.join(self.user_dir, 'list')
        self.dislike_dir = os.path.join(self.user_dir, 'dislike')
        self.snapshot_dir = os.path.join(self.list_dir, 'snapshot')

    def get_user_name(self):
        return self.user_name

    def get_user_dir(self):
        return self.user_dir

    def get_list_dir(self):
        return self.list_dir

    def get_dislike_dir(self):
        return self.dislike_dir

    def get_snapshot_dir(self):
        return self.snapshot_dir
    
    def get_snapshot_info_file(self):
        return os.path.join(self.list_dir, 'snapshotInfo.json')

    def get_latest_snapshot_file_info(self) -> Tuple[int, str]:
        '''
        snapshot_info 文件格式:
        {
            "latest": "cdf61c83e66cf8f4e648608ecb9d748c",
            "time": 1715043305463,
            "list": [
                "cc3236e5b6cc818cec926951451c8a85",
                "e7542d9be0c680e36dcef08303314804"
            ],
            "clients": {
                "+umPNitDgt/25uE2Jlgatg==": {
                "snapshotKey": "34f6fcfdfab036fde320a91f4c10811b",
                "lastSyncDate": 1706453528624
                },
                "EXexHdhAH8fvBiPhgwMO7A==": {
                "snapshotKey": "cdf61c83e66cf8f4e648608ecb9d748c",
                "lastSyncDate": 1715043305463
                }
            }
        }
        返回json结构中的 time, latest 的值
        '''
        snapshot_info_file = self.get_snapshot_info_file()
        with open(snapshot_info_file, 'r') as f:
            snapshot_info = json.load(f)
            return snapshot_info.get('time'), snapshot_info.get('latest')
        return None, None

    def get_snapshot_file(self, snapshot_key):
        return os.path.join(self.snapshot_dir, 'snapshot_' + snapshot_key)
