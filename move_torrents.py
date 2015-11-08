# Copyright 2015 Jimmy Zelinskie. All rights reserved.
# Use of this source code is governed by the BSD 2-Clause license,
# which can be found in the LICENSE file.

import argparse
import os
import sys

from bencode import bdecode, bencode


def update_path(fastresume, find_path, replace_path):
    """
    There are two paths in each fastresume file. One is for qBittorrent the
    other is for libtorrent.
    """
    fastresume['qBt-savePath'] = fastresume['qBt-savePath'].replace(
            qBT_format(find_path),
            qBT_format(replace_path)
    )
    fastresume['save_path'] = fastresume['save_path'].replace(
            libtorrent_format(find_path),
            libtorrent_format(replace_path)
    )


def qBT_format(path):
    """
    If you're on Windows, qBT expects paths to use forward slashes.
    """
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        return path.replace('\\', '/')

    return path


def libtorrent_format(path):
    """
    If you're on Windows, libtorrent expects paths to use backslashes.
    """
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        return path.replace('/', '\\')

    return path


def update_BT_BACKUP(backup_path, find_path, replace_path):
    for _, _, files in os.walk(backup_path):
        for name in files:
            if name.endswith('.fastresume'):
                path = backup_path + '/' + name
                with open(path, 'r+') as raw:
                    try:
                        fastresume = bdecode(raw.read())
                        update_path(fastresume, find_path, replace_path)
                        raw.seek(0)
                        raw.write(bencode(fastresume))
                        raw.truncate()
                    except:
                        print 'failed to update %s' % path
                        continue


class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


if __name__ == '__main__':
    parser = DefaultHelpParser(
            description='Find and replace filepaths in qBittorrent v3.3+'
    )
    parser.add_argument('--find_path',
                        help='path to find',
                        type=str)
    parser.add_argument('--replace_path',
                        help='path that replaces find_path',
                        type=str)
    parser.add_argument('--backup_path',
                        help='path to qBittorrent BT_BACKUP directory',
                        type=str)
    args = parser.parse_args()
    update_BT_BACKUP(args.backup_path, args.find_path, args.replace_path)
