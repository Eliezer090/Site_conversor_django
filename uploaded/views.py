from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
import pandas as pd
import mimetypes
import random
import json
from django.contrib import messages
from django.contrib.messages import constants
from django.http.response import HttpResponse


def validateJSON(jsonData):
    try:
        return json.loads(jsonData.read().decode())
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


def uploaded(request):
    try:

        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            valido = validateJSON(myfile)
            if myfile.content_type == 'application/json' and valido:
                # json_input = json.loads(myfile.read().decode())
                json_pronto = ajustaJson(valido)
                if json_pronto:
                    # Pega diretorio base
                    BASE_DIR = os.path.dirname(
                        os.path.dirname(os.path.abspath(__file__)))
                    path_files = BASE_DIR + '/files'
                    # fs = FileSystemStorage()
                    # Gera nome de arquivo aleatório
                    name = str(random.randrange(0, 10000000, step=3)) + \
                        myfile.name.replace('.json', '')
                    name_csv = path_files+'/csv/'+name+'.csv'
                    name_json = path_files+'/tmp/'+name+'.json'
                    # Salva o arquivo
                    # filename = fs.save(BASE_DIR+'/files/tmp/'+name+'.json', json_pronto)
                    with open(name_json, 'w') as arquivo:
                        json.dump(json_pronto, arquivo)

                    df = pd.read_json(name_json, typ="frame")
                    # Converte para CSV
                    df.to_csv(name_csv, index=None)

                    # Download do arquivo convertido
                    with open(name_csv, 'r') as path:
                        # path = open(name_csv, 'r')
                        mime_type, _ = mimetypes.guess_type(name_csv)
                        response = HttpResponse(
                            path, content_type=mime_type)
                        response['Content-Disposition'] = "attachment; filename=%s" % name+'.csv'
                        # Remove os arquivos pois não nos interessa
                        os.remove(name_json)
                        os.remove(name_csv)
                        return response
                else:
                    messages.add_message(request, constants.ERROR,
                                         f'Arquivo corrompido ou inválido!')
            else:
                if valido:
                    messages.add_message(request, constants.ERROR,
                                         f'Arquivo com a extensão {myfile.content_type} não suportado!')
                else:
                    messages.add_message(request, constants.ERROR,
                                         f'Arquivo corrompido ou inválido!')

        return render(request, 'uploaded.html')

    except Exception as e:

        if e.args[0] == 'myfile':
            messages.add_message(request, constants.ERROR,
                                 'Selecione um arquivo json')

        return render(request, 'uploaded.html')


"""
dados = json.loads(myfile.read().decode())
with open('files/csv/clientes2.csv', 'w') as arquivo:
    # Definindo qual vai ser a extrutura do nosso arquivo csv
    escreve = csv.writer(
        arquivo,
        delimiter=',',  # Qual é a nossa quebra
        quotechar='"',
        # Coloca aspas nos valores ou seja: "luiz", "otavio","miranha", fica mais seguro para trabalhar
        quoting=csv.QUOTE_ALL
    )
    print(dados.values())
    # Preenche cabeçalho
    escreve.writerow(
        list(dados.keys())
    )
    escreve.writerow(
        dados.values()
    )
    # Preenche dados
    for dado in dados.values():
        print(dado)
"""
