FROM python:3.8.2

RUN mkdir -p /usr/src/currency_monitoring/
WORKDIR /usr/src/currency_monitoring/

COPY . /usr/src/currency_monitoring/

RUN pip install --no-cache-dir -r /usr/src/currency_monitoring/requirements.txt

ENV TZ Europe/Kiev

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["/usr/src/currency_monitoring/runserver.py"]