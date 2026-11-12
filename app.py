
import streamlit as st
import streamlit.components.v1 as components
import datos
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
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    .contenido-seccion {
        min-height: 100vh;
        padding: 65px 8%;
        background-color: #f4f5f1;
    }

    .etiqueta-seccion {
        color: #66816b;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 3px;
        margin-bottom: 15px;
    }

    .titulo-seccion {
        color: #243b2b;
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .descripcion-seccion {
        color: #59645b;
        font-size: 17px;
        line-height: 1.7;
        max-width: 800px;
    }

    div.stButton > button {
        border: 1px solid #526b55;
        background-color: transparent;
        color: #314b36;
        border-radius: 4px;
        padding: 10px 22px;
    }

    div.stButton > button:hover {
        background-color: #e1e9df;
        border-color: #314b36;
        color: #243b2b;
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
                position: relative;
                width: 100%;
                height: 100vh;
                min-height: 600px;
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
                grid-template-columns: repeat(4, 1fr);
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
                    grid-template-columns: repeat(2, 1fr);
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

                <a class="opcion" href="?seccion=inicio" target="_blank">
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

                <a class="opcion" href="?seccion=mapa" target="_blank">
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

                <a class="opcion" href="?seccion=ranking" target="_blank">
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

                <a class="opcion" href="?seccion=evolucion" target="_blank">
                    <svg class="icono" viewBox="0 0 24 24"
                         fill="none" stroke="currentColor"
                         stroke-width="1.5">
                        <path d="M3 19V5"/>
                        <path d="M3 19h19"/>
                        <path d="M5 15l5-5 4 3 7-8"/>
                    </svg>
                    <span class="texto-opcion">
                        EVOLUCIÓN ANUAL
                    </span>
                </a>

            </nav>

        </main>
    </body>
    </html>
    """

    components.html(
        portada,
        height=760,
        scrolling=False
    )


# --------------------------------------------------
# MAPA DEPARTAMENTAL
# --------------------------------------------------

elif seccion == "mapa":

    st.markdown("""
    <div class="contenido-seccion">
        <div class="etiqueta-seccion">BOSQUES DEL PERÚ / EXPLORACIÓN</div>
        <div class="titulo-seccion">Mapa departamental</div>
        <div class="descripcion-seccion">
            Explora la distribución territorial de la pérdida de bosque
            húmedo amazónico en los departamentos del Perú durante el
            periodo 2001–2022.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Volver a la portada"):
        st.query_params["seccion"] = "inicio"
        st.rerun()

    st.info(
        "En esta sección incorporaremos el mapa interactivo, "
        "el selector de departamentos y la información provincial."
    )


# --------------------------------------------------
# RANKING DEPARTAMENTAL
# --------------------------------------------------

elif seccion == "ranking":

    st.markdown("""
    <div class="contenido-seccion">
        <div class="etiqueta-seccion">BOSQUES DEL PERÚ / COMPARACIÓN</div>
        <div class="titulo-seccion">Ranking departamental</div>
        <div class="descripcion-seccion">
            Identifica los departamentos con mayores registros de pérdida
            de bosque húmedo amazónico y compara sus valores por año.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Volver a la portada"):
        st.query_params["seccion"] = "inicio"
        st.rerun()

    # Cargar los datos
    df = datos.cargar_datos()

    # Seleccionar el año
    anios = sorted(df["ANIO"].dropna().unique())

    anio_seleccionado = st.selectbox(
        "Selecciona el año:",
        anios
    )
    # Obtener el ranking del año seleccionado
    ranking = datos.obtener_ranking(df, anio_seleccionado)

    # Título del gráfico
    st.subheader(
    f"Pérdida de bosque por departamento - {anio_seleccionado}"
    )

    # Gráfico de barras horizontal
    st.bar_chart(
    ranking,
    horizontal=True
    )

# --------------------------------------------------
# EVOLUCIÓN ANUAL
# --------------------------------------------------

elif seccion == "evolucion":

    st.markdown("""
    <div class="contenido-seccion">
        <div class="etiqueta-seccion">BOSQUES DEL PERÚ / TENDENCIAS</div>
        <div class="titulo-seccion">Evolución anual</div>
        <div class="descripcion-seccion">
            Analiza cómo ha cambiado la pérdida de bosque húmedo amazónico
            a lo largo del periodo 2001–2022 y compara la evolución
            entre distintos departamentos.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Volver a la portada"):
        st.query_params["seccion"] = "inicio"
        st.rerun()

    st.info(
        "En esta sección incorporaremos los gráficos de evolución "
        "anual y la comparación entre departamentos."
    )


# --------------------------------------------------
# CONTROL DE SECCIONES NO RECONOCIDAS
# --------------------------------------------------

else:
    st.query_params["seccion"] = "inicio"
    st.rerun()
