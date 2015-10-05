# -*- coding:utf-8
import os
import flask
from flask import Flask
from flask import request
from flask import make_response
import xml.etree.ElementTree as xml
import re

app = Flask(__name__)

class AuvergneTHDParser:
    """
    Cette classe parse et construit une liste de dictionnaires contenant
    les informations du deploiement THD en Auvergne

    Les fichiers kml ont été extraits des url suivantes 

    wget -O ftth-phase1.kml http://www.auvergnetreshautdebit.fr/wp-content/themes/athd/kml/phase2/ftth-phase2.kml?20151002100409
    wget -O ftth-phase2.kml http://www.auvergnetreshautdebit.fr/wp-content/themes/athd/kml/ftth.kml?20151002100409

    """
    def __init__(self):
        self.keys = []
        self.keys.append("DATES")
        self.deploiements = self.make_data_from_kml(['ftth-phase1.kml', 'ftth-phase2.kml'])

    def make_data_from_kml(self, filename_list):
        """
        Construit une liste d'objets deploiement a partir du kml du site
        auvergne haut debit
        """
        ret = []
        for filename in filename_list:
            root = xml.parse(filename).getroot()
            for node in root.findall('Document/Folder/Placemark'):
                deploiement = dict()
                for subnode in node.findall('ExtendedData/SchemaData/SimpleData'):
                    key = subnode.attrib['name']
                    if not key in self.keys:
                        self.keys.append(key)
                    deploiement[key] = subnode.text
                
                # dates de depoiement
                name = node.findall("name")[0].text
                deploiement["DATES"] = name.split('de')[2]
                ret.append(deploiement)
        return ret

parser = AuvergneTHDParser()

def request_wants_json():
    """
    La requête courante exige du json en retour.
    """
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return (best == 'application/json' \
           and request.accept_mimetypes[best] > \
           request.accept_mimetypes['text/html']) or \
           request.args.get('format') == 'json'

@app.route('/search/')
def search():
    """
    Recherche les items dont la clé / valeur correspond 
    return : csv par défaut, json si demandé

    QueryString ?key=<key>&val=<val> 
    key -- champ de recherche
    val -- valeur contenue    
    """
    from datetime import datetime
    key = request.args.get('key')
    val = request.args.get('val')
    filename = 'result_%s.csv' % datetime.now().strftime("%A_%d_%B_%Y_%I_%M")
        
    search_deploiements = parser.deploiements
    if(key and val):
        search_deploiements = [item for item in parser.deploiements if key in item.keys() and  val in item[key]]
    if(request_wants_json()):
#        return get_json_from_list_dict(search_deploiements)
        ret = flask.jsonify(results = search_deploiements)
        ret.headers['Content-Type'] = 'application/json; charset=utf-8'
        return ret
    else:
        return get_csv_from_list_dict(filename, search_deploiements)


def get_csv_from_list_dict(filename, list_dict):
    """
    Convertit une liste de liste en csv et prépare la réponse en fonction
    a partir de la liste des clés présente dans les SimpleData
    """
    if(len(parser.deploiements) > 0):
        keys = parser.keys
        grid = []
        grid.append(keys)
        for item in list_dict:
            row = []
            for key in keys:
                if key in item.keys():
                    row.append(item[key])
                else:
                    row.append('')
            grid.append(row)
   
    csv = '\r\n'.join(','.join(row) for row in grid)
    output = make_response(csv)
    output.headers["Content-Disposition"] = "attachment;filename=%s"%filename
    output.headers["Content-type"] = "text/csv"
    return output

def get_json_from_list_dict(list_dict):
    """
    Serialise en json
    """
    import json
    json_content = json.dumps(list_dict, encoding='utf-8')
    output = make_response(json_content)
    output.headers["Content-type"] = "text/json"
    return output

#app.run(debug=True)
#print get_phase1_all()
