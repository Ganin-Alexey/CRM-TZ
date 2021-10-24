FROM python:3
ENV PYTHONUNBUFFERED=1

WORKDIR /Itorum
ADD requirements.txt /Itorum
COPY wsgi-entrypoint.sh /Itorum
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["./wsgi-entrypoint.sh"]