import os
import requests
import csv
import time
from bs4 import BeautifulSoup

def extraer(catalogo):   
#Extrae la información a en formato CSV
    currentDir="D:/UOC/Tipologia y ciclo de vida de los datos/Practica1/"
    filename = "mediamarkt.csv"
    filePath = os.path.join(currentDir, filename)
    with open(filePath, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for productos_ in catalogo:
            writer.writerow(productos_) 
    return
def TratarDatos(Url):
    #Obtener los datos de la categoria
    print(Url)
    catalogo=[]
    response= requests.get(Url)
    soup = BeautifulSoup(response.text,"html.parser")
    for row in soup.findAll('li'):
       for row2 in row.findAll('figure'):
          for rows in row.findAll('img'):
             img=rows.get('data-original')
             if(len(str(img))>5):
                  load_requests("https:"+str(img))
                  img =img[img.rfind('/'):]
       for row2 in row.findAll('script'):
          x=row2.get_text()
          if(x.startswith( 'var' )):
             name=x[x.index('"name":')+8:x.index('"',x.index('"name":')+8)]
             id=x[x.index('"id":')+6:x.index('"',x.index('"id":')+6)]
             price=x[x.index('"price":')+9:x.index('"',x.index('"price":')+9)]
             brand=x[x.index('"brand":')+9:x.index('"',x.index('"brand":')+9)]
             ean=x[x.index('"ean":')+7:x.index('"',x.index('"ean":')+7)]  
             plataforma=x[x.index('"dimension11":')+15:x.index('"',x.index('"dimension11":')+15)]
             name=name.replace(brand,'')
             producto=[name,id,price,brand,ean,plataforma,img]
             catalogo.append(producto)
    return catalogo
def iteraciones(url_temp):
    #Obtener el número de páginas de la categoria
    pagina=1
    response= requests.get(url_temp)
    soup = BeautifulSoup(response.text,"html.parser")
    for row in soup.findAll('ul',{'pagination'}):
       for rows in row.findAll('li'):
          comparar=(int)(rows.get('data-value'))
          if(pagina < comparar):
              pagina=comparar
    return pagina
def Categorias(Url):
    #Obtener las categorias que se tienen que revisar
    catalogo=[]
    response= requests.get(Url)
    soup = BeautifulSoup(response.text,"html.parser")
    for row in soup.findAll('ul',{'categories-flat-descendants'}):
       for rows in row.findAll('a'):
          print(rows)
          catalogo.append(rows.get('href'))
    return catalogo
def load_requests(source):
    currentDir="D:/UOC/Tipologia y ciclo de vida de los datos/Practica1/img/"
    r=requests.get(source,stream=True)
    a=source.split('/')
    ruta=currentDir+a[len(a)-1]+".png"
    output= open(ruta,"wb")
    for chunk in r :
       output.write(chunk)
    output.close()
#url="https://www.mediamarkt.es/es/category/_nintendo-switch-702299.html?searchParams=&sort=&view=&page="
raiz="https://www.mediamarkt.es"
sufijo="?page="
url="https://www.mediamarkt.es/es/category/_juegos-701342.html"
catalogo=[]
t0=time.time()
categorias=Categorias(url)
response_delay=time.time()-t0
for ruta in categorias:
    url_temp=raiz + ruta + sufijo 
    for i in range(iteraciones(url_temp)):
       catalogo=catalogo+(TratarDatos(url_temp+str(i+1)))
       time.sleep(2*response_delay)
extraer(catalogo)
