import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def series_de_tiempo(df, variable, nombre_estacion, xlabel, ylabel, **kwargs):
    """
    Descripción: Función para graficar series de tiempo con promedio mensual.

    df          (Dataframe):    Conjunto de datos a graficar.
    variable          (str):    Variable en "str" que se desea graficar.
    nombre_estacion   (str):    Nombre de la estación de monitoreo.
    xlabel            (str):    Nombre de eje x del gráfico.
    ylabel            (str):    Nombre de eje y del gráfico.
    **kwargs               :    Variables que no están definidas en la función directamente, pero que una vez que
                                ajuste a sus requerimientos, pueden ser cambiadas. Recordar que si se tiene kwargs debe estar definido cuando se llama la función.

    Ejemplo:
        series_de_tiempo(
            df              = df, 
            variable        = "velocidadDir", 
            nombre_estacion = "Estación San Fernando",
            xlabel          = "Tiempo [años]",
            ylabel          = "Dirección del viento (°)",
            ylim            = {"bottom": 0, "top": 360},
            major_locator   = {"locator": mdates.YearLocator()},
            major_formatter = {"formatter": mdates.DateFormatter('%Y')}
            )  
    """
    # Limpieza de valores NaN.
    df = df[variable].dropna()

    # Crear figura, los valores pueden ser modificados en función de lo que se necesite.
    fig, ax = plt.subplots(
        figsize     = (9,6),
        gridspec_kw = {'left':0.075, 'right':0.975, 'top':0.945, 'bottom':0.085},
        facecolor   ='w', 
        edgecolor   ='w')

    # Graficar datos, se recomienda como punto y no lineas.
    ax.plot(
        df,
        ls     = "None",
        ms     = 0.5, 
        marker = '.',
        c      = 'blue',
        label  = "Datos", 
        alpha  = 1, 
        zorder = 4
        )
    
    # Definición de limites: "x" corresponde al tiempo e "y" corresponde a el valor a graficar.
    ax.set_xlim( df.index.min(), df.index.max() )
    ax.set_ylim( **kwargs["ylim"] )
    
    # Definición de etiqueta del eje "x" y el eje "y".
    ax.set_xlabel( xlabel, fontsize =  11, fontweight = "normal", labelpad = 2.5)
    ax.set_ylabel( ylabel, fontsize =  11, fontweight = "normal", labelpad = 2.5)
    
    # Coloca ticks en cada año y el formato de cada uno de los ticks
    ax.xaxis.set_major_locator(**kwargs["major_locator"])
    ax.xaxis.set_major_formatter( **kwargs["major_formatter"] )
    
    # Definición de tipografía del eje "x", el eje "y" y la grilla.
    ax.grid(True)
    ax.tick_params(
        axis = "both", which = "major", direction = "in", length = 7.5, width = 1, pad = 5, 
        grid_color = 'k', grid_linewidth = 0.5, grid_linestyle = "--", grid_alpha = 0.8,
        bottom = True, top = True, left = True, right = True)
    
    # Definición de legenda
    ax.legend(
        loc = 0, ncol = 2, fontsize = 10, markerscale = 10, facecolor = 'lightgrey', edgecolor = 'k')
    # Definición del titulo del gráfico
    fig.suptitle(
        "Serie de Tiempo de "+ylabel+" "+nombre_estacion, 
        size = 11, weight = "normal")
    # Guarda la figura
    fig.savefig(
        "Output/Plot/ST_"+variable+"_"+nombre_estacion.replace(" ","")+".png",
        facecolor = 'w', edgecolor = 'w', dpi = 96)
    # Cierra la figura
    plt.close(fig)
    return