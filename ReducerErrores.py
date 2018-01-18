#!/usr/bin/env python
import os
import sys
from operator import itemgetter

filas = None
lonPalabras= 0
linea=''
campos=0

# se recibe el input de mappere
for line in sys.stdin:
	
	linea=line.strip('\t')
	filas = linea.split('=>')	
	campos = len(filas)
	if campos>=2:
		print '%s\t%s\t%s' % (filas[0],filas[1])
		
