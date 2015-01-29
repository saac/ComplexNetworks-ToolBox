#!/usr/bin/env Rscript


##########Para instalar paquetes##########

#biocLite("limma")
#biocLite("affy")
#biocLite("gplots")
#biocLite(c("AnnotationDbi"))

######Para evitar probleas de instalación
#source("http://bioconductor.org/biocLite.R")
#pkgs <- rownames(installed.packages())
#biocLite(pkgs, type="source")


library(affy)
library(limma,gplots)
datos = ReadAffy()

##Como están organizados los datos?
#sampleNames(datos)

###### Grafica sin normalizar  
pdf("Graphs.pdf2",width=7,height=5)
mycolors = rep(c("blue","red","green", "magenta"), each = 2)
hist(datos, col=mycolors, main="Distribuci ́on de Datos Crudos")
boxplot(datos,col=mycolors, main="Distribuci ́ondeDatosCrudos")
 dev.off()

###############################
######Normalización############
###############################

esetbg <- expresso(datos, bgcorrect.method="mas",normalize.method="loess", pmcorrect.method="pmonly",summary.method="medianpolish")

pdf("Grafica_normalizada_por_expresso_mas.pdf",width=7,height=5)
mycolors = rep(c("blue","red","green", "magenta"), each = 2)
plotDensity(exprs(esetbg), col=mycolors, main="Despues de normalizar")
boxplot(exprs(esetbg),col=mycolors, main="DistribuciondeDatosCrudos")
dev.off()

##########Sin correccion de background ############
#
# eset <- expresso(datos, bgcorrect.method="none",normalize.method="loess", pmcorrect.method="pmonly",summary.method="medianpolish") # *
# 
# #Para graficar la normalizacion
# pdf("Grafica_normalizada_por_expresso_none.pdf",width=7,height=5)
# mycolors = rep(c("blue","red","green", "magenta"), each = 2)
# plotDensity(exprs(eset), col=mycolors, main="Despues de normalizar")
# boxplot(exprs(eset),col=mycolors, main="DistribuciondeDatosCrudos")
# dev.off()
#
#############################################

nivelesexp = data.frame(exprs(esetbg))
write.csv(nivelesexp,file='DatosNormalizados.csv')
