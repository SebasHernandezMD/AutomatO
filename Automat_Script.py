# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 21:42:45 2021

@author: SebastianHdz

Script para automatizar pipeline-analisis de WGS-TB:

En la carpeta debe tener 3 archivos en formato UNIX-UNIOCODE UTF8:
    -> automat_script.py    #Este programa
    -> ls.txt               #Lista de Samples (one per line, no other characters)
    -> pipeline.txt         #Pipeline con Sample en forma de ERRXXX
    -> batch.sh             #Archivo .sh contiene cada pipeline de cada sample
"""
print("AUTOMAT-O: script para batch de pipelines:")
print("\n")
#%%
#Se abre el archivo de lista de muestras como lectura (objeto ls)
#Se convierte el archivo en una lista python (list_raw)
#Se quita "\n" usando rstrip para lista [],  mediante loop.
with open("ls.txt", "r") as ls:
    list_raw=ls.readlines()
    list_samples=[l.rstrip() for l in list_raw]
#%%
#Definimos el patron a cambiar en cada sample (ERRXXX), OJO REVISAR EL PIPELINE ANTES DE INICIAR.
#Abrimos el archivo pipeline y lo dejamos como string (pipeline) para poder leerlo
#Contamos en mumero de ERRXXX que se deben reemplezar en string para conteos finales.
pattern="ERRXXX"
import regex as re
with open("pipeline.txt", "r") as file_handle_1:
    pipeline=file_handle_1.read()
    result_patern=re.findall(pattern, pipeline, flags=0, pos=None, endpos=None, overlapped=True, ignore_unused=False)
    patternCount=result_patern.count(pattern)
#%%
#Con este script, usando list_samples itineramos el reemplazo de cada
#elemento de la lista en el pipeline

#FOR DEBUGGIN ONLY, Copie y pegue el ejemplo de 04-FlowControl, aqui unos samples por si la lista es demasiado grande.
#samples = ['A12', 'A15', '2020-002-CH-CP1', '2020-003-CH-CP2', 'SRR1765879', 'SAMN02402666', 'ERR2206621', 'Sample_01', 'Sample_02']

import regex as re
for each_element in list_samples:
    file_handle_1=open("pipeline.txt", "r+", encoding=('UTF-8'))
    pipeline=file_handle_1.read()
    new_pipeline=re.sub(pattern, each_element, pipeline, count=0)
    with open("batch.sh", "a+", encoding=('UTF-8')) as file_handle_2:
        file_handle_2.write(new_pipeline)
        file_handle_2.close()
#%%
#Comprobaciones.
print("Esta es la lista de muestras a correr:", list_samples)
print("\n")
print("Este es el numero de muestras a procesar:", len(list_samples))
print("Este es el pattern a reemplazar:", pattern)
print("Este es el numero de", pattern, "a reemplezar en pipeline:", patternCount)
import regex as re
with open("batch.sh", "r+", encoding=('UTF-8')) as file_handle_2:
    batch=file_handle_2.read()
    count_samples=re.findall("#SAMPLE:", batch, flags=0, pos=None, endpos=None, overlapped=True, ignore_unused=False)
    print("Este es el numero de muestras agregadas al batch:", len(count_samples))
if len(count_samples) == len(list_samples):
    print("RESULTADO: Todo listo!")
else:
    print("PILAS!! Algo salio mal! Seguramente has pegado varios pipeline seguidos, o el archivo batch.sh no estaba vacio! Borra el contenido de batch.sh y vuelve a intentar!!")
#CLAVE: Revisar que no se haya append varias veces al mismo pipeline.
#%%
#Mensaje al usuario
print("\n")
print("Recuerda para ejecutar el batch.sh:")
print("$ chmod a+x batch.sh    #Activa como ejecutable el archivo.")
print("$ ./batch.sh            #Ejecuta el pipeline.")
