import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from openpyxl import load_workbook

def ciclo_diario_direccion(df, variable, nombre_estacion, vmin, vmax, **kwargs):
    """
    Descripción: Función para graficar series de tiempo con promedio mensual.

    df          (Dataframe):    Conjunto de datos a graficar.
    variable          (str):    Variable en "str" que se desea graficar.
    nombre_estacion   (str):    Nombre de la estación de monitoreo.
    vmin              (int):    Probabilidad mínima.
    vmax              (int):    Probabilidad máxima.
    **kwargs               :    Variables que no están definidas en la función directamente, pero que una vez que
                                ajuste a sus requerimientos, pueden ser cambiadas. Recordar que si se tiene kwargs debe estar definido cuando se llama la función.
    Ejemplo: 
    ciclo_diario_direccion(
        df              = df, 
        variable        = "vientoDir", 
        nombre_estacion = "Estación San Fernando",
        vmin            = 0,
        vmax            = 30
        )                                
    """
    #Limpieza de valores NaN.
    df = df.filter([variable]).dropna()

    #Creación de diccionario para definir la dirección del viento, en este caso se considera que la dirección esta en el rango de 0° a 360°.
    step        = 15
    bins        = np.arange(step/2, 360, step)
    directions  = {n: ndir for n, ndir in enumerate(np.arange(0, 360+step, step))}
    
    # clasificación de dirección en número de 1 al 16
    df["nombre_viento"] = np.digitize(x = df[variable], bins=bins)
    df["nombre_viento"] = df["nombre_viento"].map(directions)

    # Se agrega la columna hora para agilizar tabla pivote
    df['HORA'] = df.index.hour
    
    #función para determinar frecuencia relativa de una SerieFrame
    freq_relativa = lambda x: 100*x/x.sum()
    
    # Tabla pivote con índice la clasificación que se le da al viento y en las columnas la hora, se considera usar la función count para contar los valores que cumplen esa dirección a esa hora.
    pivot_table = pd.pivot_table(data=df, values = variable, index="nombre_viento",columns="HORA", aggfunc="count")
    
    #Determina la frecuencia relativa por cada hora
    pivot_table = pivot_table.apply(freq_relativa, axis=0)
    name_file = "Output/Data/CD_"+variable+"_"+nombre_estacion.replace(" ","")+".xlsx"
    if os.path.isfile(name_file)==True:
        ExcelWorkbook = load_workbook(name_file)
        writer = pd.ExcelWriter(name_file, engine = 'openpyxl')
        writer.book = ExcelWorkbook
        pivot_table.to_excel(writer, sheet_name=variable)
        writer.save()
        writer.close()
    else:
        pivot_table.to_excel(name_file, sheet_name=variable)
    
    #Crear figura, los valores pueden ser modificados en función de lo que se necesite.
    fig, (ax, cbar_ax) = plt.subplots(
        ncols       = 2,
        figsize     = (9,6), 
        gridspec_kw = {'wspace':0.025, 'hspace':0.25, 'left':0.075, 'right':0.925, 'top':0.950, 'bottom':0.1, "width_ratios": [.9, .025]},
        facecolor   ='lightgrey', 
        edgecolor   ='w')
    
    #Graficar promedio de los datos.
    cf = ax.imshow(
        pivot_table, **{"cmap": "jet", "origin": "lower", "vmin": vmin, "vmax": vmax, "zorder": 0, "aspect":"auto"})
    plt.colorbar(cf, cax= cbar_ax, ticks = np.arange(vmin, vmax + 5, 5))
    
    #Definición de etiqueta del eje "x" y el eje "y".
    ax.set_xlabel("Hora Local [horas]", fontsize = 11, fontweight = "normal", labelpad = 2.5)
    ax.set_ylabel("Dirección del Viento (°)", fontsize = 11, fontweight = "normal", labelpad = 2.5)

    # #Definición de números o tipografía del eje "x" o el eje "ylabelfw
    ax.set(xticks = pivot_table.columns, 
           yticks = np.arange(0, len(pivot_table.index), 2), 
           yticklabels = pivot_table.index[::2].astype(np.int32))
    ax.tick_params(
        axis = "both", which = "major", direction = "in", length = 5, width = 1, pad = 5, 
        grid_color = 'k', grid_linewidth = 0.75, grid_linestyle = "--", grid_alpha = 0.8,
        bottom = True, top = True, left = True, right = True, labelsize = 10)
    # #Definición de grilla, legenda y extras.
    ax.set_title(
        "Histograma del Ciclo Diario de la Dirección del Viento "+nombre_estacion, 
        **{"size": 12, "weight": "bold", "pad": 5})
    cbar_ax.set_ylabel(
        "Frecuencia (%)", fontsize = 11, labelpad = 2.5, fontweight="normal")
    fig.savefig(
        "Output/Plot/CD_"+variable+"_"+nombre_estacion.replace(" ","")+".png", 
        facecolor = 'w', edgecolor = 'w', dpi = 96)
    # Cierra la figura
    plt.close(fig)
    return