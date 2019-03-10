from flask import Flask, request, jsonify, json
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '<h1>Project 1</h1>'


@app.route('/tags', methods=['GET'])
def tags():
    return '<h1>Tags microservice</h1>'



@app.route('/tags/retrieve_tags', methods=['GET'])
def retrieve_tags():
    query_parameters = request.args

    url = query_parameters.get('url')

    query = "SELECT tag FROM tags WHERE"
    to_filter = []

    if url:
        query += ' url=? AND'
        to_filter.append(url)
    if not (url):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)



@app.route('/tags/retrieve_urls', methods=['GET'])
def retrieve_urls():
    query_parameters = request.args

    tag = query_parameters.get('tag')

    query = "SELECT url FROM tags WHERE"
    to_filter = []

    if tag:
        query += ' tag=? AND'
        to_filter.append(tag)
    if not (tag):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)



@app.route('/tags/remove_tags', methods=['DELETE'])
def remove_tags():
    query = "DELETE FROM tags WHERE url = "

    if request.headers['Content-Type'] == 'text/plain':
        query += "'"
        query += request.data.decode()
        query += "';"
    else:
        return "415 Unsupported Media Type ;)"

    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query).fetchall()
    conn.commit()

    return jsonify(results)


@app.route('/tags/add_tags', methods=['POST'])
def add_tags():
    query = 'insert into tags(id, tag, url) values '

    if request.headers['Content-Type'] == 'text/plain':
        query += '('
        query += request.data.decode()
        query += ');'
    else:
        return "415 Unsupported Media Type ;)"

    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query).fetchall()
    conn.commit()

    return jsonify(results)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404



app.run()