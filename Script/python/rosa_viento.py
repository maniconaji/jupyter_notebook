import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches

def clasificando_viento(df, nrosa, var_vientos, var_direccion, nombre_estacion):
    #clasificación del viento según su velocidad
    escala = { 
        0  : 'Calma',
        1  : '0,50 - 2,10', 
        2  : '2,10 - 3,60',
        3  : '3,60 - 5,70',
        4  : '5,70 - 8,80',
        5  : '8,80 - 11,10',
        6  : '>= 11,10',}
    bins_vel = np.array([0.5, 2.10, 3.60, 5.70, 8.80, 11.10])
    df['clase_velocidad'] = np.digitize(x = df[var_vientos], bins=bins_vel)
    
    # Clasificación viento según la dirección
    if nrosa == 8:
        step            = 360/nrosa
        name_directions = np.array('N NE E SE S SW W NW N'.split())
        bins            = np.arange(step/2, 360 + step, step)
        print(bins)
    elif nrosa == 16:
        step            = 360/nrosa
        name_directions = np.array('N NNE NE ENE E ESE SE SSE S SSW SW WSW W WNW NW NNW N'.split())
        bins            = np.arange(step/2, 360 + step, step)
    
    directions = {n: dir for n, dir in enumerate(name_directions)}
    df["Nclase_direccion"] = np.digitize(x = df[var_direccion], bins=bins)
    df["clase_direccion"]  = df["Nclase_direccion"].map(directions)
    
    # Determinación de la tabla pivote
    pivote = pd.pivot_table(
        df, 
        values     = var_vientos, 
        index      = "clase_velocidad", 
        columns    = "clase_direccion", 
        aggfunc    = "count", 
        fill_value = 0)[name_directions[:-1]]
    pivote.index   = pivote.index.map(escala)
    pivote.to_excel("Output/Data/rosadelosviento_"+nombre_estacion.replace(" ","")+".xlsx")
    calmas = pivote.iloc[0].sum().sum()*100/len(df)
    pivote = pivote[1:]
    pivote = pivote*100/pivote.sum().sum()
    return pivote, calmas, name_directions

def rosa_vientos(df, var_vientos, var_direccion, nrosa, nombre_estacion, **kwargs):
    """
    Descripción: Función para graficar ciclo diario de una variable.

    df          (Dataframe):    Conjunto de datos a graficar.
    var_vientos       (str):    Variable que representa a los vientos.
    var_direccion     (str):    Variable que representa a los direccion.
    nrosa             (int):    Número que corresponde a una rosa de 8 o 16 direcciones.
    nombre_estacion   (str):    Nombre de la estación de monitoreo.

    Ejemplo: 
    rosa_vientos(
        df              = df, 
        var_vientos     = "vientoVel", 
        var_direccion   = "vientoDir", 
        nrose           = 16, 
        nombre_estacion = "Estación San Fernando",
        )
    """

    df = df.filter([var_vientos, var_direccion]).dropna()
    pivote, calmas, name_directions = clasificando_viento(df, nrosa, var_vientos, var_direccion, nombre_estacion)
    

    # Define figura
    fig=plt.figure(
        figsize=(10,8),
        facecolor = 'lightgrey', 
        edgecolor = 'w')

    # definición de la rosa de los viento
    rect      = [0, 0.05, 0.85, 0.85]
    ax        = plt.axes(rect, projection='polar')
    btt       = 0
    direccion = np.linspace(0, 2*np.pi, nrosa+1)
    w         = 2*np.pi/nrosa

    # definición de parámetros polares
    ax.set(**{
        "theta_zero_location": "N", 
        "theta_direction": -1, 
        "rorigin": -1, 
        "rlim": (0,25), 
        "rlabel_position": 90, 
        "rticks": np.arange(0,25,5)})
        
    ax.set_thetagrids(direccion*(180/np.pi), name_directions, fontsize = 9)

    # Rosa de los vientos
    for n in range(len(pivote)):
        N = np.array(pivote.iloc[n].tolist())
        ax.bar(
            x = direccion[:nrosa], 
            height = N, 
            width  = w, 
            bottom = btt, 
            label = pivote.index[n], 
            **{
                "linewidth": 0.25, 
                "edgecolor": 'k', 
                "zorder": 5})
        btt = btt + N
    
    # Definición de legenda
    rxz=(0.325, 0.45, 1, 0.15)
    extraString = '{0:5} {1:.2f}%'.format('Calmas:', calmas)
    handles, labels = ax.get_legend_handles_labels()
    handles.append(mpatches.Patch(color='none', label=extraString))
    ax.legend(handles=handles, bbox_to_anchor=rxz, **{
        "loc": 0, 
        "facecolor": 'w', 
        "edgecolor": 'k', 
        "title": "Velocidad (m/s)", 
        "fontsize": 10, 
        "title_fontsize": 10})
    
    # Definición de titulo
    fig.suptitle("Rosa del viento "+nombre_estacion, **{"size": 14, "weight": "bold"})

    # guardar figura
    fig.savefig(**{"fname": "Output/Plot/rosadelosviento_"+nombre_estacion.replace(" ","")+".png", "facecolor": 'lightgrey', "edgecolor": 'k', "dpi": 96})

    # Cierre figura
    plt.close(fig)
    return