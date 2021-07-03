import os
import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from openpyxl import load_workbook

def ciclo_estacional_viento(df, velocidad, direccion, nombre_estacion, vmin, vmax, step, **kwargs):
    """
    Descripción: Función para graficar ciclo estacional del  viento.

    df          (Dataframe):    Conjunto de datos a graficar.
    velocidad         (str):    Variable que corresponde a la velocidad del viento.
    dirección         (str):    Variable que corresponde a la dirección del viento.
    nombre_estacion   (str):    Nombre de la estación de monitoreo.
    vmin              (int):    Valor mínimo.
    vmax              (int):    Valor máximo.
    step              (int):    Valor del paso a paso.
    **kwargs               :    Variables que no están definidas en la función directamente, pero que una vez que
                                ajuste a sus requerimientos, pueden ser cambiadas. Recordar que si se tiene kwargs debe estar definido cuando se llama la función.
    """
    #Limpieza de valores NaN.
    df = df.filter([velocidad, direccion]).dropna()
    
    # Se agrega la columna hora y mes para tabla pivote
    df['HORA'] = df.index.hour
    df['MES']  = df.index.month
    df['udir'] = df[velocidad]*np.sin(df[direccion] * np.pi/180)# + np.pi)
    df['vdir'] = df[velocidad]*np.cos(df[direccion] * np.pi/180)# + np.pi)

    # Tabla pivote con índice el mes y columna la hora, se considera usar la función mean para mostrar el promedio de los datos.
    pivote_viento = pd.pivot_table(data=df, values=velocidad, index="MES", columns="HORA", aggfunc="mean")
    pivote_udir   = pd.pivot_table(data=df, values="udir", index="MES", columns="HORA", aggfunc="mean")
    pivote_vdir   = pd.pivot_table(data=df, values="vdir", index="MES", columns="HORA", aggfunc="mean")
    
    name_file = "Output/Data/CE_"+nombre_estacion.replace(" ","")+".xlsx"
    if os.path.isfile(name_file)==True:
        ExcelWorkbook = load_workbook(name_file)
        writer = pd.ExcelWriter(name_file, engine = 'openpyxl')
        writer.book = ExcelWorkbook
        pivote_viento.to_excel(writer, sheet_name="viento")
        writer.save()
        writer.close()
    else:
        pivote_viento.to_excel(name_file, sheet_name="viento")


    #Interpolación pivote
    n = 5
    x = np.arange(pivote_viento.columns.min() - 1 - 1/n, pivote_viento.columns.max() + 1, 1/n )
    y = np.arange(pivote_viento.index.min()   - 1 - 1/n, pivote_viento.index.max()   + 1, 1/n )
    f_viento = interpolate.interp2d(pivote_viento.columns, pivote_viento.index, pivote_viento.values, kind='linear')
    f_udir   = interpolate.interp2d(pivote_udir.columns, pivote_udir.index, pivote_udir.values, kind='linear')
    f_vdir   = interpolate.interp2d(pivote_vdir.columns, pivote_vdir.index, pivote_vdir.values, kind='linear')
    z_viento = f_viento(x, y)
    u        = f_udir(x, y)
    v        = f_vdir(x, y)
    
    #Crear figura, los valores pueden ser modificados en función de lo que se necesite.
    fig, (ax, cbar_ax) = plt.subplots(
        ncols       = 2,
        figsize     = (9,6), 
        gridspec_kw = {'wspace':0.025, 'hspace':0.25, 'left':0.075, 'right':0.925, 'top':0.950, 'bottom':0.1, "width_ratios": [.9, .025]},
        facecolor   ='lightgrey', 
        edgecolor   ='w')
    
    # Grafico de contornos, correspondiente a la velocidad del viento    
    cf = ax.contourf(x, y, z_viento, **{"levels": np.arange(vmin, vmax + step, step), "cmap": 'jet'})
    ax.contour(x, y, z_viento, **{"levels": np.arange(vmin, vmax + step, step), "colors": "black", "linewidths": 0.15})

    # Grafico que contiene las flechas que representan la dirección del viento
    ax.quiver(x[1::n], y[1::n], u[1::n, 1::n], v[1::n, 1::n], scale_units='xy', scale=5, units="xy", width=0.025, headwidth=3., headlength=4.)
    
    # Grafico que corresponde a la barra de colores
    plt.colorbar(cf, cax= cbar_ax, **{"ticks":  np.arange(vmin, vmax + step*10, step*10)})
    
    # #Definición de etiqueta del eje "x", el eje "y" y colorvar
    ax.set_xlabel("Hora", **{"fontsize": 11, "fontweight": "normal", "labelpad": 2.5})
    ax.set_ylabel("Mes", **{"fontsize": 11, "fontweight": "normal", "labelpad": 2.5})
    cbar_ax.set_ylabel("Velocidad del viento (m/s)", **{"fontsize": 11, "fontweight": "normal", "labelpad": 5})
    
    # #Definición de números o tipografía del eje "x", eje "y" y colorbar
    ax.set(
        xticks = pivote_viento.columns,
        yticks = pivote_viento.index,
        xticklabels = pivote_viento.columns,
        yticklabels = ["E", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
        )
    ax.tick_params(axis="both", **{"labelsize": 10, "length": 5, "direction": "in", "width": 1.25, "pad": 5})
    cbar_ax.tick_params(labelsize = 10)
    
    # Definición de limites
    ax.set_xlim(pivote_viento.columns.min() - 5/(2*n), pivote_viento.columns.max() + 5/(2*n))
    ax.set_ylim(pivote_viento.index.min()   - 5/(2*n), pivote_viento.index.max()   + 5/(2*n))
    
    # Definición de titulo
    ax.set_title("Ciclo Estacional del viento "+nombre_estacion, **{"size": 12, "weight": "normal", "pad": 5})
    
    # Guarda la figura
    fig.savefig(
        "Output/Plot/CE_Viento_"+nombre_estacion.replace(" ","")+".png", 
        facecolor = 'w', edgecolor = 'w', dpi = 96)
    
    # Cierra la figura
    plt.close(fig)
    return