import logging
import os

from django.apps import AppConfig

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import resources
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

endpoint = os.environ.get("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", None)
logger = logging.getLogger(__name__)

logging.info(f"OTEL_EXPORTER_OTLP_TRACES_ENDPOINT: {endpoint} ")

otlp_exporter = OTLPSpanExporter(endpoint=endpoint)
resource = resources.Resource(
  attributes={
    resources.SERVICE_NAME: "IMMOBLIENSERVICE",
    resources.SERVICE_NAMESPACE: "IMMOBLIENSERVICE_NAMESPACE",
  }
)

trace_provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(otlp_exporter)
trace_provider.add_span_processor(processor)
trace.set_tracer_provider(trace_provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer(__name__)

class ImmobilienviewerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ImmobilienViewer'
