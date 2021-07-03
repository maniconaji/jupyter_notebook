rm(list=ls())
library("magrittr")

# Package names
packages <- c("tidyverse", "ggplot2", "lubridate", "reshape")

# Install packages not yet installed
installed_packages <- packages %in% rownames(installed.packages())
if (any(installed_packages == FALSE)) {
  install.packages(packages[!installed_packages])
}

# Packages loading
lapply(packages, library, character.only = TRUE) %>% invisible()

rm(packages, installed_packages) 

##################### Functions ###############################
readingCSVSEA <- function(path) {
  var_name <- strsplit(path, "_")[[1]][2] 
  df <- read.csv(
    path, 
    sep = ";", 
    dec = ",", 
    colClasses = c(
      "FECHA..YYMMDD."="character", 
      "HORA..HHMM."="character"),
    encoding = "utf8")
  if (length(names(df)) == 4) {
    colnames(df) <- c("FECHA", "HORA", var_name, "ERROR")
  } else {
    text <- "Registros validados;Registros preliminares;Registros no validado"
    text <- strsplit(text, ";")[[1]]
    colnames(df) <- c("FECHA", "HORA", 
                      var_name,
                      paste(var_name, "Pre", sep=""), 
                      paste(var_name, "NoVal", sep=""), 
                      "ERROR")
    df <- select(df, -c(paste(var_name, "Pre", sep=""),
                        paste(var_name, "NoVal", sep="")))
  }
  df$Datetime <- paste(df$FECHA, df$HORA, sep = "-") %>% 
    strptime(format="%y%m%d-%H%M")
  df <- select(df, -c(FECHA, HORA, ERROR))
  df[, c(2,1)]
}

##################33################### Reading Files ##########################
df <- lapply(
  list.files(path = "Data", pattern = "*.csv", full.names = TRUE), 
  readingCSVSEA) %>% reduce(full_join, by = "Datetime")

meltdf <- select(df, -Datetime) %>% melt()

#boxplot
p <- ggplot(meltdf, aes(factor(variable), value)) 
p + geom_boxplot() + facet_wrap(~variable, scale="free")