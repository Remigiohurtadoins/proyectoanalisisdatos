#CONTROLADOR
from rest_framework import generics #para microservicio
from apiAnalisis import models
from apiAnalisis import serializers
from rest_framework import filters
from django.http import HttpResponse
from django.shortcuts import render
from apiAnalisis.Logica.modeloAnalisis import modeloAnalisis#para utilizar modelo
from apiAnalisis.Logica.Autenticacion import Autenticacion as auten
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import JsonResponse

import json
import pandas as pd
import csv

# Create your views here.
class ListLibro(generics.ListCreateAPIView):
    """
    retrieve:
        Retorna una instancia libro.

    list:
        Retorna todos los libros, ordenados por los más recientes.

    create:
        Crea un nuevo libro.

    delete:
        Elimina un libro existente.

    partial_update:
        Actualiza uno o más campos de un libro existente.

    update:
        Actualiza un libro.
    """
    queryset = models.Libro.objects.all()
    serializer_class = serializers.LibroSerializer

class DetailLibro(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Libro.objects.all()
    serializer_class = serializers.LibroSerializer

class ListCliente(generics.ListCreateAPIView):
    queryset = models.Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

class DetailCliente(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

class CedulaClientesAPIView(generics.ListCreateAPIView):
    search_fields = ['cedula']
    filter_backends = (filters.SearchFilter,)
    queryset = models.Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

class TipoClientesAPIView(generics.ListCreateAPIView):
    search_fields = ['tipoCliente']
    filter_backends = (filters.SearchFilter,)
    queryset = models.Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

class ClientesAPIView(generics.ListCreateAPIView):
    filter_backends = (DynamicSearchFilter,)
    queryset = models.Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

class ListGrafica(generics.ListCreateAPIView):
    queryset = models.Grafica.objects.all()
    serializer_class = serializers.GraficaSerializer

class DetailGrafica(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Grafica.objects.all()
    serializer_class = serializers.GraficaSerializer

class Autenticacion():

    def singIn(request):

        return render(request, "signIn.html")

    def postsign(request):
        email=request.POST.get('email')
        passw = request.POST.get("pass")
        print("ds:",passw)
        #Con Firebase
        """
        try:
            #user = auth.sign_in_with_email_and_password(email,passw)
        except:
            mensaje = "Credenciales inválidas"
            return render(request,"signIn.html",{"msg":mensaje})
        """
        mensaje = auten.sign_in_with_email_and_password(str(email),str(passw))
        print(mensaje)
        if not(mensaje):
            mensaje = "Credenciales inválidas"
            return render(request,"signIn.html",{"msg":mensaje})
        else:
            return render(request, "welcome.html",{"e":email})

class Clasificacion():
    def mostrarInterfazPredecir(request):
        return render(request, "interfazPredecir.html")
    def mostrarInterfazBuscar(request):
        return render(request, "interfazBuscar.html")
    def mostrarInterfazPredecirConEstilo(request):
        return render(request, "main.html")

    def predecirTipoCliente(request):
        try:
            Dni = int(request.POST.get('Dni'))
        except:
            mensaje = "El DNI no tiene el formato adecuado"
            return render(request,"signIn.html",{"msg":mensaje})
        print(type(Dni))
        #resul=modeloAnalisis.suma(num1=2,num2=5)
        resul=modeloAnalisis.predecirTipoCliente(modeloAnalisis,Dni)
        print(resul)
        return render(request, "resultado.html",{"e":resul})

    #@csrf_exempt
    @xframe_options_exempt
    def predecirTipoCliente2(request):
        #try:
        #    Dni = int(request.POST.get('Dni'))
        #    print("LLego",Dni)
        #except:
        #    mensaje = "El DNI no tiene el formato adecuado"
            #return render(request,"signIn.html",{"msg":mensaje})
        #print(type(Dni))
        #resul=modeloAnalisis.suma(num1=2,num2=5)
        #resul=modeloAnalisis.predecirTipoCliente(modeloAnalisis,Dni)
        #print(resul)
        data = [{'Nombre': 'Remi', 'email': 'remi@example.org'},
            {'Nombre': 'JP', 'email': 'jp@example.org'}]
        #response = JsonResponse(
        #    data
        #)

        return JsonResponse(data, safe=False)

        #response["Access-Control-Allow-Origin"] = "*"
        #response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        #response["Access-Control-Max-Age"] = "1000"
        #response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        #return response
        #return render(request, "resultado.html",{"e":resul})
        #return HttpResponse(resul)

    def buscarCliente(request):
        try:
            Dni = int(request.POST.get('Dni'))
            response = requests.get('http://127.0.0.1:8000/apiAnalisis/clientesFiltroDinamico/?search='+str(Dni)+'&search_fields=cedula')
            cliente = response.json()
            print(cliente)
            if len(cliente)==0:
                mensaje = "El cliente no existe"
                return render(request,"interfazBuscar.html",{"msg":mensaje})
        except:
            mensaje = "El DNI no tiene el formato adecuado"
            return render(request,"interfazBuscar.html",{"msg":mensaje})
        return render(request, 'datosCliente.html', {
                'edad': int(cliente[0]['edad']),
                'tipoCliente': int(cliente[0]['tipoCliente'])})

    #def buscarClienteConPOST(request):
    #    received_json_data=json.loads(request.body)

        #desde java
    #    url = "http://localhost:8000"
    #    data = {'data':[{'key1':'val1'}, {'key2':'val2'}]}
    #    headers = {'content-type': 'application/json'}
    #    r=requests.post(url, data=json.dumps(data), headers=headers)
    #    r.text

    #def save_events_json(request):
    #    if request.is_ajax():
    #        if request.method == 'POST':
    #            print 'Raw Data: "%s"' % request.body   
    #    return HttpResponse("OK")

   
