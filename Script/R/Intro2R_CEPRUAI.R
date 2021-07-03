# Introducción a la Programación con R
# Autor: Esteban López Ochoa
# Institución: Universidad Adolfo Ibáñez

#------ Parte 0: Cosas que puede hacer R ------

# 1. Puede correr algo y no crear ningun objeto
 1+1

# 2. Puede correr algo y crear un objeto (sin imprimir)

A <- 1+1
B <- "1+1"

# 3. correr algo utilizando una función (palabras seguidas de parentesios redondos)

sum(1,10)

C <- sum(1,18)

sum("A","B")
#------ Parte 1: Explorando R ------

print('Hola mundo!, Mamá mírame!, estoy programando en R,...')

1+1

pi

demo('graphics')

install.packages("leaflet")
library(leaflet)
leaflet::leaflet() %>%
  addTiles() %>%  # Add default OpenStreetMap map tiles
  addMarkers(lng=-71.530294, lat=-33.019305,  popup="Aquí Estamos!")

#------ Parte 2: Creando un objeto ------

dosmasdos <- 2 + 2
dos_mas_dos <- 2 + 2
dos.mas.dos <- 2 + 2
sumita <- 3+4

#------ Parte 2: Funciones, manipulando un objeto ------

dosmasdos

dosmasdos*dosmasdos


#¿Qué clase de objeto es 'dosmasdos'?

class(dosmasdos)

#¿Qué puedo hacer con el objeto 'dosmasdos'?
sum(dos_mas_dos,dosmasdos,3)

sum(c(dos_mas_dos,dosmasdos,3))

#------ Parte 4: Tipos de Objetos ------

a<-1

b<-"Muchachita muchachita la peineta..."

l1<-list(a,b)

m1<-matrix(0,2,2)

sq1<-seq(1,10,1)

sq2<-LETTERS[sq1]

df1<- data.frame(sq1,sq1)

caja<-array(data = 0,dim = c(2,2,3))

#------ Parte 5: Indexación de Objetos ------

A<-c(1836457,2,2,3,4,5,6,7,8,7)

A
A[1]
A[2]
A[-1]
A[1:2]

length(A)

notas<-rnorm(100,5,1.8)

notas[1:5]
notas>4

notas[notas>4]

#------ Parte 5: Manipulación de Objetos ------

class(notas)
class(m1)

length(notas)
length(m1)

dim(m1)
dim(df1)

names(df1)

rm(m1)

ls()



#------ Parte 6: Paquetes ------
#https://www.youtube.com/watch?v=6AOpomu9V6Q

install.packages("leaflet") # instalar 

library(leaflet) # cargar

#usar
leaflet::leaflet() %>%
  addTiles() %>%  # Add default OpenStreetMap map tiles
  addMarkers(lng=-71.530294, lat=-33.019305,  popup="Aquí Estamos!")


library(foreign)


#------ Parte 6: Ayuda ------

?sum
help('sum')

help(package='foreign')

??regression

#------ Parte 7: Practica ------

install.packages("swirl") # instalar 

library(swirl) # cargar

#------ Parte 8: Ejemplo de las potencialidades de R ------
#Fuente: https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto74
install.packages("chilemapas",dependencies = T)
install.packages("leaflet")
install.packages("ggplot2")
install.packages("data.table")
install.packages("sf")
library(chilemapas)
library(leaflet)
library(ggplot2)
library(data.table)
library(sf)

pap<-fread("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto74/paso_a_paso_std.csv")

head(pap)
class(pap$Fecha)
pap$Fecha<-as.Date(pap$Fecha)
unique(pap$Fecha)
unique(pap$codigo_comuna)

ggplot(pap,aes(x=Fecha,y=factor(codigo_comuna),colour=factor(Paso)))+geom_line()+geom_bar(stat = "identity")

class(pap$codigo_comuna)
pap[,codigo_comuna:=as.character(codigo_comuna)]
pap[nchar(codigo_comuna)==4,codigo_comuna:=paste0("0",codigo_comuna)]
mm<-merge(mapa_comunas,pap[Fecha=="2020-12-23",],by="codigo_comuna",all.x=T,sort = F)

names(mm)
head(mm)

mm<-st_sf(mm)
mm$Paso<-factor(mm$Paso,ordered = T)
pasos<-colorFactor(palette = c("red","orange","yellow","blue"),domain = mm$Paso,ordered = F)
leaflet(mm)%>%
  addProviderTiles(provider = providers$CartoDB.Positron)%>%
  addPolygons(color = ~pasos(Paso),weight = 1)%>% 
  addLegend(pal = pasos, values = ~Paso, opacity = 0.7, title = NULL, position = "bottomright")
