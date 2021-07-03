import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def ciclo_diario(df, variable, nombre_estacion, xlabel, ylabel, **kwargs):
    """
    Descripción: Función para graficar ciclo diario con promedio horario.

    df          (Dataframe):    Conjunto de datos a graficar.
    variable          (str):    Variable en "str" que se desea graficar.
    nombre_estacion   (str):    Nombre de la estación de monitoreo.
    xlabel            (str):    Nombre de eje x del gráfico.
    ylabel            (str):    Nombre de eje y del gráfico.
    **kwargs               :    Variables que no están definidas en la función directamente, pero que una vez que
                                ajuste a sus requerimientos, pueden ser cambiadas. Recordar que si se tiene kwargs debe estar definido cuando se llama la función.
    Ejemplo:
        ciclo_diario(
        df              = df, 
        variable        = "vientoVel",  
        nombre_estacion = "Estación San Fernando",     
        xlabel          = "Hora Local [horas]",
        ylabel          = "Velocidad del viento (m/s)",
        ylim            = {"bottom": 0, "top": 5},
        )
    """
    #Limpieza de valores NaN.
    df = df[variable].dropna()

    #Agrupar datas por hora.
    df = df.groupby(df.index.hour)
    
    #Calcular percentil 95, percentil 5 y promedio de los datos.
    df_P95 = df.apply(lambda x: np.percentile(x, 95))
    df_P05 = df.apply(lambda x: np.percentile(x, 5))
    df_promedio = df.mean()
    
    #Crear figura, los valores pueden ser modificados en función de lo que se necesite.
    fig, ax = plt.subplots( 
        figsize     = (9,6),
        gridspec_kw = {'left':0.075, 'right':0.975, 'top':0.945, 'bottom':0.085},
        facecolor   ='w', 
        edgecolor   ='w')
    
    #Graficar promedio de los datos.
    ax.plot(df_promedio, ls = "-", lw = 1.5, c = "blue", label = "Promedio", zorder = 2)
    ax.plot(df_P05, ls = "-", lw = 1.0, c = "k", label = "__no_legend__", zorder = 2)
    ax.plot(df_P95, ls = "-", lw = 1.0, c = "k", label = "__no_legend__", zorder = 2)

    #Graficar el 90% de los datos.
    ax.fill_between(
        x = df_P05.index, y1 = df_P05, y2 = df_P95, alpha = 0.3, color = 'blue', zorder = 2, label = "90% de datos")

    #Definición de limites: "x" corresponde al tiempo e "y" corresponde a el valor a graficar.
    ax.set_xlim(df_P95.index.min(), df_P95.index.max())
    ax.set_ylim(**kwargs["ylim"])

    #Definición de etiqueta del eje "x" y el eje "y".
    ax.set_xlabel(xlabel, fontsize = 11, fontweight = "normal", labelpad = 2.5)
    ax.set_ylabel(ylabel, fontsize = 11, fontweight = "normal", labelpad = 2.5)

    # Definición de tipografía del eje "x", el eje "y" y la grilla.
    ax.grid(True)
    ax.set(xticks = df_promedio.index)
    ax.tick_params(
        axis = "both", which = "major", direction = "in", length = 7.5, width = 1, pad = 5, 
        grid_color = 'k', grid_linewidth = 0.75, grid_linestyle = "--", grid_alpha = 0.8,
        bottom = True, top = True, left = True, right = True)

    # Definición de legenda
    ax.legend(
        loc = 0, ncol = 2, fontsize = 10, markerscale = 10, facecolor = 'lightgrey', edgecolor = 'k')
    # Definición del titulo del gráfico
    fig.suptitle(
        "Ciclo Diario de "+ylabel+" "+nombre_estacion, 
        size = 11, weight = "normal")
    # Guarda la figura
    fig.savefig(
        "Output/Plot/CD_"+variable+"_"+nombre_estacion.replace(" ","")+".png", 
        facecolor = 'w', edgecolor = 'w', dpi = 96)
    # Cierra la figura
    plt.close(fig)
    return