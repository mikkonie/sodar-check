"""Main loop for running SODAR and iRODS checks on command line"""

import sys
import time

import settings

from sodar_check import SODARCheck


def main():
    try:
        sc = SODARCheck()
    except Exception as ex:
        print('SODARCheck init failed: {}'.format(ex))
        return
    while 1:
        sc.check_sodar_api()
        irods_ok = sc.check_irods_server()
        if irods_ok:
            sc.check_irods_file_read()
            sc.check_davrods_file_read()
        time.sleep(int(settings.CHECK_INTERVAL) * 60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
