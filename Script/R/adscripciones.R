# cargar librerias
library(data.table)
library(C50)
library(gmodels)

## carga de datos
dataset <- fread('dataset_empresas_adscripciones.csv', stringsAsFactors = T)
dataset$ventas <- as.factor(dataset$ventas)
dataset$Target <- as.factor(dataset$Target)

## revisamos dataset
summary(dataset)

## separar set de entrenamiento y prueba
set.seed(123)
vector_entrenamiento <- sample(1:nrow(dataset),0.7*nrow(dataset))
data_train <- dataset[vector_entrenamiento,] 
data_test <- dataset[-vector_entrenamiento,]


## generamos el modelo
modelo = C5.0(x = data_train[, c(2,3,4,6,8,10)], 
              y = data_train$Target,
              control = C5.0Control(minCases = 100))

## exploramos el modelo
summary(modelo)

## predecimos
predicciones <- predict(modelo, 
                        newdata = data_test[, c(2,3,4,6,8,10)])

## Matriz de confusión
CrossTable(data_test$Target, predicciones,
           prop.chisq = FALSE, prop.c = FALSE, prop.r = FALSE)

## accuracy
print(100*sum(data_test$Target==predicciones)/length(predicciones))

#76