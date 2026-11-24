
import streamlit as st
from pathlib import Path
from html import escape

from datos import cargar_datos, obtener_resumen_general


# ==================================================
# 1. CONFIGURACIÓN DE IMÁGENES
# ==================================================

CARPETA_IMAGENES = Path(__file__).resolve().parent / "assets" / "bosque"


def buscar_imagen(nombre):

    archivo = CARPETA_IMAGENES / nombre

    if archivo.is_file():
        return archivo

    nombre_base = Path(nombre).stem

    for extension in [".jpg", ".jpeg", ".png", ".webp"]:

        archivo = CARPETA_IMAGENES / f"{nombre_base}{extension}"

        if archivo.is_file():
            return archivo

    return None


def mostrar_fotografia(nombre, tipo="tarjeta"):

    archivo = buscar_imagen(nombre)

    if archivo is None:
        st.warning(f"No se encontró la imagen: {nombre}")
        return

    with st.container(key=f"imagen_{tipo}_{Path(nombre).stem}"):
        st.image(str(archivo), use_container_width=True)


# ==================================================
# 2. TARJETAS ECOLÓGICAS
# ==================================================

def mostrar_tarjeta(numero, titulo, descripcion, detalle, imagen):

    with st.container(border=True):

        mostrar_fotografia(imagen)

        st.markdown(
            f'<div class="numero-tarjeta">'
            f'{escape(numero)} / ECOLOGÍA FORESTAL'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="titulo-tarjeta">'
            f'{escape(titulo)}'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="descripcion-tarjeta">'
            f'{escape(descripcion)}'
            f'</div>',
            unsafe_allow_html=True
        )

        with st.expander("Explorar el proceso ecológico"):
            st.write(detalle)


# ==================================================
# 3. INDICADORES ESTADÍSTICOS
# ==================================================

def mostrar_indicador(etiqueta, valor, nota):

    st.markdown(
        f"""
        <div class="indicador">
            <div class="indicador-etiqueta">
                {escape(str(etiqueta))}
            </div>
            <div class="indicador-valor">
                {escape(str(valor))}
            </div>
            <div class="indicador-nota">
                {escape(str(nota))}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# 4. CONSECUENCIAS AMBIENTALES
# ==================================================

def mostrar_consecuencias():

    consecuencias = [
        {
            "titulo": "Alteración del ciclo del carbono",
            "imagen": "carbono.png",
            "descripcion": (
                "La eliminación de la cobertura forestal modifica "
                "los flujos y las reservas de carbono del ecosistema."
            ),
            "proceso": (
                "La vegetación incorpora dióxido de carbono mediante "
                "la fotosíntesis y almacena carbono en su biomasa. "
                "Cuando el bosque se tala o quema, parte de ese carbono "
                "puede liberarse a la atmósfera."
            ),
            "impacto": (
                "La reducción de las reservas de carbono y las emisiones "
                "asociadas a la pérdida de biomasa pueden contribuir "
                "al cambio climático."
            )
        },
        {
            "titulo": "Alteración de los sistemas hídricos",
            "imagen": "agua_impacto.png",
            "descripcion": (
                "La pérdida de vegetación puede modificar la infiltración, "
                "la escorrentía y el transporte de sedimentos."
            ),
            "proceso": (
                "La cobertura forestal intercepta parte de la lluvia "
                "y contribuye a regular el movimiento del agua. "
                "Su eliminación puede incrementar la escorrentía superficial "
                "y favorecer el arrastre de partículas del suelo."
            ),
            "impacto": (
                "Estos cambios pueden alterar la calidad del agua "
                "y las condiciones de los ecosistemas acuáticos."
            )
        },
        {
            "titulo": "Pérdida de biodiversidad",
            "imagen": "habitat.png",
            "descripcion": (
                "La deforestación reduce y fragmenta los hábitats "
                "de numerosas especies."
            ),
            "proceso": (
                "La fragmentación puede separar poblaciones y modificar "
                "la conectividad entre áreas de bosque. "
                "También puede aumentar los efectos de borde."
            ),
            "impacto": (
                "Estos procesos pueden afectar el desplazamiento, "
                "la reproducción y la persistencia de las especies."
            )
        },
        {
            "titulo": "Degradación y erosión del suelo",
            "imagen": "erosion.png",
            "descripcion": (
                "La pérdida de cobertura vegetal puede aumentar "
                "la vulnerabilidad del suelo frente a la erosión."
            ),
            "proceso": (
                "La vegetación amortigua el impacto de la lluvia "
                "y sus raíces contribuyen a estabilizar el suelo. "
                "Cuando se elimina, el suelo puede quedar más expuesto "
                "al desprendimiento y transporte de partículas."
            ),
            "impacto": (
                "La erosión puede provocar pérdida de suelo fértil, "
                "reducción de la capacidad productiva y sedimentación "
                "de cuerpos de agua."
            )
        }
    ]

    st.divider()

    st.markdown(
        '<div class="etiqueta">05 / IMPACTOS AMBIENTALES</div>',
        unsafe_allow_html=True
    )

    st.header("Consecuencias de la pérdida de bosque")

    st.write(
        "Selecciona una fotografía para explorar los procesos "
        "ecológicos asociados a la pérdida de cobertura forestal."
    )

    if "consecuencia_seleccionada" not in st.session_state:
        st.session_state.consecuencia_seleccionada = None

    columnas = st.columns(4, gap="small")

    for indice, consecuencia in enumerate(consecuencias):

        with columnas[indice]:

            imagen = buscar_imagen(consecuencia["imagen"])

            if imagen is not None:

                with st.container(
                    key=f"mosaico_consecuencia_{indice}"
                ):

                    st.image(
                        str(imagen),
                        use_container_width=True
                    )

            else:

                st.warning(
                    f"Falta la imagen: {consecuencia['imagen']}"
                )

            if st.button(
                consecuencia["titulo"],
                key=f"consecuencia_{indice}",
                use_container_width=True
            ):

                st.session_state.consecuencia_seleccionada = indice

    seleccion = st.session_state.consecuencia_seleccionada

    if seleccion is not None:

        consecuencia = consecuencias[seleccion]

        st.write("")

        with st.container(border=True):

            col_imagen, col_info = st.columns(
                [1, 1.2],
                gap="large"
            )

            with col_imagen:

                imagen = buscar_imagen(consecuencia["imagen"])

                if imagen is not None:

                    st.image(
                        str(imagen),
                        use_container_width=True
                    )

            with col_info:

                st.subheader(consecuencia["titulo"])

                st.write(consecuencia["descripcion"])

                st.markdown("**¿Qué proceso ocurre?**")
                st.write(consecuencia["proceso"])

                st.markdown("**¿Cuáles son sus impactos?**")
                st.write(consecuencia["impacto"])

                if st.button(
                    "Cerrar información",
                    key="cerrar_consecuencia"
                ):

                    st.session_state.consecuencia_seleccionada = None
                    st.rerun()


# ==================================================
# 5. CONSERVACIÓN Y SOLUCIONES
# ==================================================

def mostrar_conservacion():

    st.divider()

    st.markdown(
        '<div class="etiqueta">06 / CONSERVACIÓN Y SOLUCIONES</div>',
        unsafe_allow_html=True
    )

    st.header("¿Cómo podemos proteger nuestros bosques?")

    st.write(
        "La conservación de los bosques amazónicos del Perú "
        "requiere estrategias que integren la protección de "
        "los ecosistemas, el desarrollo económico sostenible "
        "y la participación de las comunidades locales."
    )

    estrategias = [
        {
            "titulo": "Restauración forestal",
            "imagen": "restauracion.png",
            "descripcion": (
                "Recuperar los ecosistemas degradados mediante "
                "la regeneración natural y el establecimiento "
                "de especies nativas, favoreciendo la biodiversidad "
                "y las funciones ecológicas del bosque."
            )
        },
        {
            "titulo": "Producción sostenible",
            "imagen": "agroforesteria.png",
            "descripcion": (
                "Promover sistemas agroforestales, como el cultivo "
                "de cacao y café bajo sombra, generando alternativas "
                "económicas que reduzcan la presión sobre los bosques."
            )
        },
        {
            "titulo": "Participación comunitaria",
            "imagen": "comunidades.png",
            "descripcion": (
                "Fortalecer la gestión territorial de las comunidades "
                "indígenas y locales, reconociendo sus conocimientos "
                "y su participación en la conservación de los "
                "recursos forestales."
            )
        },
        {
            "titulo": "Monitoreo y fiscalización",
            "imagen": "monitoreo.png",
            "descripcion": (
                "Utilizar tecnologías satelitales para detectar "
                "cambios en la cobertura forestal y orientar "
                "las acciones de vigilancia y fiscalización ambiental."
            )
        }
    ]

    for fila in range(0, len(estrategias), 2):

        columnas = st.columns(2, gap="large")

        for columna, estrategia in zip(
            columnas, estrategias[fila:fila + 2]
        ):

            with columna:

                with st.container(border=True):

                    mostrar_fotografia(
                        estrategia["imagen"],
                        tipo="conservacion"
                    )

                    st.markdown(
                        f'<div class="titulo-conservacion">'
                        f'{escape(estrategia["titulo"])}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f'<div class="descripcion-conservacion">'
                        f'{escape(estrategia["descripcion"])}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

        st.write("")

    st.divider()

    with st.container(border=True):

        st.subheader("Conservación y monitoreo en el Perú")

        st.write(
            "La plataforma GeoBosques del Ministerio del Ambiente "
            "permite consultar información sobre la cobertura "
            "forestal, la pérdida de bosque y las alertas "
            "tempranas de deforestación."
        )

        st.link_button(
            "Explorar la plataforma GeoBosques",
            "https://geobosques.minam.gob.pe/"
        )


# ==================================================
# 6. PÁGINA PRINCIPAL
# ==================================================

def mostrar_bosque():

    # ==============================================
    # ESTILOS GENERALES
    # ==============================================

    st.markdown("""
    <style>

    /* Fondo general */

    .stApp {
        background-color: #F4F1E9;
    }

    /* Contenedor principal */

    .block-container {
        max-width: 1250px;
        padding-top: 3rem;
        padding-bottom: 5rem;
    }

    /* Títulos */

    h1, h2, h3 {
        color: #000000 !important;
        letter-spacing: -0.5px;
    }

    h1 {
        font-size: 3rem !important;
        font-weight: 750 !important;
    }

    h2 {
        font-weight: 700 !important;
    }

    /* Párrafos */

    p {
        color: #000000 !important;
        line-height: 1.7;
    }

    /* Etiquetas */

    .etiqueta {
        color: #000000;
        font-size: 0.78rem;
        font-weight: 750;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    /* ==========================================
       FOTOGRAFÍAS DE LAS TARJETAS ECOLÓGICAS
       ========================================== */

    .st-key-imagen_tarjeta_clima img,
    .st-key-imagen_tarjeta_hidrografico img,
    .st-key-imagen_tarjeta_biodiversidad img,
    .st-key-imagen_tarjeta_suelo img {
        width: 100% !important;
        height: 260px !important;
        object-fit: cover !important;
        object-position: center !important;
        border-radius: 12px;
    }

    /* ==========================================
       FOTOGRAFÍAS DE CONSECUENCIAS
       ========================================== */

    .st-key-mosaico_consecuencia_0 img,
    .st-key-mosaico_consecuencia_1 img,
    .st-key-mosaico_consecuencia_2 img,
    .st-key-mosaico_consecuencia_3 img {
        width: 100% !important;
        height: 205px !important;
        object-fit: cover !important;
        object-position: center !important;
        border-radius: 12px;
    }

    /* ==========================================
       FOTOGRAFÍAS DE CONSERVACIÓN
       TODAS CON EL MISMO TAMAÑO
       ========================================== */

    .st-key-imagen_conservacion_restauracion img,
    .st-key-imagen_conservacion_agroforesteria img,
    .st-key-imagen_conservacion_comunidades img,
    .st-key-imagen_conservacion_monitoreo img {
        width: 100% !important;
        height: 230px !important;
        object-fit: cover !important;
        object-position: center !important;
        border-radius: 12px;
    }

    /* Títulos de conservación */

    .titulo-conservacion {
        color: #000000;
        font-size: 1.4rem;
        font-weight: 750;
        margin-top: 12px;
        margin-bottom: 12px;
    }

    /* Descripciones de conservación */

    .descripcion-conservacion {
        color: #000000;
        font-size: 0.98rem;
        line-height: 1.7;
        min-height: 145px;
        margin-bottom: 10px;
    }

    /* Botones de consecuencias */

    .st-key-consecuencia_0 button,
    .st-key-consecuencia_1 button,
    .st-key-consecuencia_2 button,
    .st-key-consecuencia_3 button {
        min-height: 52px;
        border-radius: 10px;
        background-color: #FFFEFA;
        color: #203C32;
        border: 1px solid #D8DDD2;
    }

    .st-key-consecuencia_0 button:hover,
    .st-key-consecuencia_1 button:hover,
    .st-key-consecuencia_2 button:hover,
    .st-key-consecuencia_3 button:hover {
        background-color: #E8ECE3;
        border-color: #526B52;
    }

    /* Fotografía de portada */

    .st-key-imagen_portada_portada img {
        width: 100% !important;
        height: 350px !important;
        object-fit: cover !important;
        border-radius: 12px;
    }

    /* Tarjetas */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFEFA;
        border: 1px solid #E1E3DA;
        border-radius: 18px;
        box-shadow: 0 4px 15px rgba(32, 60, 50, 0.04);
    }

    /* Numeración */

    .numero-tarjeta {
        color: #000000;
        font-size: 0.76rem;
        font-weight: 750;
        letter-spacing: 1.3px;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    /* Títulos de tarjetas */

    .titulo-tarjeta {
        color: #000000;
        font-size: 1.4rem;
        font-weight: 750;
        margin-bottom: 12px;
    }

    /* Descripciones */

    .descripcion-tarjeta {
        color: #000000;
        font-size: 0.98rem;
        line-height: 1.7;
        min-height: 65px;
        margin-bottom: 18px;
    }

    /* Desplegables */

    [data-testid="stExpander"] {
        border-radius: 10px;
    }

    /* Indicadores estadísticos */

    .indicador {
        background: #FFFEFA;
        border: 1px solid #E1E3DA;
        border-radius: 16px;
        padding: 28px 20px;
        min-height: 190px;
        box-shadow: 0 4px 15px rgba(32, 60, 50, 0.04);
    }

    .indicador-etiqueta {
        color: #000000;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .indicador-valor {
        color: #000000;
        font-size: clamp(1.7rem, 3vw, 2.5rem);
        font-weight: 800;
        margin: 16px 0 12px;
    }

    .indicador-nota {
        color: #000000;
        font-size: 0.88rem;
        line-height: 1.5;
    }

    /* Separadores */

    hr {
        border-color: #D8DDD2 !important;
    }

    </style>
    """, unsafe_allow_html=True)

    # ==============================================
    # ENCABEZADO
    # ==============================================

    st.markdown(
        '<div class="etiqueta">'
        'PERÚ / 2001—2022 / ANÁLISIS AMBIENTAL'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<h1 style="color: #000000 !important;">BOSQUES AMAZÓNICOS</h1>',
        unsafe_allow_html=True
    )

    st.markdown(
        "### Dinámica de la pérdida de cobertura forestal en el Perú"
    )

    st.write(
        "Una exploración de la importancia ecológica de los "
        "bosques húmedos amazónicos y de los cambios "
        "registrados en su cobertura."
    )

    st.write("")

    # ==============================================
    # 01. INTRODUCCIÓN
    # ==============================================

    col_imagen, col_texto = st.columns(
        [1.2, 1],
        gap="large"
    )

    with col_imagen:

        mostrar_fotografia(
            "portada.jpg",
            tipo="portada"
        )

        st.caption(
            "."
            "cobertura de bosque"
        )

    with col_texto:

        st.markdown(
            '<div class="etiqueta">01 / EL ECOSISTEMA</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "El bosque húmedo amazónico del Perú"
        )

        st.write("""
        El bosque húmedo amazónico constituye uno de los
        ecosistemas de mayor importancia ecológica del
        territorio peruano.

        Su estructura vegetal y diversidad biológica
        permiten el desarrollo de procesos esenciales
        para el funcionamiento de los ecosistemas.

        Entre ellos destacan la regulación del ciclo
        del carbono, la dinámica hidrológica y
        la conservación de la biodiversidad.
        """)

    # ==============================================
    # 02. IMPORTANCIA ECOLÓGICA
    # ==============================================

    st.divider()

    st.markdown(
        '<div class="etiqueta">'
        '02 / SERVICIOS ECOSISTÉMICOS'
        '</div>',
        unsafe_allow_html=True
    )

    st.header(
        "¿Por qué son importantes los bosques?"
    )

    st.write(
        "Explora cuatro funciones ecológicas fundamentales "
        "de los bosques húmedos amazónicos."
    )

    st.write("")

    # PRIMERA FILA

    col1, col2 = st.columns(
        2,
        gap="medium"
    )

    with col1:

        mostrar_tarjeta(
            "01",
            "Regulación climática",
            "Los bosques almacenan carbono en su vegetación "
            "y suelos, contribuyendo a la regulación del clima.",
            """
            Mediante la fotosíntesis, la vegetación incorpora
            dióxido de carbono atmosférico y almacena carbono
            en su biomasa.

            La pérdida de cobertura forestal puede provocar
            emisiones de carbono y reducir las reservas
            almacenadas en el ecosistema.
            """,
            "clima.jpg"
        )

    with col2:

        mostrar_tarjeta(
            "02",
            "Ciclo hidrológico",
            "La vegetación participa en la evapotranspiración "
            "y el reciclaje de humedad atmosférica.",
            """
            Los bosques intervienen en la interceptación
            de precipitaciones, la infiltración del agua
            y la evapotranspiración.

            Estos procesos influyen en el balance hídrico
            y en la dinámica regional de la humedad.
            """,
            "hidrografico.jpg"
        )

    st.write("")

    # SEGUNDA FILA

    col3, col4 = st.columns(
        2,
        gap="medium"
    )

    with col3:

        mostrar_tarjeta(
            "03",
            "Biodiversidad",
            "Los bosques amazónicos proporcionan hábitats "
            "para numerosas especies de flora y fauna.",
            """
            La diversidad estructural del bosque
            favorece múltiples interacciones ecológicas.

            La fragmentación de los hábitats puede
            reducir la conectividad y afectar
            a las poblaciones de especies.
            """,
            "biodiversidad.jpg"
        )

    with col4:

        mostrar_tarjeta(
            "04",
            "Protección del suelo",
            "La cobertura vegetal contribuye a limitar "
            "la erosión y favorece el reciclaje de nutrientes.",
            """
            La vegetación reduce el impacto directo
            de las precipitaciones sobre el suelo.

            Los sistemas radiculares contribuyen
            a su estabilidad, mientras que la hojarasca
            participa en el mantenimiento de la
            materia orgánica.
            """,
            "suelo.jpg"
        )

    # ==============================================
    # 03. INDICADORES ESTADÍSTICOS
    # ==============================================

    st.divider()

    st.markdown(
        '<div class="etiqueta">'
        '03 / EVIDENCIA ESTADÍSTICA'
        '</div>',
        unsafe_allow_html=True
    )

    st.header(
        "La pérdida de bosque en cifras"
    )

    st.write(
        "Indicadores calculados a partir de los registros "
        "de pérdida de bosque correspondientes al "
        "período 2001–2022."
    )

    # Cargar datos

    df = cargar_datos()

    # Calcular estadísticas

    perdida_total, anio_maximo, departamento_maximo = (
        obtener_resumen_general(df)
    )

    # Convertir hectáreas a millones

    perdida_millones = perdida_total / 1_000_000

    # Crear columnas

    col_a, col_b, col_c = st.columns(
        3,
        gap="medium"
    )

    with col_a:

        mostrar_indicador(
            "Pérdida acumulada",
            f"{perdida_millones:.2f} M ha",
            "Superficie de pérdida registrada entre 2001 y 2022."
        )

    with col_b:

        mostrar_indicador(
            "Año de mayor pérdida",
            str(anio_maximo),
            "Año con la mayor pérdida anual registrada."
        )

    with col_c:

        mostrar_indicador(
            "Mayor pérdida acumulada",
            str(departamento_maximo).title(),
            "Departamento con el mayor valor acumulado."
        )

    st.write("")

    # ==============================================
    # METODOLOGÍA
    # ==============================================

    with st.expander(
        "Metodología de los indicadores"
    ):

        st.markdown("""
        Los indicadores se calcularon mediante Python
        y Pandas, utilizando los registros de pérdida
        de cobertura forestal incluidos en la base
        de datos del proyecto.

        **Pérdida acumulada:** suma de las superficies
        de pérdida registradas entre 2001 y 2022.

        **Año de mayor pérdida:** año con la mayor
        suma anual.

        **Departamento destacado:** departamento
        con la mayor pérdida acumulada durante
        el período.

        **Limitación:** estos indicadores no permiten
        determinar directamente las causas de la pérdida
        ni la superficie de bosque que permanece.
        """)

    # ==============================================
    # 04. CAUSAS DE LA PÉRDIDA DE BOSQUE
        st.divider()

    st.markdown(
        '<div class="etiqueta">04 / CAUSAS DE LA PÉRDIDA FORESTAL</div>',
        unsafe_allow_html=True
    )

    st.header("¿Por qué estamos perdiendo nuestros bosques?")

    st.write(
        "La pérdida de bosque húmedo amazónico en el Perú "
        "está asociada a diversas actividades humanas que "
        "transforman la cobertura forestal y modifican "
        "el uso del territorio."
    )

    st.write(
        "El siguiente video explica los principales factores "
        "asociados a la pérdida de bosque en la Amazonía peruana."
    )

    video = CARPETA_IMAGENES / "causas_deforestacion.mp4"

    if video.is_file():

        st.video(str(video))

    else:

        st.warning("No se encontró el archivo del video.")

    st.caption(
        "Video educativo elaborado mediante Google NotebookLM "
        "a partir de fuentes bibliográficas, con fines académicos. "
        "Contiene recursos audiovisuales generados mediante IA."
    )
    # Pendiente de incorporar el video de NotebookLM
    # ==============================================


    # ==============================================
    # 05. CONSECUENCIAS AMBIENTALES
    # ==============================================

    mostrar_consecuencias()

    # ==============================================
    # 06. CONSERVACIÓN Y SOLUCIONES
    # ==============================================

    mostrar_conservacion()


# ==================================================
# 7. EJECUCIÓN DE PRUEBA
# ==================================================

if __name__ == "__main__":
    mostrar_bosque()
