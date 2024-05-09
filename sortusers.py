# -*- coding: utf-8 -*-
import userdata
import utils
import log
import sortsnapshot

user_name_list = ["csx_75d1f0"]

users_result = utils.load_users_handle_result()

def run_sort_by_user(user_name):
    log.i('start sort user %s...' % user_name)
    user_data = userdata.UserData(user_name)
    time, snapshot_key = user_data.get_latest_snapshot_file_info()
    user_result = users_result.get(user_name, {})
    not_need_sort = (snapshot_key == user_result.get('latest')) and (time == user_result.get('time')) 
    log.i('need sort: %s %s ?= %s, %s ?= %s' 
          % (not not_need_sort, snapshot_key, user_result.get('latest'), time, user_result.get('time')))
    if not_need_sort:
        log.i('user %s snapshot %s already sorted at %s' % (user_name, snapshot_key, time))
        return
    sortsnapshot.sort_snapshot_file(user_data.get_snapshot_file(snapshot_key))
    user_result['latest'] = snapshot_key
    user_result['time'] = time
    users_result[user_name] = user_result

for user_name in user_name_list:
    run_sort_by_user(user_name)
utils.save_users_handle_result(users_result)