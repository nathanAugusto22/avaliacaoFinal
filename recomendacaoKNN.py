# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 20:37:35 2018

@author: Nathanael e Arlan
"""
import pandas as pd
import numpy as np
from math import sqrt

#importando dados
colunas = ['usuario_id', 'filme_id', 'nota']
avaliacoes = pd.read_csv('u.data', sep='\t', names=colunas, usecols=range(3),
                      encoding='latin-1')

propriedadesFilme = avaliacoes.groupby('filme_id').agg({'nota': 
 [np.size, np.mean]}) 
propriedadesFilme.head() 

#calculando media de popularidade para cada filme
qtdeFilmesAvaliados = pd.DataFrame(propriedadesFilme['nota']['size']) 
qtdeFilmesAvaliadosNormalizados = qtdeFilmesAvaliados.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x))) 
qtdeFilmesAvaliadosNormalizados.head() 

infoFilmes = {} 
 
#percorrendo o arquivo e guardando num dict as informações
with open('u.item') as f: 
    temp = '' 
    for linha in f: 
        campos = linha.rstrip('\n').split('|') 
        filmeID = int(campos[0]) 
        nome = campos[1] 
        genero = campos[5:25] 
        genero = map(int, genero) 
        infoFilmes[filmeID] = (nome, genero,      
        qtdeFilmesAvaliadosNormalizados.loc[filmeID].get('size'),propriedadesFilme.loc[filmeID].nota.get('mean'))
        
# exemplo de retorno
infoFilmes[1] 

      

from scipy import spatial 
          
 # retorna a distancia entre cada item baseado no genero e polularidade, tendo como métrica a distancia Coseno 
def ComputaDistanciaCoseno(a, b): 
    generoA = a[1]
    
    generoB = b[1] 
    
    distanciaGenero = spatial.distance.cosine(generoA, generoB) 
    popularidadeA = a[2] 
    popularidadeB = b[2] 
    distanciaPopularidade = abs(popularidadeA - popularidadeB) 
    return distanciaGenero + distanciaPopularidade 

  # retorna a distancia entre cada item baseado no genero e polularidade, tendo como base a distancia Euclidiana
def ComputaDistanciaEuclidiana(a, b):
    
    generoA = a[3]
    generoB = b[3] 
    
    distanciaGenero = spatial.distance.euclidean(generoA, generoB)
    popularidadeA = a[2] 
    popularidadeB = b[2] 
    distanciaPopularidade = abs(popularidadeA - popularidadeB) 
    return distanciaGenero + distanciaPopularidade 
     
ComputaDistanciaCoseno(infoFilmes[2], infoFilmes[4]) 
ComputaDistanciaEuclidiana(infoFilmes[2], infoFilmes[4])


import operator 
 # retorna todas as recomendacoes baseado nas menores distancias entre todos os filmes
def getVizinhos(filmeID, K): 
    distancias = [] 
    for filme in infoFilmes: 
        if (filme != filmeID): 
            distancia = ComputaDistanciaCoseno(infoFilmes[filmeID], 
 infoFilmes[filme]) 
            distancias.append((filme, distancia)) 
    distancias.sort(key=operator.itemgetter(1)) 
    vizinho = [] 
    for x in range(K): 
        vizinho.append(distancias[x][0]) 
    return vizinho 
 
#definindo o k ( numero base para recomendações )
K = 10  
notaRecomendada = 0 
recomendacoes = getVizinhos(1, K) 
# mostrando lista de 10 recomendações
for recomendacao in recomendacoes: 
    notaRecomendada += infoFilmes[recomendacao][3] 
    print(infoFilmes[recomendacao][0] + " " + str(infoFilmes[recomendacao][3]))
    notaRecomendada /= float(K)

    # grafico com a visão geral das notas
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set(style="whitegrid", color_codes=True)
    %matplotlib inline
    sns.factorplot(x="filme_id", y="nota", data=avaliacoes, kind="bar");
    

    
    
    
    
    
    
    
    

    
    