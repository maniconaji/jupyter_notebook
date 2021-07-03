## cargar librerias
library(dplyr)
library(C50)
library(gmodels)

## leer datos
data <- read.csv("train.csv")
dim(data)

## seleccionar variables
data <- data %>% 
  select(Target, escolari, dependency, age, qmobilephone, tamhog)

## convertir variables
data <- data %>% 
  mutate(dependency = as.numeric(ifelse(dependency == 'no', 0,
                                        ifelse(dependency == "yes", 1, dependency))))

data <- data %>% 
  mutate(Target = as.factor(Target))

## revisamos dataset
summary(data)

## separar set de entrenamiento y prueba
set.seed(123)
vector_entrenamiento <- sample(1:nrow(data),0.7*nrow(data))
data_train <- data[vector_entrenamiento,] 
data_test <- data[-vector_entrenamiento,]

## generamos el modelo
tree <- C5.0(data_train[, -1], 
             data_train$Target,
             control = C5.0Control(minCases = 100))

## exploramos el modelo
summary(tree)

## predecimos
p <- predict(tree, data_test[-1])

## matriz de confusión
CrossTable(x=data_test$Target, y=p, prop.r=FALSE, prop.c=FALSE,
           prop.t=FALSE, prop.chisq=FALSE)

## accuracy
print(100*sum(data_test$Target==p)/length(p))

