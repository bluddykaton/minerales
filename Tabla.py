import streamlit as st
import pandas as pd

st.title("Buscador Interactivo de Minerales")

# 1. CARGAR LA BASE DE DATOS DESDE EL ARCHIVO EXTERNO
# Esta única línea reemplaza todo el diccionario anterior
df = pd.read_csv("minerales.csv")

# 2. LA "TABLA PERIÓDICA" VIRTUAL
st.subheader("🧪 Filtrar por Elementos")
elementos_comunes = ["Cu", "Fe", "O", "S", "Mo", "C", "H"]
columnas = st.columns(len(elementos_comunes))
elementos_seleccionados = []

for i, elemento in enumerate(elementos_comunes):
    with columnas[i]:
        if st.toggle(elemento):
            elementos_seleccionados.append(elemento)

# 3. BARRA DE BÚSQUEDA DE TEXTO
st.divider()
st.subheader("🔍 O busca por texto libre")
busqueda_texto = st.text_input("Escribe el mineral o fórmula:")

# 4. LÓGICA DE FILTRADO
resultados = df.copy()

# Filtrar por botones
if elementos_seleccionados:
    for elemento in elementos_seleccionados:
        # Busca si el elemento (ej: "Cu") está dentro del texto de la columna "Elementos"
        resultados = resultados[resultados["Elementos"].str.contains(elemento, case=True, na=False)]

# Filtrar por texto
if busqueda_texto:
    filtro_texto = (
        resultados["Mineral"].str.contains(busqueda_texto, case=False, na=False) |
        resultados["Fórmula"].str.contains(busqueda_texto, case=False, na=False)
    )
    resultados = resultados[filtro_texto]

# 5. MOSTRAR LA TABLA FINAL
tabla_final = resultados.drop(columns=["Elementos"])

if resultados.empty:
    st.warning("No se encontraron minerales con esa combinación.")
else:
    st.dataframe(tabla_final, use_container_width=True)