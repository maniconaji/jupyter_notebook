import os
import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from openpyxl import load_workbook

def ciclo_estacional(df, variable, nombre_estacion, vmin, vmax, step, clabel, unidad, **kwargs):
    """
    Descripción: Función para graficar ciclo estacional del viento.

    df          (Dataframe):    Conjunto de datos a graficar.
    variable          (str):    Variable en "str" que se desea graficar.
    nombre_estacion   (str):    Nombre de la estación de monitoreo.
    vmin              (int):    Valor mínimo.
    vmax              (int):    Valor máximo.
    step              (int):    Valor del paso a paso.
    clabel            (str):    Nombre completo de variable.
    unidad            (str):    Unidad correspondiente a la variable.

    Ejemplo:
    ciclo_estacional(
        df              = df, 
        variable        = "HR",, 
        nombre_estacion = "Estación San Fernando",
        vmin            = 0,
        vmax            = 100,
        step            = 2,
        clabel          = "Humedad Relativa del Aire",
        unidad          = "(%)",
        )
    """
    #Limpieza de valores NaN.
    df = df.filter([variable]).dropna()

    # Se agrega la columna hora y mes para tabla pivote
    df['HORA'] = df.index.hour
    df['MES']  = df.index.month
    
    # Tabla pivote con índice el mes y columna la hora, se considera usar la función mean para mostrar el promedio de los datos.
    pivote_var  = pd.pivot_table(data=df, values=variable, index="MES", columns="HORA", aggfunc="mean")
    
    # Guardar pivote en archivo excel
    name_file = "Output/Data/CE_"+nombre_estacion.replace(" ","")+".xlsx"
    if os.path.isfile(name_file)==True:
        ExcelWorkbook = load_workbook(name_file)
        writer = pd.ExcelWriter(name_file, engine = 'openpyxl')
        writer.book = ExcelWorkbook
        pivote_var.to_excel(writer, sheet_name=variable)
        writer.save()
        writer.close()
    else:
        pivote_var.to_excel(name_file, sheet_name=variable)


    
    #Interpolación pivote
    n = 5
    x = np.arange(pivote_var.columns.min() - 1 - 1/n, pivote_var.columns.max() + 1, 1/n )
    y = np.arange(pivote_var.index.min()   - 1 - 1/n, pivote_var.index.max()   + 1, 1/n )
    f_var  = interpolate.interp2d(pivote_var.columns , pivote_var.index , pivote_var.values , kind='linear')
    z_var  = f_var(x, y)
    
    #Crear figura, los valores pueden ser modificados en función de lo que se necesite.
    fig, (ax, cbar_ax) = plt.subplots(
        ncols       = 2,
        figsize     = (9,6), 
        gridspec_kw = {'wspace':0.025, 'hspace':0.25, 'left':0.075, 'right':0.925, 'top':0.950, 'bottom':0.1, "width_ratios": [.9, .025]},
        facecolor   ='lightgrey', 
        edgecolor   ='w')
    
    # Grafico de contornos, correspondiente a la velocidad del viento    
    cf = ax.contourf(
        x, y, z_var, **{"levels": np.arange(vmin, vmax + step, step), "cmap": 'jet'})
    ax.contour(
        x, y, z_var, **{"levels": np.arange(vmin, vmax + step, step), "colors": "black", "linewidths": 0.1})

    # Grafico que corresponde a la barra de colores
    plt.colorbar(cf, cax= cbar_ax, **{"ticks":  np.arange(vmin, vmax + step, step*5)})
    
    # Definición de etiqueta del eje "x" y el eje "y".
    ax.set_xlabel("Hora", **{"fontsize": 11, "fontweight": "normal", "labelpad": 2.5})
    ax.set_ylabel("Mes", **{"fontsize": 11, "fontweight": "normal", "labelpad": 2.5})
    cbar_ax.set_ylabel(clabel+" "+unidad, **{"fontsize": 11, "fontweight": "normal", "labelpad": 2.5})
    
    # Definición de números o tipografía del eje "x", eje "y" y "colorbar"
    ax.set(
        xticks = pivote_var.columns,
        yticks = pivote_var.index,
        xticklabels = pivote_var.columns,
        yticklabels = ["E", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
        )
    ax.tick_params(axis="both", **{"labelsize": 10, "length": 5, "direction": "in", "width": 1.25, "pad": 5})
    cbar_ax.tick_params(labelsize = 10)

    # Definición de limites
    ax.set_xlim(pivote_var.columns.min() - 5/(2*n), pivote_var.columns.max() + 5/(2*n))
    ax.set_ylim(pivote_var.index.min()   - 5/(2*n), pivote_var.index.max()   + 5/(2*n))
    
    # Definición de titulo
    ax.set_title("Ciclo Estacional "+clabel+" "+nombre_estacion, **{"size": 12, "weight": "normal", "pad": 5})

    # Guarda la figura
    fig.savefig(
        "Output/Plot/CE_"+variable+"_"+nombre_estacion.replace(" ","")+".png", 
        facecolor = 'w', edgecolor = 'w', dpi = 96)

    # Cierra la figura
    plt.close(fig)
    return