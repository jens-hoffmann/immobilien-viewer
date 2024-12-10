from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('POSTGRES_HOST'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'trace_formatter': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s] [%(funcName)s] %(message)s',  # optional, default is logging.BASIC_FORMAT
            'datefmt': '%Y-%m-%d %H:%M:%S',  # optional, default is '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'trace_formatter',
            'filename': 'webapp.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'trace_formatter',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'WARNING',
    },
}