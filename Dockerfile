FROM gcr.io/google_appengine/python

RUN virtualenv -p python2.7 /env

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD . /app

CMD ddtrace-run gunicorn -b 0.0.0.0:$PORT main:app
