import os

os.makedirs('logs', exist_ok=True)

LOGGER_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} - {name} - {message}',
            'style':'{'
        },
    },
    'handlers': {
        'orders_file':{
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/orders.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'orders':{
            'handlers': ['orders_file'],
            'level': 'INFO',
            'propogate': False
        }
    }
}

def configure_logging():
    from logging.config import dictConfig
    dictConfig(LOGGER_CONFIG)
