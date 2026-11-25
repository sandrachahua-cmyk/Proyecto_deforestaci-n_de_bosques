import streamlit as st
import plotly.express as px
import streamlit.components.v1 as components
import datos
from bosque import mostrar_bosque
from mapa import mostrar_mapa
from comparacion import mostrar_comparacion
import base64
from textwrap import dedent


# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Bosques del Perú",
    page_icon="assets/hoja.svg",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# ESTILOS GENERALES
# --------------------------------------------------

st.markdown("""
<style>

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .stApp {
        margin: 0;
        padding: 0;
        background-color: #f4f5f1;
        color: #000000;
    }

    .block-container {
        padding: 25px 4% !important;
        max-width: 100% !important;
    }

    .contenido-seccion {
        min-height: auto;
        padding: 45px 4%;
        background-color: #f4f5f1;
    }

    .etiqueta-seccion {
        color: #000000 !important;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2.5px;
        margin-bottom: 12px;
    }

    .titulo-seccion {
        color: #000000 !important;
        font-size: 32px !important;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .descripcion-seccion {
        color: #000000 !important;
        font-size: 15px !important;
        line-height: 1.6;
        max-width: 800px;
    }

    div[data-testid="stWidgetLabel"] p {
        color: #000000 !important;
    }

    div.stButton > button {
        border: 1px solid #526b55;
        background-color: transparent;
        color: #000000;
        border-radius: 4px;
        padding: 8px 18px;
        font-size: 13px;
    }

    div.stButton > button:hover {
        background-color: #e1e9df;
        border-color: #314b36;
        color: #000000;
    }

    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] * {
        color: #000000 !important;
        opacity: 1 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] * {
        color: #000000 !important;
        opacity: 1 !important;
        font-size: 23px !important;
    }

    .stMarkdown h3 {
        font-size: 19px !important;
        color: #000000 !important;
    }

    div[data-baseweb="select"] * {
        color: #000000 !important;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# NAVEGACIÓN
# --------------------------------------------------

if "seccion" not in st.query_params:
    st.query_params["seccion"] = "inicio"

seccion = st.query_params.get("seccion", "inicio")


# --------------------------------------------------
# PORTADA
# --------------------------------------------------

if seccion == "inicio":

    portada = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">

        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            html, body {
                width: 100%;
                height: 100%;
                overflow: hidden;
                font-family: Arial, Helvetica, sans-serif;
            }

            .portada {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                min-height: 100vh;
                overflow: hidden;

                background-image:
                    linear-gradient(
                        rgba(0, 0, 0, 0.42),
                        rgba(0, 0, 0, 0.48)
                    ),
                    url("https://d2ijqnyf2ixq2j.cloudfront.net/media/Peru/Regenwaldfluss-Maeandert-durch-die-gruene-Lunge-Peru.jpg");

                background-size: cover;
                background-position: center;
            }

            .contenido {
                position: absolute;
                top: 34%;
                left: 8%;
                right: 8%;
                transform: translateY(-30%);
                color: white;
            }

            .logo {
                font-size: 15px;
                font-weight: 700;
                letter-spacing: 5px;
                margin-bottom: 30px;
            }

            .titulo {
                font-size: clamp(34px, 5vw, 65px);
                line-height: 1.12;
                font-weight: 700;
                max-width: 950px;
                margin-bottom: 25px;
            }

            .descripcion {
                font-size: clamp(15px, 1.5vw, 19px);
                line-height: 1.7;
                max-width: 720px;
                color: rgba(255,255,255,0.92);
            }

            .navegacion {
                position: absolute;
                bottom: 7%;
                left: 8%;
                right: 8%;
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 25px;
            }

            .opcion {
                display: flex;
                align-items: center;
                gap: 13px;
                color: white;
                text-decoration: none;
                border-top: 1px solid rgba(255,255,255,0.65);
                padding-top: 18px;
                transition: 0.25s ease;
            }

            .opcion:hover {
                border-top: 2px solid white;
                transform: translateY(-4px);
            }

            .icono {
                width: 27px;
                height: 27px;
                flex-shrink: 0;
            }

            .texto-opcion {
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 1.2px;
                line-height: 1.5;
            }

            @media (max-width: 750px) {

                .contenido {
                    top: 27%;
                }

                .navegacion {
                    grid-template-columns: repeat(3, 1fr);
                    gap: 20px;
                    bottom: 5%;
                }

                .texto-opcion {
                    font-size: 10px;
                }
            }

        </style>
    </head>

    <body>
        <main class="portada">

            <section class="contenido">

                <div class="logo">
                    BOSQUES DEL PERÚ
                </div>

                <h1 class="titulo">
                    Análisis interactivo de la pérdida de bosque
                    húmedo amazónico en el Perú (2001–2022)
                </h1>

                <p class="descripcion">
                    Explora la evolución de la pérdida de bosque húmedo
                    amazónico en el territorio peruano mediante información
                    departamental, comparaciones y visualizaciones interactivas.
                </p>

            </section>

            <nav class="navegacion">

                <a class="opcion" href="/?seccion=bosque" target="_top">

                    <svg class="icono" viewBox="0 0 24 24"
                         fill="none" stroke="currentColor"
                         stroke-width="1.5">

                        <path d="M3 10.5L12 3l9 7.5"/>
                        <path d="M5.5 9.5V21h13V9.5"/>
                        <path d="M9 21v-7h6v7"/>

                    </svg>

                    <span class="texto-opcion">
                        BOSQUE Y PÉRDIDA DE BOSQUE
                    </span>

                </a>

                <a class="opcion" href="/?seccion=mapa" target="_top">

                    <svg class="icono" viewBox="0 0 24 24"
                         fill="none" stroke="currentColor"
                         stroke-width="1.5">

                        <path d="M3 6l6-3 6 3 6-3v15l-6 3-6-3-6 3z"/>
                        <path d="M9 3v15"/>
                        <path d="M15 6v15"/>

                    </svg>

                    <span class="texto-opcion">
                        MAPA DEPARTAMENTAL
                    </span>

                </a>

                <a class="opcion" href="/?seccion=ranking" target="_top">

                    <svg class="icono" viewBox="0 0 24 24"
                         fill="none" stroke="currentColor"
                         stroke-width="1.5">

                        <path d="M4 20V12"/>
                        <path d="M10 20V7"/>
                        <path d="M16 20V3"/>
                        <path d="M22 20H2"/>

                    </svg>

                    <span class="texto-opcion">
                        RANKING DEPARTAMENTAL
                    </span>

                </a>

            </nav>

        </main>
    </body>
    </html>
    """

    st.markdown("""
    <style>
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.html(portada)


# --------------------------------------------------
# BOSQUE Y PÉRDIDA DE BOSQUE
# --------------------------------------------------

elif seccion == "bosque":

    st.markdown("""
    <style>

    .barra-superior {
        background-color: #A66C4B;
        width: 100vw;
        margin-left: calc(50% - 50vw);
        margin-top: -25px;
        padding: 18px 4%;
        box-sizing: border-box;
    }

    .barra-superior a {
        color: white !important;
        text-decoration: none !important;
        font-size: 16px;
        font-weight: bold;
    }

    </style>

    <div class="barra-superior">
        <a href="/?seccion=inicio" target="_top">← Inicio</a>
    </div>
    """, unsafe_allow_html=True)

    mostrar_bosque()


# --------------------------------------------------
# MAPA DEPARTAMENTAL
# --------------------------------------------------

elif seccion == "mapa":

    mostrar_mapa()


# --------------------------------------------------
# RANKING DEPARTAMENTAL Y COMPARACIÓN
# --------------------------------------------------

elif seccion == "ranking":

    # IMAGEN PANORÁMICA Y BARRA SUPERIOR

    with open("assets/bosque/bosque_loreto.jpg", "rb") as archivo:
        imagen_base64 = base64.b64encode(archivo.read()).decode()

    st.html(f"""
    <style>

    .banner-ranking {{
        position: relative;
        width: 100vw;
        height: 380px;
        margin-left: calc(50% - 50vw);
        margin-top: -25px;
        overflow: hidden;
    }}

    .banner-ranking img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
        display: block;
    }}

    .barra-superior {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #A66C4B;
        padding: 18px 4%;
        box-sizing: border-box;
        z-index: 10;
    }}

    .barra-superior a {{
        color: white !important;
        text-decoration: none !important;
        font-size: 16px;
        font-weight: bold;
    }}

    </style>

    <div class="banner-ranking">

        <img src="data:image/jpeg;base64,{imagen_base64}">

        <div class="barra-superior">
            <a href="/?seccion=inicio" target="_top">← Inicio</a>
        </div>

    </div>
    """)


    # ENCABEZADO GENERAL

    st.html("""
    <div style="padding: 15px 0 5px 0;">

        <div style="color: #000000; font-size: 13px;
        letter-spacing: 3px; font-weight: bold;">

            BOSQUES DEL PERÚ / COMPARACIÓN

        </div>

        <h1 style="color: #000000; font-size: 32px; margin: 5px 0;">

            PÉRDIDA DE BOSQUE POR DEPARTAMENTO

        </h1>

        <p style="color: #000000; font-size: 15px; line-height: 1.6;">

            ¿Qué departamentos registran mayor pérdida de bosque?

        </p>

        <p style="color: #000000; font-size: 15px; line-height: 1.6;">

            Explora cómo se distribuye la pérdida de bosque húmedo
            amazónico en los departamentos del Perú entre 2001 y 2022.
            Consulta el ranking anual o compara la evolución acumulada
            de los departamentos.

        </p>

    </div>
    """)


    # ==========================================
    # BOTONES CENTRADOS DE NAVEGACIÓN
    # ==========================================

    st.html("""
    <style>

    .st-key-nav_ranking button,
    .st-key-nav_comparacion button {
        width: 100% !important;
        height: 60px !important;
        min-height: 60px !important;
        border-radius: 6px !important;
        border: 1px solid #D2B48C !important;
        font-weight: 600 !important;
        color: #000000 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 10px !important;
    }

    .st-key-nav_ranking button p,
    .st-key-nav_comparacion button p {
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #000000 !important;
        text-align: center !important;
        margin: 0 !important;
    }

    .st-key-nav_ranking button[kind="primary"],
    .st-key-nav_comparacion button[kind="primary"] {
        background-color: #D2B48C !important;
        border-color: #A66C4B !important;
    }

    .st-key-nav_ranking button[kind="secondary"],
    .st-key-nav_comparacion button[kind="secondary"] {
        background-color: #FFFFFF !important;
    }

    .st-key-nav_ranking button:hover,
    .st-key-nav_comparacion button:hover {
        background-color: #E8D6BF !important;
        border-color: #A66C4B !important;
    }

    </style>
    """)


    # ESTADO DEL APARTADO SELECCIONADO

    if "vista_ranking" not in st.session_state:
        st.session_state["vista_ranking"] = "Ranking anual"


    # COLUMNAS SIMÉTRICAS PARA CENTRAR LOS BOTONES

    espacio1, boton1, boton2, espacio2 = st.columns(
        [1, 3, 3, 1],
        gap="medium"
    )


    # BOTÓN DE RANKING ANUAL

    with boton1:

        if st.button(
            "Ranking anual",
            key="nav_ranking",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state["vista_ranking"] == "Ranking anual"
                else "secondary"
            )
        ):

            st.session_state["vista_ranking"] = "Ranking anual"

            st.rerun()


    # BOTÓN DE COMPARACIÓN ACUMULADA

    with boton2:

        if st.button(
            "Comparación acumulada",
            key="nav_comparacion",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state["vista_ranking"] == "Comparación acumulada"
                else "secondary"
            )
        ):

            st.session_state["vista_ranking"] = "Comparación acumulada"

            st.rerun()


    apartado = st.session_state["vista_ranking"]

    st.divider()


    # ==========================================
    # APARTADO 1: RANKING ANUAL
    # ==========================================

    if apartado == "Ranking anual":

        # CARGAR DATOS

        df = datos.cargar_datos()


        # SELECTOR DE AÑOS

        anios = sorted(df["ANIO"].dropna().unique())

        anio_seleccionado = st.selectbox(
            "Año de análisis:",
            anios
        )


        # OBTENER RANKING

        ranking = datos.obtener_ranking(
            df,
            anio_seleccionado
        )

        ranking = ranking.sort_values(
            ascending=False
        )

        ranking_df = ranking.rename(
            "PERDIDA_BOSQUE"
        ).reset_index()

        ranking_df.columns = [
            "DEPARTAMENTO",
            "PERDIDA_BOSQUE"
        ]


        # INDICADORES

        perdida_total = ranking.sum()

        primer_lugar = ranking.idxmax()

        departamentos_evaluados = ranking.count()


        # ESTILOS DE LAS TARJETAS

        st.html("""
        <style>

        .tarjeta-ranking {
            background: rgba(166, 108, 75, 0.12);
            border: 1px solid rgba(166, 108, 75, 0.25);
            border-radius: 12px;
            padding: 18px;
            height: 120px;
            box-sizing: border-box;
        }

        .titulo-tarjeta-ranking {
            color: #000000;
            font-size: 12px;
            font-weight: 600;
        }

        .valor-tarjeta-ranking {
            color: #000000;
            font-size: 21px;
            margin-top: 8px;
        }

        </style>
        """)


        # ==========================================
        # TARJETAS DE INDICADORES
        # ==========================================

        col1, col2, col3, col4 = st.columns(4)


        # TARJETA 1: PÉRDIDA TOTAL

        with col1:

            st.markdown(dedent(f"""
            <div class="tarjeta-ranking">
            <div class="titulo-tarjeta-ranking">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:5px;">
            <path d="M12 22v-7"/>
            <path d="M5 12a7 7 0 1 1 14 0c0 3-3 5-7 5s-7-2-7-5Z"/>
            <path d="M8 10c1 1 2 1 4 1s3 0 4-1"/>
            </svg>
            PÉRDIDA TOTAL
            </div>
            <div class="valor-tarjeta-ranking">
            {perdida_total:,.0f} ha
            </div>
            </div>
            """).strip(), unsafe_allow_html=True)


        # TARJETA 2: PRIMER LUGAR

        with col2:

            st.markdown(dedent(f"""
            <div class="tarjeta-ranking">
            <div class="titulo-tarjeta-ranking">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:5px;">
            <path d="M8 21h8"/>
            <path d="M12 17v4"/>
            <path d="M7 4h10v5a5 5 0 0 1-10 0V4Z"/>
            <path d="M7 6H4v2a4 4 0 0 0 4 4"/>
            <path d="M17 6h3v2a4 4 0 0 1-4 4"/>
            </svg>
            PRIMER LUGAR
            </div>
            <div class="valor-tarjeta-ranking">
            {primer_lugar}
            </div>
            </div>
            """).strip(), unsafe_allow_html=True)


        # TARJETA 3: DEPARTAMENTOS EVALUADOS

        with col3:

            st.markdown(dedent(f"""
            <div class="tarjeta-ranking">
            <div class="titulo-tarjeta-ranking">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:5px;">
            <rect x="4" y="4" width="16" height="16" rx="2"/>
            <path d="M8 9h8M8 13h8M8 17h5"/>
            </svg>
            DEPARTAMENTOS EVALUADOS
            </div>
            <div class="valor-tarjeta-ranking">
            {departamentos_evaluados}
            </div>
            </div>
            """).strip(), unsafe_allow_html=True)


        # TARJETA 4: UNIDAD DE ANÁLISIS

        with col4:

            st.markdown(dedent("""
            <div class="tarjeta-ranking">
            <div class="titulo-tarjeta-ranking">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:5px;">
            <path d="M12 22V12"/>
            <path d="M12 15C5 15 3 10 3 5c5 0 9 2 9 7"/>
            <path d="M12 12c0-5 3-8 9-8 0 5-2 9-9 9"/>
            </svg>
            UNIDAD DE ANÁLISIS
            </div>
            <div class="valor-tarjeta-ranking">
            Hectáreas (ha)
            </div>
            </div>
            """).strip(), unsafe_allow_html=True)


        # ==========================================
        # GRÁFICO DE DONA
        # ==========================================

        st.markdown(
            f"### Participación de la pérdida por departamento ({anio_seleccionado})"
        )

        fig_dona = px.pie(
            ranking_df,
            names="DEPARTAMENTO",
            values="PERDIDA_BOSQUE",
            hole=0.55
        )

        fig_dona.update_traces(

            textposition="inside",

            textinfo="percent",

            textfont=dict(
                color="#ffffff"
            ),

            hovertemplate=(
                "<b>%{label}</b><br>"
                "Pérdida: %{value:,.2f} ha<br>"
                "Participación: %{percent}"
                "<extra></extra>"
            )
        )

        fig_dona.update_layout(

            template="plotly_white",

            colorway=[
                "#064b27",
                "#078b3d",
                "#28b84c",
                "#65cc70",
                "#a1dfa1",
                "#c8efc8"
            ],

            showlegend=True,

            paper_bgcolor="#ffffff",

            plot_bgcolor="#ffffff",

            font=dict(
                color="#243b2b"
            ),

            legend=dict(
                font=dict(
                    color="#243b2b",
                    size=11
                )
            ),

            height=480,

            margin=dict(
                t=20,
                b=20,
                l=20,
                r=20
            ),

            separators=",."
        )

        st.plotly_chart(
            fig_dona,
            use_container_width=True
        )


        # ==========================================
        # GRÁFICO DE BARRAS HORIZONTAL
        # ==========================================

        st.markdown(
            f"### Pérdida de bosque por departamento ({anio_seleccionado})"
        )

        fig = px.bar(

            ranking_df,

            x="PERDIDA_BOSQUE",

            y="DEPARTAMENTO",

            orientation="h",

            labels={
                "PERDIDA_BOSQUE": "Pérdida de bosque (ha)",
                "DEPARTAMENTO": "Departamento"
            }
        )

        fig.update_layout(

            template="plotly_white",

            yaxis={
                "autorange": "reversed"
            },

            colorway=["#078b3d"],

            paper_bgcolor="#ffffff",

            plot_bgcolor="#ffffff",

            font=dict(
                color="#243b2b"
            ),

            height=480,

            separators=",.",

            margin=dict(
                t=20,
                b=35,
                l=20,
                r=20
            )
        )

        fig.update_yaxes(

            tickfont=dict(
                color="#243b2b",
                size=11
            ),

            title_font=dict(
                color="#243b2b"
            )
        )

        fig.update_xaxes(

            tickfont=dict(
                color="#243b2b",
                size=11
            ),

            title_font=dict(
                color="#243b2b"
            ),

            title_text="Pérdida de bosque (ha)",

            tickformat=",.0f"
        )

        fig.update_traces(

            marker_color="#078b3d",

            hovertemplate=(
                "<b>Departamento:</b> %{y}<br>"
                "<b>Pérdida de bosque:</b> %{x:,.2f} ha"
                "<extra></extra>"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ==========================================
    # APARTADO 2: COMPARACIÓN ACUMULADA
    # ==========================================

    elif apartado == "Comparación acumulada":

        mostrar_comparacion()


# --------------------------------------------------
# CONTROL DE SECCIONES NO RECONOCIDAS
# --------------------------------------------------

else:

    st.query_params["seccion"] = "inicio"

    st.rerun()