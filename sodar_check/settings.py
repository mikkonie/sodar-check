import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv(usecwd=True))

SODAR_URL = os.getenv('SODAR_CHECK_SODAR_URL', '0.0.0.0:8000')
SODAR_API_TOKEN = os.getenv('SODAR_CHECK_SODAR_API_TOKEN', '')
IRODS_ENV_PATH = os.getenv(
    'SODAR_CHECK_IRODS_ENV_PATH', '/home/user/.irods/irods_environment.json'
)
IRODS_FILE_PATH = os.getenv(
    'SODAR_CHECK_IRODS_FILE_PATH', '/sodarZone/path/to/your/file.txt'
)
DAVRODS_URL = os.getenv('SODAR_CHECK_DAVRODS_URL', '')
CHECK_INTERVAL = os.getenv('SODAR_CHECK_INTERVAL', 10)
LOG_LEVEL = os.getenv('SODAR_CHECK_LOG_LEVEL', 'INFO')
LOG_FORMAT = os.getenv(
    'SODAR_CHECK_LOG_FORMAT', '%(asctime)s [%(levelname)s] %(message)s'
)
LOG_DATEFMT = os.getenv('SODAR_CHECK_LOG_DATEFMT', '%Y-%m-%d %H:%M:%S')
