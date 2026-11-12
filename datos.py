import pandas as pd

# Nombre del archivo CSV
ARCHIVO = "3a Dataset Bosques_V2.0 (2).csv"


# FUNCIÓN 1: Cargar y limpiar los datos
def cargar_datos():

    # Leer el CSV
    df = pd.read_csv(ARCHIVO, sep=";", encoding="latin-1")

    # Eliminar columnas completamente vacías
    df = df.dropna(axis=1, how="all")

    return df


# FUNCIÓN 2: Obtener el ranking de departamentos
def obtener_ranking(df, anio=None):

    # Filtrar por año, si se seleccionó uno
    if anio is not None:
        datos = df[df["ANIO"] == anio]
    else:
        datos = df

    # Calcular la pérdida total por departamento
    ranking = datos.groupby("DEPARTAMENTO")["PERDIDA_BOSQUE"].sum()

    # Ordenar de mayor a menor
    ranking = ranking.sort_values(ascending=False)

    return ranking

# FUNCIÓN 3: Obtener la evolución anual por departamento
def obtener_evolucion(df, departamentos=None):

    # Filtrar los departamentos seleccionados
    if departamentos is not None:
        datos = df[df["DEPARTAMENTO"].isin(departamentos)]#Permite comprobar si un departamento pertenece a una lista.
    else:
        datos = df

    # Sumar la pérdida de bosque por año y departamento
    evolucion = datos.groupby(
        ["ANIO", "DEPARTAMENTO"]
    )["PERDIDA_BOSQUE"].sum().reset_index()

    return evolucion

# FUNCIÓN 4: Preparar datos para el mapa departamental
def obtener_datos_mapa(df, anio=None):
    ranking = obtener_ranking(df, anio)
    return ranking.reset_index()
# FUNCIÓN 5: Obtener estadísticas generales
def obtener_resumen_general(df):

    perdida_total = df["PERDIDA_BOSQUE"].sum()
    perdida_por_anio = df.groupby("ANIO")["PERDIDA_BOSQUE"].sum()

    anio_maximo = perdida_por_anio.idxmax()
    ranking = obtener_ranking(df)
    departamento_maximo = ranking.idxmax()


    return perdida_total, anio_maximo, departamento_maximo
# FUNCIÓN 6: Obtener pérdida anual de bosque
def obtener_perdida_anual(df):

    perdida_anual = df.groupby("ANIO")["PERDIDA_BOSQUE"].sum()

    return perdida_anual.reset_index()

# PRUEBA DEL PROGRAMA
if __name__ == "__main__":

    df = cargar_datos()

    print("Tamaño de la base de datos:")
    print(df.shape)

    print("\nRanking del año 2020:")
    print(obtener_ranking(df, 2020))
    print("\nDatos del mapa del año 2020:")
    print(obtener_datos_mapa(df, 2020))
    print("\nEvolución anual de Ucayali:")
    print(obtener_evolucion(df, ["UCAYALI"]))
    print("\nResumen general de pérdida de bosque:")
    print(obtener_resumen_general(df))
    print("\nPérdida anual de bosque (2001-2022):")
    print(obtener_perdida_anual(df))