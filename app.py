import pandas as pd
import streamlit as st
from joblib import load

# Configurar la página inicial
st.set_page_config(page_title="Predicción de Valor de Mercado", layout="wide")

# Función para cargar datos (usando st.cache_data)
@st.cache_data(persist=True)
def load_data(file_path):
    return pd.read_csv(file_path)

# Función para cargar modelos (usando st.cache_resource)
@st.cache_resource
def load_model(model_path):
    return load(model_path)

# Cargar archivos necesarios
df_club_name = load_data("df_club_name.csv")
df_foot = load_data("df_foot.csv")
df_pos = load_data("df_pos.csv")
df_sub_pos = load_data("df_sub_pos.csv")
df_country = load_data("df_country.csv")
df_comp_id = load_data("df_comp_id.csv")

# Cargar label encoders
label_encoder_country_of_birth = load("le_country_of_birth.sav")
label_encoder_competition_id = load("le_competition_id.sav")
label_encoder_club_name = load("le_club_name.sav")
label_encoder_foot = load("le_foot.sav")
label_encoder_sub_position = load("le_sub_position.sav")
label_encoder_position = load("le_position.sav")

# Cargar modelo de predicción
 model = load_model("modelo.joblib")

# Estado inicial: una variable en sesión
if "page" not in st.session_state:
    st.session_state.page = "inicio"

# Función para cambiar de página
def change_page(page_name):
    st.session_state.page = page_name

# Lógica de navegación
if st.session_state.page == "inicio":
    st.title("Bienvenido a la App de Predicción de Valor de Mercado")
    st.markdown("""
    Esta aplicación predice el valor de mercado de un jugador de fútbol profesional
    en función de características como su edad, rendimiento y otros factores.
    """)
    if st.button("Ir a completar datos"):
        change_page("completar_datos")

elif st.session_state.page == "completar_datos":
    st.title("Completar Datos del Jugador")
    st.sidebar.title("Parámetros del jugador")

    # Inputs del usuario
    matches_played = st.sidebar.slider('Matches Played', 0, 100, 25)
    yellow_cards = st.sidebar.slider('Yellow Cards', 0, 2, 0)
    red_cards = st.sidebar.slider('Red Cards', 0, 1, 0)
    goals = st.sidebar.slider('Goals', 0, 6, 0)
    assists = st.sidebar.slider('Assists', 0, 10, 0)
    minutes_played = st.sidebar.slider('Minutes Played', 0, 120, 90)
    age = st.sidebar.slider('Age', 15, 45, 25)
    height_in_cm = st.sidebar.slider('Height (cm)', 150, 220, 180)
    highest_market_value_in_eur = st.sidebar.slider('Highest Market Value (€)', 100000, 20000000, 5000000)

    club_name = st.selectbox('Select a Club Name', df_club_name)
    foot = st.selectbox('Select a Foot', df_foot)
    position = st.selectbox('Select a Position', df_pos)
    sub_position = st.selectbox('Select a Sub Position', df_sub_pos)
    country_of_birth = st.selectbox('Select a Country of Birth', df_country)
    competition_id = st.selectbox('Select a Competition', df_comp_id)

    # Codificar inputs con los label encoders
    competition_id_le = label_encoder_competition_id.transform([competition_id])[0]
    club_name_le = label_encoder_club_name.transform([club_name])[0]
    foot_le = label_encoder_foot.transform([foot])[0]
    position_le = label_encoder_position.transform([position])[0]
    sub_position_le = label_encoder_sub_position.transform([sub_position])[0]
    country_of_birth_le = label_encoder_country_of_birth.transform([country_of_birth])[0]

    # Crear lista con la información
    info = [
        matches_played, yellow_cards, red_cards, goals, assists,
        minutes_played, age, height_in_cm, highest_market_value_in_eur,
        competition_id_le, club_name_le, foot_le, position_le,
        sub_position_le, country_of_birth_le
    ]

    # Botón para predecir
    if st.button("Realizar predicción"):
        try:
            prediccion = model.predict([info])[0]
            st.success(f"Predicción del valor de mercado: €{prediccion:,.2f}")
        except Exception as e:
            st.error(f"Error al realizar la predicción: {str(e)}")

    # Botón para regresar a la página inicial
    if st.button("Volver al inicio"):
        change_page("inicio")

