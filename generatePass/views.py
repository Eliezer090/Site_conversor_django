from django.shortcuts import render, redirect
from django.http import HttpResponse
import string
import random


def genpass(request):
    if request.method == "POST":
        tamanho_senha = request.POST.get('tamanho_senha')
        incluir = request.POST.get('incluir')

        letras = string.ascii_letters  # Minuscula e maiuscula
        digitos = string.digits
        caracteres = '!@$#%&*(()_+.'

        geral = letras+digitos+caracteres
        # Join junta os valores, pois o choives retorna uma lista
        senha = "".join(random.choices(geral, k=int(tamanho_senha)))
        senha += incluir
        return render(request, 'generatepass.html', {'retorno': senha, 'tamanho_senha': tamanho_senha, 'incluir': incluir})
    return render(request, 'generatepass.html', {'tamanho_senha': 10})
