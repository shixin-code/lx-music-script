# -*- coding: utf-8 -*-
import argparse, sys, os
import userdata
import utils
import log
import sortsnapshot


def run_sort_by_user(user_data):
    user_name = user_data.get_user_name()
    time, snapshot_key = user_data.get_latest_snapshot_file_info()

    users_result = utils.load_users_handle_result()
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

    utils.save_users_handle_result(users_result)

def find_real_user_name(datadir, user_name):
    user_dir = os.path.join(datadir, 'users')
    user_name_list = os.listdir(user_dir)
    for name in user_name_list:
        if name.startswith(user_name):
            return name
    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Usage: %s' % sys.argv[0])
    parser.add_argument('--datadir', required=True, help='lx-music data root dir')
    parser.add_argument('--username', required=True, help='lx-music sync user name without suffix')
    args = parser.parse_args()

    log.i('lx-music data root dir: %s' % args.datadir)
    log.i('start sort user %s...' % args.username)
    real_user_name = find_real_user_name(args.datadir, args.username)
    if real_user_name is None:
        log.e('user %s not found' % args.username)
        sys.exit(1)
    log.i('real user name: %s' % real_user_name)
    user_data = userdata.UserData(args.datadir, real_user_name)
    run_sort_by_user(user_data)
