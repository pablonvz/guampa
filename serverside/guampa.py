#!/usr/bin/env python3

"""
This module handles all of the URL dispatching for guampa, mapping from
URLs to the functions that will be called in response.
"""
import json
import os

from flask import Flask, request, session, url_for, redirect, render_template,\
                  abort, g, flash, _app_ctx_stack, send_from_directory, jsonify
from werkzeug import check_password_hash, generate_password_hash

import db
import utils

DEBUG = True
app = Flask(__name__)

## this file is in serverside, but we need one directory up.
myfn = os.path.abspath(__file__)
app.root_path = os.path.dirname(os.path.dirname(myfn)) + os.path.sep
app.debug = DEBUG

@utils.nocache
@app.route('/')
def index():
    return send_from_directory(app.root_path + 'app', 'index.html')

@app.route('/partials/<fn>')
def partials(fn):
    return send_from_directory(app.root_path + 'app/partials', fn)

@app.route('/css/<fn>')
def css(fn):
    return send_from_directory(app.root_path + 'app/css', fn)

@utils.nocache
@app.route('/js/<fn>')
def js(fn):
    return send_from_directory(app.root_path + 'app/js', fn)

@app.route('/img/<fn>')
def img(fn):
    return send_from_directory(app.root_path + 'app/img', fn)

@app.route('/lib/<fn>')
def lib(fn):
    return send_from_directory(app.root_path + 'app/lib', fn)

@app.route('/json/documents')
@utils.json
@utils.nocache
def documents():
    docs = db.list_documents()
    out = {'documents': [{'title': doc.title, 'id':doc.id} for doc in docs]}
    print(out)
    return(json.dumps(out))

@app.route('/json/tags')
@utils.json
@utils.nocache
def tags():
    tags = db.list_tags()
    out = {'tags': [tag.text for tag in tags]}
    print(out)
    return(json.dumps(out))

@app.route('/json/documents/<tagname>')
@utils.json
@utils.nocache
def documents_for_tag(tagname):
    docs = db.documents_for_tagname(tagname)
    out = {'documents': [{'title': doc.title, 'id':doc.id} for doc in docs]}
    print(out)
    return(json.dumps(out))

@app.route('/json/document/<docid>')
@utils.json
@utils.nocache
def document(docid):
    """All the stuff you need to render a document in the editing interface."""
    docid = int(docid)
    sentences = db.sentences_for_document(docid)

    sent_texts = [sentence.text for sentence in sentences]
    trans_texts = []
    ## XXX(alexr): make this into a faster query or something
    for sentence in sentences:
        latest = db.latest_translation_for_sentence(sentence.id)
        trans_texts.append(latest.text if latest else None)

    out = {'docid': docid, 'sentences':sent_texts, 'translations':trans_texts}
    print(out)
    return(json.dumps(out))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
