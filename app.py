import streamlit as st
import pickle
import requests
import os
import gdown

# === Ensure model folder exists ===
os.makedirs("model", exist_ok=True)

# === Google Drive file IDs ===
movie_list_file_id = "1r1XIh-7YLwHZ3scUbl_i10IQ5hdN6XVv"
similarity_file_id = "1YXmuSYT_MkYh2RS2_E1inv-6osOseSwJ"

# === Download model files if not present ===
movie_list_path = "model/movie_list.pkl"
similarity_path = "model/similarity.pkl"

if not os.path.exists(movie_list_path):
    gdown.download(f"https://drive.google.com/uc?id={movie_list_file_id}", movie_list_path, quiet=False)

if not os.path.exists(similarity_path):
    gdown.download(f"https://drive.google.com/uc?id={similarity_file_id}", similarity_path, quiet=False)

# === Load models ===
movies = pickle.load(open(movie_list_path, 'rb'))
similarity = pickle.load(open(similarity_path, 'rb'))

# === Helper function to fetch poster ===
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# === Recommendation logic ===
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# === Streamlit UI ===
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header('🎬 Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
