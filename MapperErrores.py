#!/usr/bin/env python
import os
import sys

longFiltro=0
#Filtros de texto predefinidos para obtener el texto que nos interesa del archivo
filtro=[]
filtro.append("error")
filtro.append("Error")
filtro.append("fail")
filtro.append("Fail")
filtro.append("Connecting")
filtro.append("Contacting")
filtro.append("Cannot")
filtro.append("TimeOut")
filtro.append("timeout")
filtro.append("Time1:")
filtro.append("Time2:")
#Longitud del Array de filtros
longFiltro=len(filtro)
linea =''
for line in sys.stdin:	
	linea=line.strip('\t')#se limpia el archivo de entrada de tabs iniciales
	#para cada filtro se separa cada caracter y se busca su coincidencia, si existe se agrega para pasar a reduce
	for i in range(0,longFiltro):
		if filtro[i] in linea.split():
				print linea