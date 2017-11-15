import json
import os
from flask import current_app, Flask, redirect, request, render_template, url_for
from google.cloud import datastore
from datadog import initialize, statsd
from random import randint
from ddtrace import tracer
from doglib import utils


def create_app(config, debug=False):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug

    options = {
        'api_key': 'YOUR_API_KEY',
        'app_key': 'YOUR_APP_KEY',
        'statsd_host': os.environ['DATADOG_AGENT_HOST_IP'],
        'statsd_port': 8125
    }

    initialize(**options)

    tracer.set_tags({"pod_name": os.environ.get("MY_POD_NAME")})

    # Flask index route, get a random adlib puzzle
    @app.route('/', methods=['GET'])
    def view_index():
        statsd.increment("doglib.index_web_counter", tags=['pod_name:' + os.environ['MY_POD_NAME']])

        id = utils.get_random_key().id_or_name
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
    @app.route('/create', methods=['GET', 'POST'])
    def create_adlib():

        if (request.method == 'POST'):
            json_content = request.get_json()

            if ('title' in json_content and
                'adlib' in json_content and
                'entries' in json_content):

                utils.create_entity(json_content['title'],
                                    json_content['adlib'],
                                    json_content['entries'])
            else:
                return "error", 500

        return render_template("adlib-create.html"), 200

    return app
