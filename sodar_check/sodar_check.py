"""SODARCheck for SODAR availability checks"""

import getpass
import logging
import requests
import time

from irods.session import iRODSSession

import settings


logging.getLogger('irods').disabled = True
logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(settings.LOG_LEVEL)
log_handler = logging.StreamHandler()
log_formatter = logging.Formatter(
    settings.LOG_FORMAT, datefmt=settings.LOG_DATEFMT
)
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)

API_PATH = '/project/api/users/current'


class SODARCheck:
    """SODAR and iRODS availability checks"""

    def __init__(self):
        logger.debug('Init SODAR Check..')
        print(settings.IRODS_ENV_PATH)
        # Set vars
        self.api_url = settings.SODAR_URL + API_PATH
        self.api_headers = {
            'Authorization': f'token {settings.SODAR_API_TOKEN}'
        }
        self.irods_pw = getpass.getpass(prompt='iRODS password: ')
        self.irods_kw = {
            'irods_env_file': settings.IRODS_ENV_PATH,
            'password': self.irods_pw,
        }
        self.davrods_url = settings.DAVRODS_URL + settings.IRODS_FILE_PATH
        # Test iRODS connection
        try:
            with iRODSSession(**self.irods_kw) as irods:
                _ = irods.server_version
                logger.info('iRODS auth successful')
                self.irods_user = irods.username
        except Exception:
            msg = 'iRODS auth failed'
            logger.error(msg)
            raise ValueError(msg)
        logger.debug('Init OK')

    def check_sodar_api(self):
        """Check SODAR server availability with an API request"""
        logger.debug('Run check_sodar_api()..')
        try:
            response = requests.get(self.api_url, headers=self.api_headers)
            if response.status_code == 200:
                logger.info('OK: SODAR server available')
                return True
            else:
                logger.error(
                    'ERROR: SODAR API request unsuccessful: '
                    f'{response.status_code}'
                )
                return False
        except Exception as ex:
            logger.error(f'ERROR: Failed to perform SODAR API request: {ex}')
            return False

    def check_irods_server(self):
        """Check iRODS iCAT server availability"""
        logger.debug('Run check_irods_server()..')
        try:
            with iRODSSession(**self.irods_kw) as irods:
                irods_version = irods.server_version
                logger.info(
                    'OK: iRODS iCAT server available (version={})'.format(
                        '.'.join([str(x) for x in irods_version])
                    )
                )
                return True
        except Exception as ex:
            logger.error(f'ERROR: Failed to connect to iRODS iCAT server: {ex}')
            return False

    def check_irods_file_read(self):
        """Check iRODS file reading"""
        logger.debug('Run check_irods_file_read()..')
        with iRODSSession(**self.irods_kw) as irods:
            obj_exists = irods.data_objects.exists(settings.IRODS_FILE_PATH)
            if not obj_exists:
                logger.error('ERROR: iRODS file with given path does not exist')
                return False
            else:
                logger.debug('iRODS file exists')
            obj = irods.data_objects.get(settings.IRODS_FILE_PATH)
            try:
                t_start = time.time()
                with obj.open('r') as f:
                    f_data = f.read()
                t_end = time.time() - t_start
                f_len = len(f_data)
                logger.info(
                    'OK: iRODS file successfully read '
                    f'({f_len}B in {round(t_end, 3)}s)'
                )
                return True
            except Exception as ex:
                logger.error(f'ERROR: Failed to read file: {ex}')
                return False

    def check_davrods_file_read(self):
        """Check Davrods file reading"""
        logger.debug('Run check_davrods_file_read()..')
        try:
            response = requests.get(
                self.davrods_url, auth=(self.irods_user, self.irods_pw)
            )
            if response.status_code == 200:
                logger.info('OK: Davrods available and file can be read')
                return True
            else:
                logger.error(
                    'ERROR: Davrods request unsuccessful: '
                    f'{response.status_code}'
                )
                return False
        except Exception as ex:
            logger.error(f'ERROR: Failed to connect to Davrods: {ex}')
            return False