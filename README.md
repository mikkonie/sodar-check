# SODAR Check

Basic tool for monitoring the availability of
[SODAR](https://github.com/bihealth/sodar-server) and associated
[iRODS](https://irods.org) components. Possibly modifiable into something
actually usable.

I created this for dev purposes and it's currently hardcoded to log into stdout.
That can be changed to make external tools parse the log. Furthermore, this
could be turned into a proper package for integrating the `sodar_check` module
into other monitoring tools supporting Python. I'm open for suggestions.

Tested on Python 3.11.

## Usage

1. Install requirements with `pip install -r requirements.txt`.
2. Create `.env` file with your configuration (see below).
3. Run with `make run`.
4. Insert the iRODS password of the specified user when prompted.
5. Observe the log output. Problems show up with the `ERROR` log level.

## Configuration

| Environment Variable          | Description                                      | Example                                    |
|-------------------------------|--------------------------------------------------|--------------------------------------------|
| `SODAR_CHECK_SODAR_URL`       | SODAR server URL, including possible port        | `https://sodar.example.com`                |
| `SODAR_CHECK_SODAR_API_TOKEN` | SODAR API token                                  | <64-character string>                      |
| `SODAR_CHECK_IRODS_ENV_PATH`  | Path to iRODS client environment JSON file       | `/home/user/.irods/irods_environment.json` |
| `SODAR_CHECK_IRODS_FILE_PATH` | Path to file on iRODS server (1)                 | `/sodarZone/path/to/your/file.txt`         |
| `SODAR_CHECK_DAVRODS_URL`     | Davrods server URL (2)                           | `https://sodar.example.com`                |
| `SODAR_CHECK_INTERVAL`        | Interval for performing checks in minutes        | `10`                                       |
| `SODAR_CHECK_LOG_LEVEL`       | Logging level                                    | `INFO`                                     |
| `SODAR_CHECK_LOG_FORMAT`      | Log format in syntax accepted by Python logging  | `%(asctime)s [%(levelname)s] %(message)s`  |
| `SODAR_CHECK_LOG_DATEFMT`     | Date format in syntax accepted by Python logging | `%Y-%m-%d %H:%M:%S`                        |

1. It is recommended to select a small-ish file, as it will be read into memory
   on each iteration of the checks. The user specified in the iRODS environment
   file must also be able to access this file.
2. If the SODAR instance is deployed using
   [sodar-docker-compose](https://github.com/bihealth/sodar-docker-compose),
   this should be the same URL as for the SODAR server. If left empty, the SODAR
   server URL is assumed.
