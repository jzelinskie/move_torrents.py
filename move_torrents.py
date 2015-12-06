# Copyright 2015 Jimmy Zelinskie. All rights reserved.
# Use of this source code is governed by the BSD 2-Clause license,
# which can be found in the LICENSE file.

import argparse
import logging
import os
import sys

from bencode import bdecode, bencode


QBT_KEY = 'qBt-savePath'
LT_KEY = 'save_path'
FASTRESUME_EXT = '.fastresume.0'

logger = logging.getLogger(__name__)


def update_fastresume(file, find_path, replace_path):
    """
    qBittorrent stores metadata in "fastresume" files. The files are encoded in
    a format called bencode, which is used elsewhere in the BitTorrent protocol.
    There are two paths to your files in each fastresume file. One is for
    qBittorrent; the other is for libtorrent. This function runs a find and
    replace on those paths.
    """
    # Decode the bencoded file.
    fastresume = bdecode(file.read())

    # Update the two paths inside the file.
    fastresume[QBT_KEY] = fastresume[QBT_KEY].replace(find_path, replace_path)
    fastresume[LT_KEY] = fastresume[LT_KEY].replace(find_path, replace_path)

    # Overwrite the file with our updated structure.
    file.seek(0)
    file.write(bencode(fastresume))
    file.truncate()


def update_bt_backup(bt_backup_path, find_path, replace_path):
    """
    qBittorrent stores torrent metadata in a BT_BACKUP directory. This function
    walks that directory and runs a find and replace on the "fastresume" files
    for each torrent.
    """
    logger.info('searching for fastresume files in %s' % bt_backup_path)
    for _, _, files in os.walk(bt_backup_path):
        found = [name for name in files if name.endswith(FASTRESUME_EXT)]
        logger.info('found %d fastresume files' % len(found))
        for name in found:
            path = os.path.join(bt_backup_path, name)
            with open(path, 'r+') as raw:
                try:
                    update_fastresume(raw, find_path, replace_path)
                    logger.info('successfully updated %s' % path)
                except:
                    logger.exception('failed to update %s' % path)
                    continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find and replace filepaths in qBittorrent v3.3+'
    )
    parser.add_argument('--find-path',
                        help='path to find',
                        type=str,
                        required=True)
    parser.add_argument('--replace-path',
                        help='path that replaces find_path',
                        type=str,
                        required=True)
    parser.add_argument('--bt-backup-path',
                        help='path to qBittorrent BT_BACKUP directory',
                        type=str,
                        required=True)
    args = parser.parse_args()

    update_bt_backup(args.bt_backup_path, args.find_path, args.replace_path)
