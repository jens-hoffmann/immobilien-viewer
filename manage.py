#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


def main():
    load_dotenv()

    app_environment = os.environ.get("APP_ENV", "local")

    """Run administrative tasks."""
    if app_environment == "local":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.local')
    elif app_environment == "prod":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')
        DjangoInstrumentor().instrument(is_sql_commentor_enabled=True)
        LoggingInstrumentor().instrument()
        RequestsInstrumentor().instrument()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
