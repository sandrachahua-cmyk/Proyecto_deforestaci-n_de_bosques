import streamlit as st
import folium
import pandas as pd
import altair as alt
import json
import unicodedata
import re
import base64

from html import escape
from pathlib import Path
from streamlit_folium import st_folium
from datos import cargar_datos


# ==================================================
# 1. RUTAS DE LOS ARCHIVOS
# ==================================================

CARPETA_MAPA = (
    Path(__file__).resolve().parent
    / "assets"
    / "mapa"
)

RUTA_MAPA = CARPETA_MAPA / "peru_departamental_simple.geojson"

RUTA_PORTADA = CARPETA_MAPA / "portada.mapa.png"


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
# 5. TARJETAS ESTADÍSTICAS
# ==================================================

def tarjeta(etiqueta, valor, color="#243B2B"):

    contenido = (
        '<div class="tarjeta-mapa">'
        '<div class="tarjeta-etiqueta">'
        f'{escape(str(etiqueta))}'
        '</div>'
        f'<div class="tarjeta-valor" style="color:{color};">'
        f'{escape(str(valor))}'
        '</div>'
        '</div>'
    )

    st.html(contenido)


# ==================================================
# 6. DISEÑO GENERAL
# ==================================================

def aplicar_estilos_mapa():

    st.html("""
    <style>

        #MainMenu, footer, header {
            visibility: hidden;
        }

        html, body {
            overflow-x: hidden;
        }

        .stApp {
            background-color: #F4F5F1;
            color: #000000;
            overflow-x: hidden;
        }

        [data-testid="stMain"] {
            overflow-x: hidden;
        }

        .block-container {
            padding: 25px 4% !important;
            max-width: 100% !important;
        }

        /* IMAGEN PANORÁMICA */

        .banner-mapa {
            position: relative;
            width: calc(100% / 0.92);
            height: 380px;
            margin-left: calc(-4% / 0.92);
            margin-top: -25px;
            overflow: hidden;
            background-color: #386641;
        }

        .banner-mapa img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center;
            display: block;
        }

        /* FRANJA SUPERIOR MARRÓN */

        .barra-mapa {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #A66C4B;
            padding: 18px 4%;
            box-sizing: border-box;
            z-index: 10;
        }

        .barra-mapa a {
            color: white !important;
            text-decoration: none !important;
            font-size: 16px;
            font-weight: bold;
        }

        .barra-mapa a:hover {
            opacity: 0.85;
        }

        /* ENCABEZADO */

        .encabezado-mapa {
            padding: 15px 0 10px 0;
        }

        .etiqueta-mapa {
            color: #000000;
            font-size: 13px;
            letter-spacing: 3px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .titulo-mapa {
            color: #000000 !important;
            font-size: 32px !important;
            font-weight: 700;
            margin: 5px 0 15px 0;
            line-height: 1.3;
        }

        .descripcion-mapa {
            color: #000000;
            font-size: 15px;
            line-height: 1.7;
            max-width: 1000px;
        }

        /* SUBTÍTULOS NUMERADOS */

        .subtitulo-mapa {
            color: #314B36;
            font-size: 19px;
            font-weight: 700;
            letter-spacing: 1px;
            margin-top: 25px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #CBD5C8;
        }

        /* TARJETAS ESTADÍSTICAS */

        .tarjeta-mapa {
            background: rgba(166,108,75,0.12);
            border: 1px solid rgba(166,108,75,0.25);
            border-radius: 12px;
            padding: 18px;
            min-height: 115px;
            box-sizing: border-box;
            margin-bottom: 12px;
        }

        .tarjeta-etiqueta {
            color: #000000;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .tarjeta-valor {
            font-size: 23px;
            font-weight: 600;
            margin-top: 12px;
            overflow-wrap: anywhere;
        }

        /* LEYENDA DE COLORES */

        .leyenda-mapa {
            background-color: #FFFFFF;
            border: 1px solid #DDE3D9;
            border-radius: 12px;
            padding: 18px;
        }

        .leyenda-titulo {
            color: #243B2B;
            font-size: 17px;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .leyenda-descripcion {
            color: #66756A;
            font-size: 12px;
            margin-bottom: 20px;
        }

        .fila-leyenda {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
            color: #243B2B;
            font-size: 13px;
        }

        .color-leyenda {
            width: 24px;
            height: 24px;
            border-radius: 4px;
            flex-shrink: 0;
        }

        /* PERIODO SELECCIONADO */

        .periodo-mapa {
            background-color: #E3EDE1;
            border: 1px solid #C5D6C2;
            color: #314B36;
            padding: 12px 18px;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 600;
            text-align: center;
            margin-bottom: 15px;
        }

        /* INFORMACIÓN DEPARTAMENTAL */

        .nombre-departamento {
            font-size: 25px;
            color: #314B36;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .periodo-departamento {
            font-size: 13px;
            color: #66756A;
            margin-bottom: 20px;
        }

        /* INTERPRETACIÓN */

        .interpretacion-mapa {
            background-color: #E8F0E5;
            border-left: 5px solid #386641;
            border-radius: 6px;
            padding: 20px;
            color: #243B2B;
            font-size: 15px;
            line-height: 1.7;
            margin-top: 15px;
        }

        /* TEXTOS GENERALES */

        div[data-testid="stWidgetLabel"] p {
            color: #000000 !important;
        }

        .stMarkdown h3 {
            color: #243B2B !important;
        }

        /* PANTALLAS PEQUEÑAS */

        @media (max-width: 750px) {

            .banner-mapa {
                height: 250px;
            }

            .titulo-mapa {
                font-size: 25px !important;
            }

            .etiqueta-mapa {
                font-size: 11px;
                letter-spacing: 2px;
            }

            .tarjeta-valor {
                font-size: 20px;
            }

        }

    </style>
    """)


# ==================================================
# 7. MOSTRAR PORTADA PANORÁMICA
# ==================================================

def mostrar_portada_mapa():

    imagen_html = ""

    if RUTA_PORTADA.exists():

        imagen_base64 = base64.b64encode(
            RUTA_PORTADA.read_bytes()
        ).decode()

        imagen_html = (
            f'<img src="data:image/png;base64,{imagen_base64}" '
            'alt="Bosque amazónico">'
        )

    portada_html = (
        '<div class="banner-mapa">'
        f'{imagen_html}'
        '<div class="barra-mapa">'
        '<a href="/?seccion=inicio" target="_top">'
        '← Inicio'
        '</a>'
        '</div>'
        '</div>'

        '<div class="encabezado-mapa">'

        '<div class="etiqueta-mapa">'
        'BOSQUES DEL PERÚ / EXPLORACIÓN TERRITORIAL'
        '</div>'

        '<h1 class="titulo-mapa">'
        'DISTRIBUCIÓN GEOGRÁFICA DE LA PÉRDIDA DE BOSQUE'
        '</h1>'

        '<p class="descripcion-mapa">'
        '<strong>'
        '¿Dónde se concentra la pérdida de bosque en el Perú?'
        '</strong>'
        '</p>'

        '<p class="descripcion-mapa">'
        'Explora la distribución territorial de la pérdida '
        'acumulada de bosque húmedo amazónico y la superficie '
        'forestal existente en los departamentos del Perú '
        'durante el periodo 2001–2022. '
        'Selecciona un departamento para conocer la '
        'distribución de la pérdida de bosque entre '
        'sus provincias.'
        '</p>'

        '</div>'
    )

    st.html(portada_html)

    if not RUTA_PORTADA.exists():

        st.warning(
            "No se encontró la imagen portada.mapa.png "
            "dentro de assets/mapa."
        )


# ==================================================
# 8. SUBTÍTULOS
# ==================================================

def subtitulo(texto):

    st.html(
        '<div class="subtitulo-mapa">'
        f'{escape(texto)}'
        '</div>'
    )


# ==================================================
# 9. FUNCIÓN PRINCIPAL
# ==================================================

def mostrar_mapa():

    aplicar_estilos_mapa()

    mostrar_portada_mapa()

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


    # ==================================================
    # 10. EXPLORACIÓN TEMPORAL
    # ==================================================

    subtitulo("01 / EXPLORACIÓN TEMPORAL")

    st.markdown(
        "Selecciona el año final para explorar la "
        "pérdida de bosque acumulada desde el año 2001."
    )

    anio = st.slider(
        "Año final del periodo:",
        min_value=2001,
        max_value=2022,
        value=2022,
        step=1,
        key="selector_anio_mapa"
    )

    st.html(
        '<div class="periodo-mapa">'
        f'Periodo acumulado: 2001 – {anio}'
        '</div>'
    )


    # ==================================================
    # 11. CALCULAR LA PÉRDIDA ACUMULADA
    # ==================================================

    df_periodo = df[
        (df["ANIO"] >= 2001) &
        (df["ANIO"] <= anio)
    ]

    perdidas = df_periodo.groupby(
        "DEPARTAMENTO"
    )["PERDIDA_BOSQUE"].sum(
        min_count=1
    ).to_dict()


    # ==================================================
    # 12. CALCULAR LA COBERTURA FORESTAL
    # ==================================================

    df_anio = df[df["ANIO"] == anio]

    cobertura = df_anio.groupby(
        "DEPARTAMENTO"
    )["SUP_BOSQUE"].sum(
        min_count=1
    ).to_dict()

    departamentos_estudiados = set(
        df["DEPARTAMENTO"]
    )


    # ==================================================
    # 13. CARGAR EL GEOJSON
    # ==================================================

    if not RUTA_MAPA.exists():

        st.error(
            "No se encontró el archivo "
            "peru_departamental_simple.geojson."
        )

        return

    with open(RUTA_MAPA, encoding="utf-8") as archivo:

        departamentos = json.load(archivo)


    # ==================================================
    # 14. RELACIONAR EL CSV CON EL GEOJSON
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
    # 15. DISTRIBUCIÓN GEOGRÁFICA
    # ==================================================

    subtitulo("02 / DISTRIBUCIÓN GEOGRÁFICA")

    col_leyenda, col_mapa, col_detalle = st.columns(
        [1, 2.5, 1.3]
    )


    # ==================================================
    # 16. LEYENDA DE COLORES CORREGIDA
    # ==================================================

    with col_leyenda:

        rangos = [
            ("#26734D", "0 a < 10 000"),
            ("#8BC34A", "10 000 a < 50 000"),
            ("#FDD835", "50 000 a < 150 000"),
            ("#FB8C00", "150 000 a < 300 000"),
            ("#E53935", "300 000 a < 500 000"),
            ("#8B0000", "500 000 o más"),
            ("#D9D9D9", "Fuera del estudio o sin datos")
        ]

        filas = ""

        for color, texto in rangos:

            filas += (
                '<div class="fila-leyenda">'
                '<div class="color-leyenda" '
                f'style="background-color:{color};">'
                '</div>'
                f'<span>{escape(texto)}</span>'
                '</div>'
            )

        leyenda_html = (
            '<div class="leyenda-mapa">'

            '<div class="leyenda-titulo">'
            'Pérdida acumulada'
            '</div>'

            '<div class="leyenda-descripcion">'
            'Superficie expresada en hectáreas'
            '</div>'

            f'{filas}'

            '</div>'
        )

        st.html(leyenda_html)

        st.caption(
            "Los rangos de colores se mantienen constantes "
            "para todos los años."
        )

        st.info(
            "Pasa el cursor sobre un departamento "
            "para consultar sus datos. Haz clic para "
            "explorar sus provincias."
        )


    # ==================================================
    # 17. CONSTRUIR EL MAPA
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

        # Fondo del mapa y ocultar logo de Leaflet

        mapa.get_root().header.add_child(
            folium.Element("""
                <style>

                    .leaflet-container {
                        background-color: #F4F5F1 !important;
                    }

                    .leaflet-control-attribution {
                        display: none !important;
                    }

                    .leaflet-tooltip {
                        box-shadow: 0 3px 12px
                        rgba(0,0,0,0.12);
                    }

                    .leaflet-tooltip tr:nth-child(3) td {
                        color: #B91C1C;
                        font-weight: bold;
                    }

                    .leaflet-tooltip tr:nth-child(4) td {
                        color: #26734D;
                        font-weight: bold;
                    }

                </style>
            """)
        )

        # Límites departamentales

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

            # Información emergente

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
            padding=(15, 15)
        )

        # Mostrar mapa y recuperar el clic

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
    # 18. RECUPERAR DEPARTAMENTO SELECCIONADO
    # ==================================================

    seleccion = resultado_mapa.get(
        "last_object_clicked_popup"
    )

    departamento_elegido = None

    if seleccion:

        texto = re.sub(
            r"<[^>]+>",
            " ",
            str(seleccion)
        )

        texto = normalizar_nombre(
            " ".join(texto.split())
        )

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

    # Guardar la selección

    if departamento_elegido is not None:

        st.session_state["departamento_mapa"] = (
            departamento_elegido
        )

    departamento_elegido = st.session_state.get(
        "departamento_mapa"
    )


    # ==================================================
    # 19. INFORMACIÓN DEPARTAMENTAL
    # ==================================================

    with col_detalle:

        st.markdown("### Departamento seleccionado")

        if departamento_elegido is None:

            st.info(
                "Selecciona un departamento del mapa "
                "para visualizar sus indicadores."
            )

        elif departamento_elegido not in departamentos_estudiados:

            st.html(
                '<div class="nombre-departamento">'
                f'{escape(departamento_elegido.title())}'
                '</div>'
            )

            st.warning(
                "Este departamento no forma parte "
                "del ámbito de estudio."
            )

        else:

            st.html(
                '<div class="nombre-departamento">'
                f'{escape(departamento_elegido.title())}'
                '</div>'

                '<div class="periodo-departamento">'
                f'Periodo 2001–{anio}'
                '</div>'
            )

            tarjeta(
                "Pérdida acumulada de bosque",
                formato_hectareas(
                    perdidas.get(departamento_elegido)
                ),
                color="#B91C1C"
            )

            tarjeta(
                f"Cobertura forestal en {anio}",
                formato_hectareas(
                    cobertura.get(departamento_elegido)
                ),
                color="#26734D"
            )

            provincias_monitoreadas = df_periodo[
                df_periodo["DEPARTAMENTO"]
                == departamento_elegido
            ]["PROVINCIA"].nunique()

            tarjeta(
                "Provincias monitoreadas",
                provincias_monitoreadas
            )


    # ==================================================
    # 20. ANÁLISIS PROVINCIAL
    # ==================================================

    subtitulo("03 / ANÁLISIS PROVINCIAL")

    if departamento_elegido is None:

        st.info(
            "Haz clic sobre un departamento del mapa "
            "para visualizar la pérdida acumulada "
            "de sus provincias."
        )

    elif departamento_elegido not in departamentos_estudiados:

        st.warning(
            f"{departamento_elegido.title()} no forma "
            "parte del ámbito de estudio de esta "
            "base de datos."
        )

    else:

        st.markdown(
            f"### {departamento_elegido.title()}"
        )

        st.markdown(
            f"**Periodo acumulado: 2001 – {anio}**"
        )

        # Filtrar departamento

        df_departamento = df_periodo[
            df_periodo["DEPARTAMENTO"]
            == departamento_elegido
        ]

        # Agrupar por provincias

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
            # 21. TARJETAS PROVINCIALES
            # ==========================================

            col1, col2, col3 = st.columns(3)

            with col1:

                tarjeta(
                    "Provincias con datos de pérdida",
                    total_provincias
                )

            with col2:

                tarjeta(
                    "Pérdida acumulada",
                    formato_hectareas(perdida_total),
                    color="#B91C1C"
                )

            with col3:

                tarjeta(
                    "Provincia con mayor pérdida",
                    provincia_mayor.title()
                )


            # ==========================================
            # 22. GRÁFICO PROVINCIAL
            # ==========================================

            st.markdown(
                "### Distribución de la pérdida por provincia"
            )

            st.caption(
                "Provincias ordenadas de mayor a menor "
                "pérdida acumulada de bosque."
            )

            provincias = provincias.copy()

            provincias["PROVINCIA"] = (
                provincias["PROVINCIA"].str.title()
            )

            provincias["HECTAREAS"] = (
                provincias["PERDIDA_BOSQUE"]
                .apply(formato_hectareas)
            )

            base = alt.Chart(provincias).encode(

                x=alt.X(
                    "PERDIDA_BOSQUE:Q",
                    title="Pérdida acumulada (ha)",
                    axis=alt.Axis(
                        format=",.0f",
                        grid=True,
                        labelColor="#243B2B",
                        titleColor="#243B2B"
                    )
                ),

                y=alt.Y(
                    "PROVINCIA:N",
                    title="Provincia",
                    sort="-x",
                    axis=alt.Axis(
                        labelLimit=350,
                        labelFontSize=12,
                        labelColor="#243B2B",
                        titleColor="#243B2B"
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
            )

            barras = base.mark_bar(
                color="#078B3D",
                cornerRadiusEnd=4,
                size=28
            )

            grafico = barras.properties(
                height=max(
                    300,
                    len(provincias) * 45
                ),
                background="#FFFFFF"
            ).configure_view(
                strokeWidth=0
            ).configure_axis(
                gridColor="#E4E9E2"
            )

            st.altair_chart(
                grafico,
                use_container_width=True
            )


            # ==========================================
            # 23. INTERPRETACIÓN AUTOMÁTICA
            # ==========================================

            if perdida_total > 0:

                porcentaje = (
                    perdida_provincia_mayor
                    / perdida_total
                ) * 100

                interpretacion = (
                    '<div class="interpretacion-mapa">'

                    '<strong>'
                    'INTERPRETACIÓN DE LOS RESULTADOS'
                    '</strong>'

                    '<br><br>'

                    'La provincia de '

                    '<strong>'
                    f'{escape(provincia_mayor.title())}'
                    '</strong>'

                    ' registra una pérdida acumulada de '

                    '<strong>'
                    f'{formato_hectareas(perdida_provincia_mayor)}'
                    '</strong>'

                    ', lo que representa el '

                    '<strong>'
                    f'{porcentaje:.2f}%'
                    '</strong>'

                    ' de la pérdida provincial registrada en '

                    '<strong>'
                    f'{escape(departamento_elegido.title())}'
                    '</strong>'

                    f' durante el periodo 2001–{anio}.'

                    '</div>'
                )

                st.html(interpretacion)


    # ==================================================
    # 24. METODOLOGÍA Y FUENTES
    # ==================================================

    subtitulo("04 / METODOLOGÍA Y FUENTES")

    with st.expander("Metodología de cálculo"):

        st.markdown("""
**Pérdida acumulada de bosque**

Corresponde a la suma de las hectáreas de bosque
perdido desde el año 2001 hasta el año seleccionado.

**Cobertura forestal existente**

Corresponde a la superficie de bosque registrada
en el año seleccionado, tomando como línea base
el año 2000.

**Clasificación cartográfica**

Los rangos de colores constituyen una clasificación
propia para fines de visualización. Estos rangos
permanecen constantes durante todo el periodo de
análisis.

**Departamentos en gris**

Representan departamentos fuera del ámbito de
estudio o sin datos disponibles. No significan
necesariamente ausencia de pérdida de bosque.

**Análisis provincial**

Los indicadores provinciales se calculan a partir
de los distritos monitoreados incluidos en la
base de datos.
        """)

    with st.expander("Fuentes de información"):

        st.markdown("""
**Fuente de datos**

Ministerio del Ambiente (MINAM).
Monitoreo de la cobertura de bosques a nivel distrital.

**Fuente cartográfica**

Repositorio juaneladio/peru-geojson.
Licencia MPL-2.0.

 """)


# ==================================================
# 25. PRUEBA INDEPENDIENTE
# ==================================================

if __name__ == "__main__":

    st.set_page_config(
        layout="wide",
        page_title="Mapa de pérdida forestal",
        initial_sidebar_state="collapsed"
    )

    mostrar_mapa()