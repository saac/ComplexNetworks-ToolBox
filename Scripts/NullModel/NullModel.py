
import sys

import itertools
import random
import math
import networkx as nx


def gnp_random_graph(p, diccionario, m, directed=False):

  if directed:
      G=nx.DiGraph()
  else:
      G=nx.Graph()
      
  G.add_nodes_from(diccionario)  

  if p<=0:
      return G
  if p>=1:
      return nx.complete_graph(n,create_using=G)  
  
  while(G.number_of_edges() < int(m)):    
    a,b = random.sample(diccionario, 2)
    a = a.strip()
    b = b.strip()
    if (a != b):
      if random.random() < p:
	if ((G.has_edge(diccionario[a],diccionario[b]) == False) and (G.has_edge(diccionario[b],diccionario[a]) == False)):
	    G.add_edge(diccionario[a],diccionario[b])

  return G

##------------------------------------------------------------------------------------------------------------------------------------------##

def gnp_random_graph2(diccionario, m, directed=False):

  if directed:
      G=nx.DiGraph()
  else:
      G=nx.Graph()
      
  G.add_nodes_from(diccionario)  
  n = G.number_of_nodes()
  
  #p = float(float(n)/float(m))
  p = 2*float(m)/float(n*(n-1))
  


  if p<=0:
      return G
  if p>=1:
      return nx.complete_graph(n,create_using=G)  
  

  while(G.number_of_edges() < int(m)):    
    a,b = random.sample(diccionario, 2)
    a = a.strip()
    b = b.strip()

    if (a != b):
      if random.random() < p:
	if ((G.has_edge(a,b) == False) and (G.has_edge(b,a) == False)):
	    G.add_edge(a,b)

  return G
  
 
##############################################################################################################################
 
red = sys.argv[1]
sep = sys.argv[2]
form = sys.argv[3]

m0 = sys.argv[4]
#p0 = sys.argv[5]

#m0 = 0


diccionario = {}
genesDIC = []

izq = []
der = []

name = red.split('.')
output = name[0]+'_NullModel.net'
SALIDA = open(output,"w")


if (sep == "cma"):
  sep = ","
elif (sep == "tab"):
  sep = "\t"
elif (sep == "spa"):
  sep = " "  

interacciones = open(red).readlines()

print "Lineas interacciones (SIF) = ", len(interacciones)

k = 0
tmp="---"
for i in interacciones:
    genes  = i.split(sep)

    a=genes[0].strip()
    b=genes[1].strip()
    c=genes[2].strip()
    
     
    if (form == "nIn"):
      
      if (genes[0].strip() not in genesDIC): genesDIC.append(genes[0].strip())
      if (genes[2].strip() not in genesDIC): genesDIC.append(genes[2].strip())

      
    elif (form == "nnI"):
      
      if (genes[0].strip() not in genesDIC): genesDIC.append(genes[0].strip())
      if (genes[1].strip() not in genesDIC): genesDIC.append(genes[1].strip())

SALIDA.write("%s %s \n" % ("*Vertices", len(genesDIC)))

i = 1
for n in genesDIC:
    n = n.strip()
    diccionario[n] = i
    SALIDA.write('%s "%s" \n' % (i,n))
    i+=1


#G = gnp_random_graph(0.5,diccionario,m0)
G = gnp_random_graph2(diccionario,m0)

output2 = name[0]+'_NullModel.sif'
SIF = open(output2,"w")

print "Nodos = ", G.number_of_nodes()  
print "Edges sin repetidos ni selfloops = ", G.number_of_edges()

SALIDA.write("%s %s \n" % ("*Edges", G.number_of_edges()))
for e in G.edges():
    ed = G.get_edge_data(*e)
    #SALIDA.write("%s %s %s \n" % (e[0],e[1],ed['w']))
    #SALIDA.write("%s %s %s \n" % (e[0],e[1],1))
    SALIDA.write("%s %s %s \n" % (diccionario[e[0]],diccionario[e[1]],1))
    SIF.write("%s\t%s\t%s\n" % (e[0],"pp",e[1]))
 
SALIDA.close()  

#SIF.write("------\n")

if not nx.is_connected(G):
  print nx.number_connected_components(G)
  for g in nx.connected_components(G):
    #print g
    if len(g) <= 2:
      for n in g:
	#SIF.write("%s\t%s\t%s\n" % (n,"pp",n))
	SIF.write("%s\n" % n)
  

SIF.close()  