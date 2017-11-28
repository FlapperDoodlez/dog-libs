import json
from flask import current_app
from google.cloud import datastore
from random import randint
from datadog import statsd
from ddtrace import tracer
import time


def get_entity(id, kind='adlib'):
    with tracer.trace("utils.get_entity", service="adlib") as span:

        # Get adlib entry
        client = datastore.Client()
        key = client.key(kind, id)
        try:
            with tracer.trace("client.get", service="datastore") as child_span:
                entity = client.get(key)
                return entity
        except Exception as e:
            print(e)
            # Oops! Tried to retrieve an entity that doesn't exist
            return None


def process_adlib(id, words_sent):
    with tracer.trace("utils.process_adlib", service="adlib") as span:
        with tracer.trace("client.get", service="datastore") as child_span:
            # Get old adlib data
            client = datastore.Client()
            key = client.key('adlib', id)
            entity = client.get(key)

        # Assert that the number of words sent matches the number of entries
        num_words_sent = len(words_sent)
        num_entries = len(entity['entries'])
        if (num_words_sent != num_entries):
            return

        # Update list of words in adlib (either increment or add to list)
        word_usage_in_entity = entity['words']

        if ('popular_words' in entity):
            popular_words = entity['popular_words']
        else:
            popular_words = entity['popular_words'] = []

        with tracer.trace("utils.process_adlib.apply_input") as child_span:
            time.sleep(0.2)
            for i in range(0, num_entries):
                entry = words_sent[i].lower()

                if (entry in word_usage_in_entity):
                    word_usage_in_entity[entry] += 1
                else:
                    word_usage_in_entity[entry] = 1

                if (len(popular_words) < num_entries):
                    popular_words.append(entry)
                else:
                    popular_word = popular_words[i]
                    popular_word_usage = word_usage_in_entity[popular_word]

                    if (word_usage_in_entity[entry] > popular_word_usage):
                        popular_words[i] = entry

        with tracer.trace("client.put", service="datastore") as child_span:
            client.put(entity)

# Get the adlib solution, and clean up the entity
def get_solution(id, kind='adlib'):
    with tracer.trace("utils.get_solution", service="adlib") as span:

        # Tracing for get_entity is done in that function
        entity = get_entity(id, kind)

        if (entity is None):
            return None
        else:
            with tracer.trace("clean_entity") as span:
                cleaned_entity = {
                    'title': entity['title'],
                    'adlib': entity['adlib']
                }

                if ('popular_words' in entity):
                    cleaned_entity['popular_words'] = entity['popular_words']
                else:
                    cleaned_entity['popular_words'] = []

                return cleaned_entity

# Get a random key of an entity from our datastores
def get_random_key(kind='adlib'):
    with tracer.trace("utils.get_random_key", service="adlib") as span:
        client = datastore.Client()
        query = client.query(kind='adlib')
        query.keys_only()

        with tracer.trace("query.fetch", service="datastore") as child_span:
            query_keys_list = list(query.fetch())

        random_index = randint(0, len(query_keys_list) - 1)
        return query_keys_list[random_index].key

# Create an entity
def create_entity(title, adlib, entries):
    with tracer.trace("utils.create_entity", service="adlib") as span:
        client = datastore.Client()

        # Create entity
        incomplete_key = client.key('adlib')

        entity = datastore.Entity(key=incomplete_key)

        with tracer.trace("entity.update", service="datastore") as child_span:
            entries = [x.strip() for x in entries.split(',')]
            entity.update({
                'title': title,
                'adlib': adlib,
                'entries': entries,
                'words': datastore.Entity(),
                'popular_words': [],
            })

        with tracer.trace("entity.put", service="datastore") as child_span:
            client.put(entity)
