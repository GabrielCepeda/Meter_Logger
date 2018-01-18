#!/usr/bin/env python
#import pyhs2 as hive
from impala.dbapi import connect
import getpass
import numpy as np
import itertools
from sklearn import tree
import pydotplus

#CONFIGURACION
#Parametros de conexion para pyhs2
DEFAULT_DB = 'analizadorlogsdb'
DEFAULT_SERVER = '192.168.1.108'
DEFAULT_PORT = 10001

#solicitud de datos de entrada
usuario = raw_input('Ingresar Usuario:')
passwd = getpass.getpass()
num=2 #por defecto la cantidad de errores minima seran 2.
while True:
    try:
        num = input('Ingrese Tipos de Error para asignar a clases de arbol:2-4-5:  ')
        if num == 5 or num ==2 or num ==4:
            break
        else:
            print 'opcion errada_ 2-4-5'
    except NameError:
        print 'Dato ingresado no es un numero por favor intente nuevamente.'

#conexion a Hive
con = connect(host=DEFAULT_SERVER,port=DEFAULT_PORT,database=DEFAULT_DB,user=usuario,password=passwd,auth_mechanism='PLAIN')

#queries
query='select * from errores_clasificacion'#Traemos los resultados de la tabla errores clasificacion

#cursor que abre la conexion
cur= con.cursor()

#ejecucion de la query
cur.execute(query)

#tratamiento del texto de la tabla para convertirlo en arrays
x=[]
for i in cur.fetch():	
	linea=str(i).split('of approx.')#separacion del texto en 2
	x1=linea[0][58:len(linea[0])]#se extrae el valor de bloques leidos correctamente
	x1=int(x1)
	x2=linea[1][0:(len(linea[1])-42)]#se extrae el valor total de Bloques
	x2=int(x2)
	temp=[x1,x2]#se preparan los atributos bloques leidos y total de bloques para agregarlos al array de datos de entrenamiento.
	x.append(temp)#los atributos se agregan al array de entrenamiento

print 'vector de entrenamiento condatos de bloques correctos y totales'
print x

#Se clasificaran en 4 posibles clases: 50 en cada tipo.
y=[]
#for i in range(1,5):
#	y1=i*np.ones((1,50))# se crea el vector y de objetivos con cada posible solucion
#	y=np.append(y,y1)

for i in range(1,num+1):
	y1=i*np.ones((1,200/num))# se crea el vector y de objetivos con cada posible solucion restringidos a que sea un numero primo de 200 por la muestra
	y=np.append(y,y1)
print 'vector de objetivos con las clases:'
print y

# con los vectores de entrenamiento y de objetivos se entrena el arbol de decision
clasificador=tree.DecisionTreeClassifier()
clasificador=clasificador.fit(x,y)

print 'Informacion del clasificador:'
print clasificador
print 'Generacion de archivo con grafica del arbol generado para la muestra'

dot_data = tree.export_graphviz(clasificador, out_file=None) 
graph = pydotplus.graph_from_dot_data(dot_data) 
graph.write_pdf("tipomantenimiento.pdf") # se exporta el arbol de clasificacion

#Con el arbol de decision para clasificar ajustado ahora se puede predecir la clase de cada combinacion
prediccion=clasificador.predict(x)

#Con la prediccion se retorna el resultado a Hive en un objeto generando el HQL
sentenciaborrado ='DROP TABLE IF EXISTS resultado_clasificacion_py'# Borrado de la tabla para limpiar resultados anteriores
sentenciacreacion='CREATE TABLE resultado_clasificacion_py(bloques_leidos int, bloques_totales int,clase_error int) STORED AS SEQUENCEFILE' #recreacion de la tabla.

#Generacion de Insert con los resultados
sentenciainsercion='INSERT INTO TABLE resultado_clasificacion_py VALUES ' 
cur.execute(sentenciaborrado)
cur.execute(sentenciacreacion)
for k in range(0,len(x)):
	if k !=len(x)-1:
		sentenciainsercion +='(' + str(x[k][0]) + ',' + str(x[k][1]) + ',' + str(prediccion[k]) + '),'
  	else:
		sentenciainsercion +='(' + str(x[k][0]) + ',' + str(x[k][1]) + ',' + str(prediccion[k]) + ')'

#print sentenciainsercion
cur.execute(sentenciainsercion)#cargamos los valores en hive
print 'Insercion Terminada Consultar en Hive :http://192.165.1.108:8080/#/main/views/HIVE/1.0.0/AUTO_HIVE_INSTANCE'





