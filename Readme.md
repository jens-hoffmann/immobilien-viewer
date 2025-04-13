# ImmobilienApp

Django web application for displaying plot and properties gathered via web scraping from official web site for compulsory auctions.

## Technologies

* Django for backend and frontend
* Celery with RabbitMQ to perform and schedule web scraping jobs and enrich object with geocoding informations
* Nominatim for geocoding
* Selenium for web scraping
* GeoDjango and PostGIS to store geospatial informations
* Leaflet to diplay maps in frontend
* PyTest for testing
* Prometheus, Opentelemetry, Jaeger, Grafana for monitoring