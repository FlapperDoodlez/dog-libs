import json
import os
from flask import current_app, Flask, redirect, request, render_template, url_for
from google.cloud import datastore
from datadog import initialize, statsd
from random import randint
from ddtrace import tracer
from doglib import utils


def create_app(debug=False):
    app = Flask(__name__)

    app.debug = debug

    options = {
        'statsd_host': os.environ['DATADOG_AGENT_HOST_IP'],
        'statsd_port': 8125
    }

    initialize(**options)

    tracer.set_tags({"pod_name": os.environ.get("MY_POD_NAME")})

    # Flask index route, get a random adlib puzzle
    @app.route('/', methods=['GET'])
    def view_index():
        statsd.increment("doglib.index_web_counter", tags=['pod_name:' + os.environ['MY_POD_NAME']])

        random_key = utils.get_random_key()
        if (random_key is None):
            return render_template("adlib-empty.html"), 200
        else:
            id = random_key.id_or_name
            entity = utils.get_entity(id)
            return render_template("adlib-index.html", entity=entity, id=id), 200

    # Flask adib solution
    @app.route('/<int:id>/solution/', methods=['GET', 'POST'])
    def view_adlib_solution(id):
        entity = utils.get_solution(id)

        if entity:
            if (request.method == 'POST'):
                words = request.form.getlist('word')
                utils.process_adlib(id, words)
            else:
                words = entity['popular_words']

            return render_template("adlib-solution.html", entity=entity,
                                   word_data=words, id=id)
        else:
            return render_template("404.html"), 404

    # Flask create adlib
    @app.route('/create/', methods=['GET', 'POST'])
    def create_adlib():

        if (request.method == 'POST'):
            if ('title' in request.form and
                'adlib' in request.form and
                'entries' in request.form):

                utils.create_entity(request.form['title'],
                                    request.form['adlib'],
                                    request.form['entries'])
            else:
                return "error", 500

        return render_template("adlib-create.html"), 200

    return app
