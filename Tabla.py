import streamlit as st
import pandas as pd

st.title("Buscador Interactivo de Minerales")

# 1. CARGAR LA BASE DE DATOS
df = pd.read_csv("minerales.csv")

# 2. LA MEMORIA DE LOS BOTONES
# Creamos una lista vacía en la memoria para guardar los elementos que vayas seleccionando
if "elementos_activos" not in st.session_state:
    st.session_state.elementos_activos = []


# Esta es la función que se ejecuta cada vez que aprietas un cuadro
def alternar_elemento(elemento):
    if elemento in st.session_state.elementos_activos:
        st.session_state.elementos_activos.remove(elemento)  # Lo apaga si ya estaba encendido
    else:
        st.session_state.elementos_activos.append(elemento)  # Lo enciende si estaba apagado


# 3. DISEÑO DE LA "TABLA PERIÓDICA"
st.subheader("🧪 Filtrar por Elementos")
st.write("Haz clic en los cuadros para activarlos o desactivarlos:")

elementos_comunes = ["Cu", "Fe", "O", "S", "Mo", "C", "H", "Pb", "Zn"]

# Creamos una cuadrícula de 5 columnas para dar ese efecto de bloque o tabla
columnas_tabla = st.columns(5)

# Dibujamos un botón (cuadro) por cada elemento químico
for i, elemento in enumerate(elementos_comunes):
    # Esto hace que los botones se ordenen de izquierda a derecha en las 5 columnas
    col_actual = columnas_tabla[i % 5]

    with col_actual:
        # Revisamos si el elemento está en nuestra memoria de "encendidos"
        es_activo = elemento in st.session_state.elementos_activos

        # Si está encendido, usamos el color 'primary' (destacado). Si no, 'secondary' (gris).
        tipo_color = "primary" if es_activo else "secondary"

        # Dibujamos el cuadro clickeable
        st.button(
            label=f"{elemento}",
            key=elemento,
            type=tipo_color,
            on_click=alternar_elemento,
            args=(elemento,),
            use_container_width=True  # Esto hace que el botón sea un cuadro ancho que llena el espacio
        )

# 4. BARRA DE BÚSQUEDA DE TEXTO
st.divider()
st.subheader("🔍 O busca por texto libre")
busqueda_texto = st.text_input("Escribe el mineral o fórmula:")

# 5. LÓGICA DE FILTRADO
resultados = df.copy()

# Filtrar por los cuadros encendidos
if st.session_state.elementos_activos:
    for elemento in st.session_state.elementos_activos:
        resultados = resultados[resultados["Elementos"].str.contains(elemento, case=True, na=False)]

# Filtrar por texto
if busqueda_texto:
    filtro_texto = (
            resultados["Mineral"].str.contains(busqueda_texto, case=False, na=False) |
            resultados["Fórmula"].str.contains(busqueda_texto, case=False, na=False)
    )
    resultados = resultados[filtro_texto]

# 6. MOSTRAR LA TABLA FINAL
# Ocultamos la columna de la lista separada por comas para que se vea más limpio
tabla_final = resultados.drop(columns=["Elementos"], errors="ignore")

if resultados.empty:
    st.warning("No se encontraron minerales.")
else:
    st.dataframe(tabla_final, use_container_width=True)
