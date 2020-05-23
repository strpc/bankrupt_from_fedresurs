#database settings:
PG_USER = 'user'
PG_PASSWORD = 'hackme'
PG_HOST = 'localhost'
PG_PORT = 5432
PG_DATABASE = 'bankrupt'

#log settings:
DEBUG_MODE = 'DEBUG'
DIR_NAME_LOG = 'logs'
FILE_NAME_LOG = 'bankrupt_from_fedresurs.log'
FILESIZE_LOG = 5 # ib Mb
COUNT_BACKUP_LOG = 5
LOG_FORMAT = '%(asctime)s: %(levelname)s: %(message)s'
FORMAT_DATE_TIME = '%Y-%m-%d %H:%M:%S'