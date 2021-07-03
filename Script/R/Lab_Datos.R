##############################################
##        Laboratorio Data Wrangling        ##
##    Escuela de Verano CEPR-Goblab 2021    ##
##          Autor: Javier Fernández         ## 
## contacto: https://jfernandez.netlify.app ##
##############################################

# dplyr
#####

### 1.Setup

## Cargamos paquetes

library(dplyr)
library(readxl)

## Abrimos la base de datos

ive<-read_xlsx(path ="DATOS_IVE_2018_2020.xlsx")

## 2. Exploración

head(ive)
View(ive) # Se activa este mismo comando cuando hago click al objeto en el environment
names(ive)
na
## 3. Pre-procesamiento

#a. Seleccionar variables

ive <- ive %>% 
  select(-starts_with("PSI"),-starts_with("ASIST"),-starts_with("DUPLA"),-starts_with("VISITA"))
## Aquí esta deseleccionando las variables, debido al signo negativo.

#b. Cambiar clase de variables

ive<-ive %>% mutate(edad=as.integer(`edad de la mujer`))
ive<-ive %>% mutate(edadgest=as.intedfger(`edad gestacional concurrencia`))

## 4. Operaciones sencillas

#a. Calcular promedio de:

# edad

ive %>% summarise(mean(edad,na.rm=TRUE)) 

# edad gestacional

ive %>% summarise(mean(edadgest,na.rm=TRUE))

#b. Calcular número de casos:

# Decisión sobre embarazo

table(ive$`Decisión De la mujer sobre su embarazo`)
ive %>% group_by(`Decisión De la mujer sobre su embarazo`) %>% summarise(n()) #solución dplyir

# Tipo de establecimiento de atención

table(ive$`tipo de establecimiento`)

# Nacionalidad

table(ive$nacionalidad)


## 5. Operaciones Intermedias

#a. Promedio de edad:

# Por tipo de establecimiento

ive %>%  group_by(`tipo de establecimiento`) %>% 
  summarise(mean(edad,na.rm=TRUE))

# Por región

ive %>%  group_by(`Región de residencia de la mujer`) %>% 
  summarise(mean(edad,na.rm=TRUE)) %>% arrange(desc(`mean(edad, na.rm = TRUE)`))

#b. Porcentaje de 

# Mujeres que tienen sobre 40 años

ive %>%  filter(edad>40) %>% 
  summarise(n()/nrow(ive))

#c. Promedio de consultas de acompañamiento por región para aquellas mujeres que al menos asistieron a una consulta

ive %>% filter(`total de consultas de acompañamiento`>=1)  %>%
  group_by(`Región de residencia de la mujer`) %>%
  summarise(mean(`total de consultas de acompañamiento`)) 

## 6. Operaciones avanzadas

#Crear serie temporal con el número de mujeres mensual que decidieron interrumpir su embarazo. 

ivemen <- ive %>% filter(`Decisión De la mujer sobre su embarazo`=="INTERRUMPIR EL EMBARAZO")  %>%
  group_by(`Año concurrencia`,`mes de concurrencia`) %>%
  summarise(n=n()) 

# Ordene de forma temporal. Para esto es necesario pasar el mes a numeric

ivemen <- ivemen %>% mutate(`mes de concurrencia`=as.numeric(`mes de concurrencia`)) %>%
  arrange(`Año concurrencia`,`mes de concurrencia`)

# cree una variable de tiempo

ivemen <- ivemen %>% mutate(fecha=as.Date(paste0(`Año concurrencia`,"-",`mes de concurrencia`,"-01")))

# Elimine los NAs y seleccione las columnas relevantes

ivemen <- ivemen %>% filter(!is.na(fecha)) %>% ungroup() %>% select(fecha,n)

# Grafique estos resultados

plot(ivemen$fecha,ivemen$n,type = "l",col="red")


rm(list=ls())
# data.table
#####

### 1.Setup

## Cargamos paquetes

library(data.table)
library(readxl)

## Abrimos la base de datos

ive <- read_xlsx(path ="DATOS_IVE_2018_2020.xlsx")
ive <- as.data.table(ive)

## 2. Exploración

head(ive)
View(ive)
names(ive)

## 3. Pre-procesamiento

#a. Seleccionar variables

ive<-ive[,-(PSICOLOGO1:VISITA10)]

#b. Cambiar clase de variables

ive[,edad:=as.integer(`edad de la mujer`)]
ive[,edadgest:=as.integer(`edad gestacional concurrencia`)]

## 4. Operaciones sencillas

#a. Calcular promedio de:

# edad

ive[,mean(edad,na.rm=T)]

# edad gestacional

ive[,mean(edadgest,na.rm=T)]

#b. Calcular número de casos:

# Decisión sobre embarazo

ive[,.N,by=.(`Decisión De la mujer sobre su embarazo`)]

# Tipo de establecimiento de atención

ive[,.N,by=.(`tipo de establecimiento`)]

# Nacionalidad

ive[,.N,by=.(nacionalidad)][order(N, decreasing = TRUE)]

## 5. Operaciones Intermedias

#a. Promedio de edad:

# Por tipo de establecimiento

ive[,mean(edad,na.rm=T),by=.(`tipo de establecimiento`)]

# Por región

ive[,mean(edad,na.rm=T),by=.(`Región de residencia de la mujer`)][order(V1,decreasing = TRUE)]

#b. Porcentaje de 

# Mujeres que tienen sobre 40 años

ive[edad>40,.N/ive[,.N]]

#c. Promedio de consultas de acompañamiento por región para aquellas mujeres que al menos asistieron a una consulta

ive[`total de consultas de acompañamiento`>=1,mean(`total de consultas de acompañamiento`,na.rm=T),by=.(`Región de residencia de la mujer`)] 


## 6. Operaciones avanzadas

#Crear serie temporal con el número de mujeres mensual que decidieron interrumpir su embarazo. 

ivemen <- ive[`Decisión De la mujer sobre su embarazo`=="INTERRUMPIR EL EMBARAZO",.N,by=.(`Año concurrencia`,`mes de concurrencia`)]

# Ordene de forma temporal. Para esto es necesario pasar el mes a numeric

ivemen[,`mes de concurrencia`:=as.numeric(`mes de concurrencia`)]
ivemen <-ivemen[order(`Año concurrencia`,`mes de concurrencia`)]

# cree una variable de tiempo

ivemen[,fecha:=as.Date(paste0(`Año concurrencia`,"-",`mes de concurrencia`,"-01"))] 

# Elimine los NAs y seleccione las columnas relevantes

ivemen <- ivemen[!is.na(fecha),.(fecha,N)]

# Grafique estos resultados

plot(x=ivemen$fecha,y=ivemen$N,type = "l",col="red")

