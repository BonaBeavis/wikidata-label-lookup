#!/usr/bin/env python3

import re
import requests
import sys

input = ''
terms = set()

for line in sys.stdin:
    input += line

for line in input.splitlines(keepends=True):
    # Match RDF terms like wdt:P1001
    regex = r"wdt?n?:[^!$&'()*+,;=\s?]+"
    match = re.findall(regex, line)
    terms.update(match)

def replace_ns(term):
    return "wd:" + term.split(":")[1]

terms = map(replace_ns, terms)
terms = ' '.join(terms)
query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wdtn: <http://www.wikidata.org/prop/direct-normalized/>

SELECT DISTINCT ?term  (SAMPLE(?l) AS ?label)  WHERE {
  VALUES ?term { """ + terms + """}
  ?term rdfs:label ?l .
  FILTER (langMatches( lang(?l), "EN" ) )
}
GROUP BY ?term
"""
url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
data = requests.get(url, params={'query': query, 'format': 'json'}).json()
results = data['results']['bindings']
labels = dict()

for result in results:
    term = result['term']['value']
    term = term.split('/')[-1]
    labels[term] = result['label']['value']

def replace_labels(match):
    # Labels are all inside the wd namespace
    noNsTerm = match.group().split(":")[1]
    return '<' + labels[noNsTerm] + '>'

for line in input.splitlines(keepends=False):
    # Match RDF terms like wdt:P1001
    regex = r"wdt?n?:[^!$&'()*+,;=\s?]+"
    match = re.sub(regex, replace_labels, line)
    print(match)
