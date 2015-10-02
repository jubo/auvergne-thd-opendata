# -*- coding:utf-8
import os
from flask import Flask
from flask import make_response
import xml.etree.ElementTree as xml

app = Flask(__name__)

class AuvergneTHDParser:
    """
    Cette classe parse et construit une liste de dictionnaires contenant
    les informations du deploiement THD en Auvergne
    """
    def __init__(self):
        self.deploiements = self.make_data_from_kml(['ftth-phase1.kml', 'ftth-phase2.kml'])

    def make_data_from_kml(self, filename_list):
        """
        Construit une liste d'objets deploiement a partir du kml du site
        auvergne haut debit
        """
        ret = []
        for filename in filename_list:
            root = xml.parse(filename).getroot()
            for node in root.findall('Document/Folder/Placemark/ExtendedData/SchemaData'):
                deploiement = dict()
                for subnode in node.findall('SimpleData'):
                    deploiement[subnode.attrib['name']] = subnode.text
                ret.append(deploiement)
        return ret

parser = AuvergneTHDParser()

@app.route('/info')
def info():    
    return 'Ce site a pour but de compiler les informations disponibles sur le site auvergne haut débit sous un format exploitable.'

@app.route('/phase1/all')
def get_phase1_all():
    d = [item.values() for item in parser.deploiements if item['ZONE'] == 'Phase 1']
    return getcsvfromdict('phase1.csv', d)

@app.route('/phase2/all')
def get_phase2_all():
    d = [item.values() for item in parser.deploiements if item['ZONE'] == 'Phase 2']
    return getcsvfromdict('phase2.csv', d)

def getcsvfromdict(filename, d):
    csv = '\r\n'.join(','.join(row) for row in d)
    output = make_response(csv)
    output.headers["Content-Disposition"] = "attachment;filename=%s"%filename
    output.headers["Content-type"] = "text/csv"
    return output

app.run(debug=True)

#print get_phase1_all()
