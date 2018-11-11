import sys
import requests
from bs4 import BeautifulSoup
import time
import csv

url_main = "https://carros.tucarro.com.co/"

def scraping_page(url,pag):
    lOk=True
    page = requests.get(url)
    if page.status_code == 200 : ## peticion exitosa
        soup = BeautifulSoup(page.content,"html.parser")
        if pag == 1: # Primera página
            archivocsv=open("vehiculos.csv", "w")
            encabezados = ['descripcion', 'modelo_y_km', 'precio', 'ubicacion']
            datos = csv.DictWriter(archivocsv, fieldnames=encabezados)
            datos.writeheader()
        else:
            archivocsv=open("vehiculos.csv", "a")
        for vehiculo in soup.find_all(class_="item__info-link item__js-link "):
            precio = vehiculo.find('span', {'class' : 'price__fraction'}).getText()
            modelo_y_km = vehiculo.find('div', {'class' : 'item__attrs'}).getText()
            descripcion = vehiculo.find('span', {'class' : 'main-title'}).getText()
            ubicacion = vehiculo.find('div', {'class' : 'item__location'}).getText()
            csvwriter = csv.writer(archivocsv, delimiter=",", lineterminator="\n")
            csvwriter.writerow([descripcion.strip(), modelo_y_km.strip(), precio.strip(), ubicacion.strip()])
    else:
        lOk=False
        print("Fallo el proceso, Error al conectar con la web")
    return lOk

def parameters_ok(npara):
    lOk=True
    if  1 < npara <= 4 : ## evaluando numero de argumentos
        try:
            year_ini=int(sys.argv[1])
            year_fin=int(sys.argv[2])
            marca=""
            if year_fin > year_ini:
                if npara == 4:
                    ## incluye marca
                    marca=sys.argv[3]
                    marca = marca.lower()+ '/'
                url1 = url_main + marca +str(year_ini)+'-'+str(year_fin)+"/_OrderId_PRICE"
                url2 = url_main + marca +str(year_ini)+'-'+str(year_fin)+"/_Desde_49_OrderId_PRICE"
                url3 = url_main + marca +str(year_ini)+'-'+str(year_fin)+"/_Desde_97_OrderId_PRICE"
                print("Scraping page 1")
                if scraping_page(url1,1):
                    time.sleep(10)
                    print("Scraping page 2")
                    if scraping_page(url2,2):
                        time.sleep(10)
                        print("Scraping page 3")
                        if not scraping_page(url3,3):
                            lOk=False
                            print("ERROR: Fallo el proceso en la tercera página")
                    else:
                        lOk=False
                        print("ERROR: Fallo el proceso en la segunda página")
                else:
                    lOk=False
                    print("ERROR: Fallo el proceso en la primera página")
            else:
                lOk=False
                print("ERROR: Año inicial es mayor que el año final")
        except:
             lOk=False
             print("ERROR: parametros incorrectos\n Ej: python sctucarro.py 2000 2018 mazda")
    else:
        lOk=False
        print("ERROR: Invalido número de parámetros")
    return lOk



if parameters_ok(len(sys.argv)):
    print("*** HA FINALIZADO EL PROCESO EXITOSAMENTE! ***")
