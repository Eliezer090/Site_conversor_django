from django.shortcuts import render, redirect
import csv
import json
import os
import mimetypes
import random
import pandas as pd
from django.contrib import messages
from django.contrib.messages import constants
from django.http.response import HttpResponse


def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True


def ajustaJson(jsonInput):
    try:
        if not isinstance(jsonInput, list):
            return [jsonInput]
        return jsonInput
    except ValueError as err:
        return False


def JsontoCsv(request):

    if request.method == 'POST':
        myfile = request.POST.get('json')
        valido = validateJSON(myfile)
        if valido:
            dados = json.loads(myfile)
            json_pronto = ajustaJson(dados)
            if json_pronto:
                BASE_DIR = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__)))
                path_files = BASE_DIR + '/files'
                # Gera nome de arquivo aleatório
                name = str(random.randrange(0, 10000000, step=3))

                name_csv = path_files+'/csv/'+name+'.csv'
                name_json = path_files+'/tmp/'+name+'.json'

                with open(name_json, 'w') as arquivo:
                    json.dump(json_pronto, arquivo)

                df = pd.read_json(name_json)
                print(name_csv)
                # Converte para CSV
                df.to_csv(name_csv, index=None)
                path = open(name_csv, 'r')
                mime_type, _ = mimetypes.guess_type(name_csv)
                response = HttpResponse(path, content_type=mime_type)
                response['Content-Disposition'] = "attachment; filename=%s" % name+'.csv'
                # Remove os arquivos pois não nos interessa
                os.remove(name_json)
                os.remove(name_csv)
                return response
            else:
                messages.add_message(request, constants.ERROR,
                                     f'Arquivo corrompido ou inválido!')
        else:
            pass

    return render(request, 'jsontocsv.html')
