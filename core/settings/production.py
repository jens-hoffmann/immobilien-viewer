from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
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

STATICFILES_DIRS = [BASE_DIR / "static"]  # Todo change static files handling

MEDIA_ROOT = BASE_DIR / 'media'
solr_url = os.environ.get('SOLR_URL', 'http://localhost:8983')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': f'{solr_url}/solr/haystackcore',
        'ADMIN_URL': f'{solr_url}/solr/admin/cores'
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
