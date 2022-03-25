import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON
from flask import Flask, render_template, request
app = Flask(__name__)

g = rdflib.Graph()
g.parse("azot_dongusu.owl", format='ttl')
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

@app.route('/main',methods=['GET'])
def get_main():
    return render_template('index.html',output=None)

@app.route('/main', methods=['POST'])
def post_main():
    query = request.form["query"]
    qres = g.query(query)
    output = " ".join([str(i) for i in qres])
    return render_template('index.html',output=output)

@app.route('/dbpedia',methods=['GET'])
def getdbpedia():
    return render_template('index.html',dbpedia_output=None)

@app.route('/dbpedia', methods=['POST'])
def postdbpedia():
    query = request.form["dbpedia_output"]
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results =sparql.query().convert()
    output = ""
    for result in results["results"]["bindings"]:
        output += result["comment"]["value"] + " \n "
    return render_template('index.html',dbpedia_output=output)
