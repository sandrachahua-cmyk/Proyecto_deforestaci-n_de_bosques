import streamlit as st
import pandas as pd
import plotly.express as px

from datos import cargar_datos


# ==================================================
# 1. FUNCIONES DE SELECCIÓN
# ==================================================

def seleccionar_todos(departamentos):

    for departamento in departamentos:
        st.session_state[f"comparar_{departamento}"] = True


def limpiar_seleccion(departamentos):

    for departamento in departamentos:
        st.session_state[f"comparar_{departamento}"] = False


# ==================================================
# 2. FUNCIÓN PRINCIPAL
# ==================================================

def mostrar_comparacion():

    df = cargar_datos().copy()

    df = df[
        (df["ANIO"] >= 2001) &
        (df["ANIO"] <= 2022)
    ]

    departamentos = sorted(
        df["DEPARTAMENTO"].dropna().unique().tolist()
    )

    nombres_especiales = {
        "HUANUCO": "Huánuco",
        "JUNIN": "Junín",
        "SAN MARTIN": "San Martín",
        "MADRE DE DIOS": "Madre de Dios",
        "LA LIBERTAD": "La Libertad"
    }

    nombres = {
        departamento: nombres_especiales.get(
            departamento.upper(),
            departamento.title()
        )
        for departamento in departamentos
    }


    # ==================================================
    # 3. ESTILOS
    # ==================================================

    st.html("""
    <style>

        .stApp {
            background-color: #FFFFFF !important;
            color: #000000;
        }

        .titulo-comparacion {
            color: #000000;
            font-size: 27px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .descripcion-comparacion {
            color: #000000;
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 8px;
        }

        .subtitulo-comparacion {
            color: #000000;
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 1px;
            margin-top: 15px;
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 1.5px solid #000000;
        }


        /* TARJETAS DE RESULTADOS */

        .tarjeta-comparacion {
            background-color: #D2B48C !important;
            border: 1px solid #000000;
            border-radius: 12px;
            padding: 15px;
            min-height: 150px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .etiqueta-comparacion {
            font-size: 12px;
            font-weight: 700;
            color: #000000;
            min-height: 35px;
        }

        .valor-comparacion {
            font-size: 21px;
            font-weight: 600;
            color: #000000;
            margin-top: 8px;
            overflow-wrap: anywhere;
        }

        .titulo-tabla-comparacion {
            color: #000000;
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .nota-comparacion {
            color: #000000 !important;
            font-size: 14px;
            line-height: 1.5;
        }


        /* AVISO DE SELECCIÓN */

        .aviso-comparacion {
            background-color: #D2B48C !important;
            color: #000000 !important;
            border: 1px solid #000000;
            border-radius: 10px;
            padding: 18px;
            font-size: 16px;
            line-height: 1.5;
        }


        /* SELECCIÓN DE DEPARTAMENTOS */

        .st-key-selector_comparacion
        div[data-testid="stVerticalBlock"] {
            gap: 0.35rem;
        }

        .st-key-selector_comparacion
        div[data-testid="stCheckbox"] {
            margin: 0;
            padding: 0;
        }

        .st-key-selector_comparacion
        div[data-testid="stCheckbox"] p {
            color: #000000 !important;
        }

        .st-key-selector_comparacion
        label[data-baseweb="checkbox"]:has(input:checked) > div:first-child {
            background-color: #386641 !important;
            border-color: #386641 !important;
        }

        .st-key-selector_comparacion button {
            background-color: #FFFFFF;
            color: #000000;
            border: 1px solid #000000;
            border-radius: 8px;
        }

        .st-key-selector_comparacion button:hover {
            background-color: #D2B48C;
            color: #000000;
            border-color: #000000;
        }

        .st-key-selector_comparacion button p {
            color: #000000 !important;
        }


        /* TABLA COMPARATIVA PERSONALIZADA */

        .contenedor-tabla-comparacion {
            max-height: 150px;
            overflow: auto;
            border: 1.5px solid #000000;
            border-radius: 8px;
            background-color: #FFFFFF;
        }

        .tabla-comparacion {
            width: 100%;
            border-collapse: collapse;
            background-color: #FFFFFF;
            color: #000000 !important;
            font-size: 14px;
            margin: 0 !important;
        }

        .contenedor-tabla-comparacion
        .tabla-comparacion thead th {
            background-color: #D2B48C !important;
            color: #000000 !important;
            font-weight: 700 !important;
            text-align: left !important;
            padding: 10px !important;
            border: 1.5px solid #000000 !important;
            position: sticky;
            top: 0;
            z-index: 1;
        }

        .tabla-comparacion td {
            color: #000000 !important;
            background-color: #FFFFFF !important;
            padding: 10px !important;
            border: 1.5px solid #000000 !important;
        }

        .tabla-comparacion td:last-child {
            text-align: right !important;
        }

        .contenedor-tabla-comparacion
        .tabla-comparacion th:first-child,
        .tabla-comparacion td:first-child {
            border-left: none !important;
        }

        .contenedor-tabla-comparacion
        .tabla-comparacion th:last-child,
        .tabla-comparacion td:last-child {
            border-right: none !important;
        }

        .contenedor-tabla-comparacion
        .tabla-comparacion thead th {
            border-top: none !important;
        }

        .tabla-comparacion tbody tr:last-child td {
            border-bottom: none !important;
        }

    </style>
    """)


    # ==================================================
    # 4. ENCABEZADO
    # ==================================================

    st.html(
        '<div class="titulo-comparacion">'
        'EVOLUCIÓN COMPARATIVA DE LA PÉRDIDA DE BOSQUE'
        '</div>'
    )

    st.html(
        '<div class="descripcion-comparacion">'
        '<strong>¿Cómo ha evolucionado la pérdida acumulada '
        'de bosque entre los departamentos del Perú?</strong>'
        '</div>'
    )

    st.html(
        '<div class="descripcion-comparacion">'
        'Selecciona los departamentos que deseas comparar '
        'y explora la evolución de su pérdida acumulada '
        'de bosque húmedo amazónico durante el periodo '
        '2001–2022.'
        '</div>'
    )


    # ==================================================
    # 5. SELECCIÓN DE DEPARTAMENTOS
    # ==================================================

    st.html(
        '<div class="subtitulo-comparacion">'
        '01 / SELECCIÓN DE DEPARTAMENTOS'
        '</div>'
    )

    seleccionados = []

    with st.container(key="selector_comparacion"):

        columnas = st.columns(5)

        for i, departamento in enumerate(departamentos):

            with columnas[i % 5]:

                seleccionado = st.checkbox(
                    nombres[departamento],
                    key=f"comparar_{departamento}"
                )

                if seleccionado:
                    seleccionados.append(departamento)


        # BOTONES DE SELECCIÓN

        col_boton1, col_boton2, col_vacia = st.columns(
            [1, 1, 4]
        )

        with col_boton1:

            st.button(
                "Seleccionar todos",
                on_click=seleccionar_todos,
                args=(departamentos,),
                key="comparacion_todos"
            )

        with col_boton2:

            st.button(
                "Limpiar selección",
                on_click=limpiar_seleccion,
                args=(departamentos,),
                key="comparacion_limpiar"
            )

        st.html(
            '<div class="nota-comparacion">'
            f'Departamentos seleccionados: '
            f'{len(seleccionados)} de {len(departamentos)}'
            '</div>'
        )


    # ==================================================
    # 6. EVOLUCIÓN TEMPORAL COMPARATIVA
    # ==================================================

    st.html(
        '<div class="subtitulo-comparacion">'
        '02 / EVOLUCIÓN TEMPORAL COMPARATIVA'
        '</div>'
    )


    # AVISO CUANDO NO HAY DEPARTAMENTOS SELECCIONADOS

    if not seleccionados:

        st.html(
            '<div class="aviso-comparacion">'
            'Selecciona al menos un departamento '
            'para visualizar su evolución temporal.'
            '</div>'
        )

        return


    # FILTRAR LOS DEPARTAMENTOS SELECCIONADOS

    df_seleccion = df[
        df["DEPARTAMENTO"].isin(seleccionados)
    ]


    # CALCULAR LA PÉRDIDA ANUAL

    evolucion = df_seleccion.groupby(
        ["DEPARTAMENTO", "ANIO"]
    )["PERDIDA_BOSQUE"].sum(
        min_count=1
    ).reset_index()


    # COMPROBAR QUE EXISTAN LOS 22 AÑOS

    indice_completo = pd.MultiIndex.from_product(
        [seleccionados, range(2001, 2023)],
        names=["DEPARTAMENTO", "ANIO"]
    )

    evolucion = evolucion.set_index(
        ["DEPARTAMENTO", "ANIO"]
    ).reindex(
        indice_completo
    ).reset_index()

    if evolucion["PERDIDA_BOSQUE"].isna().any():

        st.warning(
            "Existen datos anuales faltantes en los "
            "departamentos seleccionados. No es posible "
            "calcular una comparación acumulada completa."
        )

        return


    # ORDENAR CRONOLÓGICAMENTE

    evolucion = evolucion.sort_values(
        ["DEPARTAMENTO", "ANIO"]
    )


    # CALCULAR LA PÉRDIDA ACUMULADA

    evolucion["PERDIDA_ACUMULADA"] = (
        evolucion.groupby("DEPARTAMENTO")
        ["PERDIDA_BOSQUE"].cumsum()
    )


    # FORMATO DE LOS NOMBRES

    evolucion["DEPARTAMENTO"] = (
        evolucion["DEPARTAMENTO"].map(nombres)
    )


    # ==================================================
    # 7. GRÁFICO LINEAL INTERACTIVO
    # ==================================================

    colores = [
        "#1B7837",
        "#2166AC",
        "#B2182B",
        "#E67E22",
        "#762A83",
        "#008B8B",
        "#795548",
        "#D81B60",
        "#636363",
        "#827717",
        "#3949AB",
        "#00ACC1",
        "#F9A825",
        "#8E44AD",
        "#558B2F"
    ]

    mapa_colores = {
        nombres[departamento]: colores[i % len(colores)]
        for i, departamento in enumerate(departamentos)
    }

    grafico = px.line(

        evolucion,

        x="ANIO",

        y="PERDIDA_ACUMULADA",

        color="DEPARTAMENTO",

        markers=True,

        color_discrete_map=mapa_colores,

        labels={
            "ANIO": "Año",
            "PERDIDA_ACUMULADA":
                "Pérdida acumulada de bosque (ha)",
            "DEPARTAMENTO": "Departamento"
        }
    )


    # GROSOR DE LAS LÍNEAS Y PUNTOS

    grafico.update_traces(

        line=dict(width=5),

        marker=dict(size=7),

        connectgaps=False,

        hovertemplate=(
            "Año: %{x}<br>"
            "Pérdida acumulada: %{y:,.2f} ha"
            "<extra>%{fullData.name}</extra>"
        )
    )


    # DISEÑO GENERAL DEL GRÁFICO

    grafico.update_layout(

        height=460,

        autosize=True,

        plot_bgcolor="#FFFFFF",

        paper_bgcolor="#FFFFFF",

        font=dict(
            color="#000000",
            size=14
        ),

        hovermode="x unified",

        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(
                color="#000000",
                size=13
            )
        ),

        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_color="#000000",
            bordercolor="#000000"
        ),

        margin=dict(
            l=135,
            r=35,
            t=55,
            b=80,
            autoexpand=True
        )
    )


    # EJE X: AÑOS

    grafico.update_xaxes(

        tickmode="linear",

        tick0=2001,

        dtick=1,

        tickangle=-45,

        range=[2000.7, 2022.3],

        automargin=True,

        showgrid=False,

        showline=True,

        linecolor="#000000",

        linewidth=2,

        ticks="outside",

        tickcolor="#000000",

        ticklen=5,

        tickfont=dict(
            color="#000000",
            size=12
        ),

        title=dict(
            text="Año",
            standoff=15,
            font=dict(
                color="#000000",
                size=14
            )
        )
    )


    # EJE Y: PÉRDIDA ACUMULADA

    grafico.update_yaxes(

        rangemode="tozero",

        tickformat=",.0f",

        automargin=True,

        showline=True,

        linecolor="#000000",

        linewidth=2,

        ticks="outside",

        tickcolor="#000000",

        ticklen=5,

        showgrid=True,

        gridcolor="#B0B0B0",

        gridwidth=1.2,

        zeroline=True,

        zerolinecolor="#000000",

        zerolinewidth=2,

        tickfont=dict(
            color="#000000",
            size=13
        ),

        title=dict(
            text="Pérdida acumulada de bosque (ha)",
            standoff=25,
            font=dict(
                color="#000000",
                size=14
            )
        )
    )


    # MOSTRAR GRÁFICO

    st.plotly_chart(
        grafico,
        use_container_width=True,
        theme=None,
        config={
            "responsive": True,
            "displaylogo": False,
            "displayModeBar": False,
            "staticPlot": True
        }
    )

    st.html(
        '<div class="nota-comparacion">'
        'Cada línea representa la pérdida acumulada '
        'de bosque desde 2001 hasta el año correspondiente.'
        '</div>'
    )


    # ==================================================
    # 8. RESULTADOS COMPARATIVOS
    # ==================================================

    st.html(
        '<div class="subtitulo-comparacion">'
        '03 / RESULTADOS COMPARATIVOS'
        '</div>'
    )

    resultados = evolucion[
        evolucion["ANIO"] == 2022
    ].sort_values(
        "PERDIDA_ACUMULADA",
        ascending=False
    )

    perdida_total = resultados[
        "PERDIDA_ACUMULADA"
    ].sum()

    departamento_mayor = resultados.iloc[0][
        "DEPARTAMENTO"
    ]


    # PREPARAR LA TABLA COMPARATIVA

    tabla = resultados[
        ["DEPARTAMENTO", "PERDIDA_ACUMULADA"]
    ].copy()

    tabla.columns = [
        "Departamento",
        "Pérdida acumulada (ha)"
    ]


    # ==================================================
    # 9. TARJETAS Y TABLA EN UNA SOLA FILA
    # ==================================================

    with st.container(key="resultados_comparacion"):

        col1, col2, col3, col4 = st.columns(
            [1, 1.3, 1.2, 2.5],
            gap="small"
        )


        # TARJETA 1: DEPARTAMENTOS SELECCIONADOS

        with col1:

            st.html(
                '<div class="tarjeta-comparacion">'
                '<div class="etiqueta-comparacion">'
                'DEPARTAMENTOS SELECCIONADOS'
                '</div>'
                '<div class="valor-comparacion">'
                f'{len(seleccionados)}'
                '</div></div>'
            )


        # TARJETA 2: PÉRDIDA ACUMULADA TOTAL

        with col2:

            st.html(
                '<div class="tarjeta-comparacion">'
                '<div class="etiqueta-comparacion">'
                'PÉRDIDA ACUMULADA TOTAL'
                '</div>'
                '<div class="valor-comparacion">'
                f'{perdida_total:,.2f} ha'
                '</div></div>'
            )


        # TARJETA 3: DEPARTAMENTO CON MAYOR PÉRDIDA

        with col3:

            st.html(
                '<div class="tarjeta-comparacion">'
                '<div class="etiqueta-comparacion">'
                'MAYOR PÉRDIDA ENTRE LOS SELECCIONADOS'
                '</div>'
                '<div class="valor-comparacion">'
                f'{departamento_mayor}'
                '</div></div>'
            )


        # COLUMNA 4: TABLA COMPARATIVA

        with col4:

            st.html(
                '<div class="titulo-tabla-comparacion">'
                'Pérdida acumulada por departamento (2001–2022)'
                '</div>'
            )

            tabla_visual = tabla.copy()

            tabla_visual["Pérdida acumulada (ha)"] = (
                tabla_visual["Pérdida acumulada (ha)"]
                .apply(lambda valor: f"{valor:,.2f}")
            )

            tabla_html = tabla_visual.to_html(
                index=False,
                classes="tabla-comparacion",
                border=0
            )

            st.html(
                '<div class="contenedor-tabla-comparacion">'
                f'{tabla_html}'
                '</div>'
            )


# ==================================================
# 10. EJECUCIÓN INDEPENDIENTE
# ==================================================

if __name__ == "__main__":

    st.set_page_config(
        page_title="Comparación entre departamentos",
        layout="wide"
    )

    mostrar_comparacion()