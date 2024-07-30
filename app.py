import pickle
import streamlit as st
import requests
import gzip
import numpy as np

APIKEY=st.secrets["APIKEY"]

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(APIKEY)
    }

    data = requests.get(url, headers=headers)
    data = data.json()
    poster_path = data['poster_path']
    full_path= "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path

def recommend(movie, percentile=95):
    idx = movies[movies['title'] == movie].index[0]
    # Obtener las puntuaciones de similitud en coseno para todas las películas con esa película
    sim_scores = list(enumerate(similarity[idx]))

    # Extraer las puntuaciones de similitud
    sim_values = [score[1] for score in sim_scores]

    # Determinar el umbral basado en el percentil
    threshold = np.percentile(sim_values, percentile)

    # Filtrar las películas basadas en el umbral de similitud
    sim_scores = [score for score in sim_scores if score[1] >= threshold]

    # Ordenar las películas basadas en las puntuaciones de similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    recommended_movies_name = []

    recommendend_movies_poster = []

    for i in sim_scores[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommendend_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommendend_movies_poster


    

st.header("Sistema de Recomendacion de Películas con Machine Learning")
with gzip.open('matrices/movie_list.pkl.gz', 'rb') as f:
    movies = pickle.load(f)

with gzip.open('matrices/similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

movie_list = movies['title']
selected_movie=st.selectbox(
    'Selecciona una pelicula',
    movie_list
)
if st.button('Mostrar Recomendaciones'):
    recommended_movies_name,recommendend_movies_poster = recommend(selected_movie)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommendend_movies_poster[0])
    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommendend_movies_poster[1])
    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommendend_movies_poster[2])
    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommendend_movies_poster[3])
    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommendend_movies_poster[4])