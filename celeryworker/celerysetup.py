import logging
import os

from celery import Celery
from celery.signals import worker_process_init
from kombu import Exchange, Queue
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    OTLPMetricExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk import resources
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs import set_logger_provider


@worker_process_init.connect(weak=False)
def init_celery_tracing(*args, **kwargs):
    CeleryInstrumentor().instrument()
    LoggingInstrumentor().instrument()
    RequestsInstrumentor().instrument()

    traces_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", None)
    metrics_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_METRICS_ENDPOINT", None)
    logs_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_LOGS_ENDPOINT", None)
    logger = logging.getLogger(__name__)

    logging.info(f"OTEL_EXPORTER_OTLP_TRACES_ENDPOINT: {traces_endpoint} ")
    resource = resources.Resource(
        attributes={
            resources.SERVICE_NAME: "CELERYWORKER",
            resources.SERVICE_NAMESPACE: "CELERYWORKER_NAMESPACE",
        }
    )

    otlp_exporter = OTLPSpanExporter(endpoint=traces_endpoint)
    trace_provider = TracerProvider(resource=resource)
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(trace_provider)
    tracer = trace.get_tracer("celery-tracer")

    reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=metrics_endpoint)
    )
    metrics.set_meter_provider(
        MeterProvider(
            resource=resource,
            metric_readers=[reader],
        )
    )
    meter = metrics.get_meter("celery-meter")

    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)

    exporter = OTLPLogExporter(endpoint=logs_endpoint)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

    # Attach OTLP handler to root logger
    logging.getLogger().addHandler(handler)

app = Celery('task')
app.config_from_object('celeryconfig')

app.conf.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks',
          queue_arguments={'x-max-priority': 10}),
    Queue('dead_letter', routing_key='dead_letter'),
]

app.conf.task_acks_late = True
app.conf.task_default_priority = 5
app.conf.worker_prefetch_multiplier = 1
app.conf.worker_concurrency = 1

app.autodiscover_tasks()

