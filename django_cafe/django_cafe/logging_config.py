import os

os.makedirs('logs', exist_ok=True)

LOGGER_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'order_log': {
            'format': '{levelname} - {name} - {message}',
            'style':'{'
        },
        'item_log': {
            'format': '{levelname} - {message}',
            'style':'{'
        },
    },
    'handlers': {
        'orders_file':{
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/orders.log',
            'formatter': 'order_log'
        },
        'items_file':{
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/items.log',
            'formatter': 'item_log'
        }
    },
    'loggers': {
        'orders':{
            'handlers': ['orders_file'],
            'level': 'INFO',
            'propogate': False
        },
        'items': {
            'handlers': ['items_file'],
            'level': 'INFO',
            'propogate': False
        }
    }
}

def configure_logging():
    from logging.config import dictConfig
    dictConfig(LOGGER_CONFIG)
