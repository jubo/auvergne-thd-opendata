import os
from flask import Flask

app = Flask(__name__)

@app.route('/info')
def info():
    return 'Ce site a pour but de compiler les informations disponibles
sur le site auvergne haut débit sous un format exploitable.'

@app.route('/phase1/all')
def get_phase1_all():
    return 'phase 1 tout'

@app.route('/phase2/all')
def get_phase2_all():
    return 'phase 2 tout'
