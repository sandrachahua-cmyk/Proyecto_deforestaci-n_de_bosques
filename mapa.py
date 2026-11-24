import streamlit as st
import folium
import pandas as pd
import altair as alt
import json
import unicodedata
import re

from pathlib import Path
from streamlit_folium import st_folium
from datos import cargar_datos


# ==================================================
# 1. RUTA DEL ARCHIVO GEOGRÁFICO
# ==================================================

RUTA_MAPA = (
    Path(__file__).resolve().parent
    / "assets"
    / "mapa"
    / "peru_departamental_simple.geojson"
)


# ==================================================
# 2. NORMALIZAR NOMBRES
# ==================================================

def normalizar_nombre(nombre):

    nombre = str(nombre).upper().strip()

    nombre = unicodedata.normalize("NFD", nombre)

    return "".join(
        letra for letra in nombre
        if unicodedata.category(letra) != "Mn"
    )


# ==================================================
# 3. ESCALA DE COLORES
# ==================================================

def obtener_color(perdida):

    if perdida is None or pd.isna(perdida):
        return "#D9D9D9"

    elif perdida < 10000:
        return "#26734D"

    elif perdida < 50000:
        return "#8BC34A"

    elif perdida < 150000:
        return "#FDD835"

    elif perdida < 300000:
        return "#FB8C00"

    elif perdida < 500000:
        return "#E53935"

    else:
        return "#8B0000"


# ==================================================
# 4. FORMATO DE HECTÁREAS
# ==================================================

def formato_hectareas(valor):

    if valor is None or pd.isna(valor):
        return "Sin datos"

    return (
        f"{valor:,.2f}"
        .replace(",", " ")
        .replace(".", ",")
        + " ha"
    )


# ==================================================
# 5. FUNCIÓN PRINCIPAL
# ==================================================

def mostrar_mapa():

    st.title("Pérdida acumulada de bosque en el Perú")

    st.markdown("""
    Explora la distribución territorial de la pérdida
    acumulada de bosque húmedo amazónico y la superficie
    forestal existente en el Perú desde el año 2001.
    """)

    # Cargar la base de datos

    df = cargar_datos().copy()

    df["DEPARTAMENTO"] = df["DEPARTAMENTO"].apply(
        normalizar_nombre
    )

    # Verificar registros duplicados

    if df.duplicated(subset=["UBIGEO", "ANIO"]).any():

        st.error(
            "Se encontraron registros duplicados "
            "para un mismo distrito y año."
        )

        return

    # SELECTOR DE AÑO

    anio = st.slider(
        "Selecciona el año final del periodo",
        min_value=2001,
        max_value=2022,
        value=2022,
        step=1
    )

    st.markdown(
        f"**Periodo acumulado: 2001 – {anio}**"
    )


    # ==================================================
    # 6. CALCULAR LA PÉRDIDA ACUMULADA
    # ==================================================

    df_periodo = df[
        (df["ANIO"] >= 2001) &
        (df["ANIO"] <= anio)
    ]

    perdidas = df_periodo.groupby(
        "DEPARTAMENTO"
    )["PERDIDA_BOSQUE"].sum(min_count=1).to_dict()


    # ==================================================
    # 7. CALCULAR LA COBERTURA FORESTAL
    # ==================================================

    df_anio = df[df["ANIO"] == anio]

    cobertura = df_anio.groupby(
        "DEPARTAMENTO"
    )["SUP_BOSQUE"].sum(min_count=1).to_dict()

    departamentos_estudiados = set(
        df["DEPARTAMENTO"]
    )


    # ==================================================
    # 8. CARGAR EL GEOJSON
    # ==================================================

    with open(RUTA_MAPA, encoding="utf-8") as archivo:

        departamentos = json.load(archivo)


    # ==================================================
    # 9. RELACIONAR EL CSV CON EL GEOJSON
    # ==================================================

    for feature in departamentos["features"]:

        propiedades = feature["properties"]

        nombre = normalizar_nombre(
            propiedades["NOMBDEP"]
        )

        perdida = perdidas.get(nombre)

        superficie = cobertura.get(nombre)

        propiedades["nombre"] = nombre

        propiedades["color"] = obtener_color(perdida)

        propiedades["periodo"] = f"2001 – {anio}"

        if nombre not in departamentos_estudiados:

            propiedades["perdida"] = "Fuera del estudio"

            propiedades["cobertura"] = "Fuera del estudio"

        else:

            propiedades["perdida"] = formato_hectareas(
                perdida
            )

            propiedades["cobertura"] = formato_hectareas(
                superficie
            )


    # ==================================================
    # 10. DISTRIBUCIÓN DE LA PÁGINA
    # ==================================================

    col_leyenda, col_mapa = st.columns([1, 3])

    # LEYENDA DE COLORES

    with col_leyenda:

        st.markdown("### Pérdida acumulada")

        st.caption(
            "Superficie expresada en hectáreas"
        )

        rangos = [
            ("#26734D", "0 a < 10 000"),
            ("#8BC34A", "10 000 a < 50 000"),
            ("#FDD835", "50 000 a < 150 000"),
            ("#FB8C00", "150 000 a < 300 000"),
            ("#E53935", "300 000 a < 500 000"),
            ("#8B0000", "500 000 o más"),
            ("#D9D9D9", "Fuera del estudio o sin datos")
        ]

        for color, texto in rangos:

            st.markdown(
                f"""
                <div style="
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin-bottom: 15px;
                ">
                    <div style="
                        background-color: {color};
                        width: 24px;
                        height: 24px;
                        border-radius: 4px;
                        flex-shrink: 0;
                    "></div>
                    <span>{texto}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.info(
            "Pasa el cursor sobre un departamento "
            "para consultar sus datos. Haz clic sobre "
            "él para explorar sus provincias."
        )


    # ==================================================
    # 11. CONSTRUIR EL MAPA
    # ==================================================

    with col_mapa:

        mapa = folium.Map(
            location=[-9.19, -75.01],
            zoom_start=6,
            tiles=None,
            zoom_control=False,
            scroll_wheel_zoom=False,
            dragging=False,
            double_click_zoom=False,
            touch_zoom=False,
            box_zoom=False,
            keyboard=False,
            zoom_snap=0.25
        )

        # Fondo blanco y ocultar texto de Leaflet

        mapa.get_root().header.add_child(
            folium.Element("""
                <style>

                    .leaflet-container {
                        background-color: #FFFFFF !important;
                    }

                    .leaflet-control-attribution {
                        display: none !important;
                    }

                </style>
            """)
        )

        # Límites y colores departamentales

        capa = folium.GeoJson(

            departamentos,

            name="Pérdida acumulada de bosque",

            style_function=lambda feature: {
                "fillColor": feature["properties"]["color"],
                "color": "#FFFFFF",
                "weight": 1.5,
                "fillOpacity": 1
            },

            highlight_function=lambda feature: {
                "color": "#333333",
                "weight": 3,
                "fillOpacity": 0.85
            },

            # RECUADRO DE INFORMACIÓN

            tooltip=folium.GeoJsonTooltip(

                fields=[
                    "nombre",
                    "periodo",
                    "perdida",
                    "cobertura"
                ],

                aliases=[
                    "Departamento:",
                    "Periodo acumulado:",
                    "Pérdida acumulada:",
                    f"Cobertura forestal en {anio}:"
                ],

                sticky=True,

                style="""
                    background-color: white;
                    color: #263D2B;
                    font-family: Arial;
                    font-size: 14px;
                    padding: 12px;
                    border-radius: 8px;
                    border: 1px solid #CCCCCC;
                """
            ),

            # Identificar departamento seleccionado

            popup=folium.GeoJsonPopup(
                fields=["nombre"],
                labels=False
            )

        ).add_to(mapa)

        # Centrar el mapa

        mapa.fit_bounds(
            capa.get_bounds(),
            padding=(20, 20)
        )

        # Visualizar el mapa y recuperar el clic

        resultado_mapa = st_folium(
            mapa,
            use_container_width=True,
            height=600,
            key=f"mapa_{anio}",
            returned_objects=[
                "last_object_clicked_popup"
            ]
        )


    # ==================================================
    # 12. ANÁLISIS PROVINCIAL
    # ==================================================

    st.divider()

    st.header(
        "Pérdida acumulada de bosque por provincias"
    )

    # Recuperar el departamento seleccionado

    seleccion = resultado_mapa.get(
        "last_object_clicked_popup"
    )

    departamento_elegido = None

    if seleccion:

        # Eliminar etiquetas HTML

        texto = re.sub(
            r"<[^>]+>",
            " ",
            str(seleccion)
        )

        texto = normalizar_nombre(
            " ".join(texto.split())
        )

        # Comparar nombres de departamentos

        nombres_mapa = sorted(
            [
                feature["properties"]["nombre"]
                for feature in departamentos["features"]
            ],
            key=len,
            reverse=True
        )

        for departamento in nombres_mapa:

            if re.search(
                r"\b" + re.escape(departamento) + r"\b",
                texto
            ):

                departamento_elegido = departamento
                break

    # Guardar selección

    if departamento_elegido is not None:

        st.session_state["departamento_mapa"] = (
            departamento_elegido
        )

    departamento_elegido = st.session_state.get(
        "departamento_mapa"
    )

    # Si todavía no se selecciona un departamento

    if departamento_elegido is None:

        st.info(
            "Haz clic sobre un departamento del mapa "
            "para visualizar la pérdida acumulada "
            "de sus provincias."
        )

    # Departamento fuera del estudio

    elif departamento_elegido not in departamentos_estudiados:

        st.warning(
            f"{departamento_elegido} no forma parte "
            "del ámbito de estudio de esta base de datos."
        )

    # Departamento monitoreado

    else:

        st.subheader(
            departamento_elegido.title()
        )

        st.markdown(
            f"**Periodo acumulado: 2001 – {anio}**"
        )

        # Filtrar departamento seleccionado

        df_departamento = df_periodo[
            df_periodo["DEPARTAMENTO"]
            == departamento_elegido
        ]

        # Agrupar pérdida por provincias

        provincias = df_departamento.groupby(
            "PROVINCIA"
        )["PERDIDA_BOSQUE"].sum(
            min_count=1
        ).reset_index()

        # Eliminar valores no disponibles

        provincias = provincias.dropna(
            subset=["PERDIDA_BOSQUE"]
        )

        # Ordenar de mayor a menor

        provincias = provincias.sort_values(
            "PERDIDA_BOSQUE",
            ascending=False
        )

        if provincias.empty:

            st.warning(
                "No hay datos provinciales disponibles "
                "para el periodo seleccionado."
            )

        else:

            # Calcular indicadores

            total_provincias = len(provincias)

            perdida_total = provincias[
                "PERDIDA_BOSQUE"
            ].sum()

            provincia_mayor = provincias.iloc[0][
                "PROVINCIA"
            ]

            perdida_provincia_mayor = provincias.iloc[0][
                "PERDIDA_BOSQUE"
            ]


            # ==========================================
            # 13. INDICADORES PROVINCIALES
            # ==========================================

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Provincias monitoreadas",
                    total_provincias
                )

            with col2:

                st.metric(
                    "Pérdida acumulada",
                    formato_hectareas(perdida_total)
                )

            with col3:

                st.metric(
                    "Provincia con mayor pérdida",
                    provincia_mayor.title()
                )


            # ==========================================
            # 14. GRÁFICO DE BARRAS HORIZONTALES
            # ==========================================

            st.markdown(
                "### Distribución de la pérdida por provincia"
            )

            provincias = provincias.copy()

            provincias["PROVINCIA"] = (
                provincias["PROVINCIA"].str.title()
            )

            provincias["HECTAREAS"] = (
                provincias["PERDIDA_BOSQUE"]
                .apply(formato_hectareas)
            )

            grafico = alt.Chart(provincias).mark_bar(
                color="#386641",
                cornerRadiusEnd=4,
                size=30
            ).encode(

                x=alt.X(
                    "PERDIDA_BOSQUE:Q",
                    title="Pérdida acumulada (ha)",
                    axis=alt.Axis(
                        format=",.0f",
                        grid=True
                    )
                ),

                y=alt.Y(
                    "PROVINCIA:N",
                    title="Provincia",
                    sort="-x",
                    axis=alt.Axis(
                        labelLimit=350,
                        labelFontSize=12
                    )
                ),

                tooltip=[
                    alt.Tooltip(
                        "PROVINCIA:N",
                        title="Provincia"
                    ),
                    alt.Tooltip(
                        "HECTAREAS:N",
                        title="Pérdida acumulada"
                    )
                ]

            ).properties(
                height=max(
                    300,
                    len(provincias) * 45
                )
            ).configure_view(
                strokeWidth=0
            )

            st.altair_chart(
                grafico,
                use_container_width=True
            )


            # ==========================================
            # 15. INTERPRETACIÓN AUTOMÁTICA
            # ==========================================

            if perdida_total > 0:

                porcentaje = (
                    perdida_provincia_mayor
                    / perdida_total
                ) * 100

                st.info(
                    f"La provincia de "
                    f"{provincia_mayor.title()} "
                    f"registra una pérdida acumulada de "
                    f"{formato_hectareas(perdida_provincia_mayor)}, "
                    f"lo que representa el "
                    f"{porcentaje:.2f}% de la pérdida "
                    f"provincial registrada en "
                    f"{departamento_elegido.title()} "
                    f"durante el periodo 2001–{anio}."
                )


    # ==================================================
    # 16. NOTA METODOLÓGICA
    # ==================================================

    st.divider()

    st.markdown("### Nota metodológica")

    st.caption(
        "La pérdida acumulada corresponde a la suma "
        "de las hectáreas de bosque perdido desde 2001 "
        "hasta el año seleccionado. La cobertura forestal "
        "corresponde a la superficie de bosque existente "
        "en el año seleccionado, tomando como línea base "
        "el año 2000. Los rangos de colores son una "
        "clasificación propia para fines de visualización."
    )

    st.caption(
        "Los indicadores provinciales se calculan "
        "a partir de los distritos monitoreados "
        "incluidos en la base de datos."
    )

    st.caption(
        "Fuente de datos: Ministerio del Ambiente (MINAM). "
        "Monitoreo de la cobertura de bosques "
        "a nivel distrital."
    )

    st.caption(
        "Fuente cartográfica: juaneladio/peru-geojson. "
        "Visualización cartográfica mediante Folium y Leaflet."
    )


# ==================================================
# 17. PRUEBA INDEPENDIENTE
# ==================================================

if __name__ == "__main__":

    st.set_page_config(
        layout="wide",
        page_title="Mapa de pérdida forestal"
    )

    mostrar_mapa()