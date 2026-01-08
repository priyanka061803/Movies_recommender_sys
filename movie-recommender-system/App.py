import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(page_title="FilmFusion", layout="wide")
st.markdown("""
<style>
.sidebar-info {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 12px;
    border-left: 4px solid #f5c518;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar.expander("ℹ️ How This System Works"):
    st.markdown("""
    <div class="sidebar-info">
    <b>🎬 FilmFusion</b><br><br>

    🔹 Select a movie you like  
    🔹 Our ML model finds similar movies  
    🔹 Posters & details are fetched via OMDb  
    🔹 Results update instantly  

    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
section[data-testid="stSidebar"] > div:first-child {
    background: rgba(0,0,0,0.85);
    backdrop-filter: blur(10px);
    color: white;
    padding: 20px;
}

/* Sidebar radio buttons */
.stRadio > div {
    gap: 10px;
}

.stRadio label {
    padding: 10px;
    border-radius: 10px;
    transition: background 0.3s;
}

.stRadio label:hover {
    background: rgba(245,197,24,0.2);
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* Sidebar background collage */
section[data-testid="stSidebar"] > div:first-child {
    background:
        linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
        url("download (2).jpg"),
        url("https://i.pinimg.com/736x/83/08/4c/83084c34bcb62c67377d496f54fd1f80.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    color: white;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* Container for header + subtitle */
.animated-header {
    text-align: center;
    color: #ffffff;
    font-family: 'Arial', sans-serif;
    margin-top: 30px;
    animation: slideFade 2s ease-in-out;
}

/* Subtitle styling */
.animated-subtitle {
    text-align: center;
    color: #d3d3d3;
    font-size: 18px;
    margin-top: 10px;
    animation: fadeIn 3s ease-in-out;
}

/* Keyframes for slide + fade */
@keyframes slideFade {
    0% {
        opacity: 0;
        transform: translateY(-30px);
    }
    100% {
        opacity: 1;
        transform: translateY(0px);
    }
}

/* Keyframes for subtitle fade-in */
@keyframes fadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}
</style>

<h1 class="animated-header">🎬 FilmFusion</h1>
<p class="animated-subtitle">Discover movies you'll love based on your taste</p>
""", unsafe_allow_html=True)


st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #1b2735, #090a0f);
    color: white;
}
</style>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    response = requests.get('http://www.omdbapi.com/?i={}&apikey=bf20192b'.format(movie_id))
    data = response.json()
    poster_path = data.get('poster_path')

    if poster_path:
        return "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwODI5OTM0Mw@@._V1_SX500.jpg" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
       movie_id = movies.iloc[i[0]].movie_id

       recommended_movies.append(movies.iloc[i[0]].title)
       recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))



selected_movie_name = st.selectbox(
'Type or select a movie from the dropdown',
movies['title'].values)

if st.button('Show Recommendations 🎯'):
   with st.spinner("Finding the perfect movies for you"):

       names, posters = recommend(selected_movie_name)
       col1, col2, col3, col4, col5 = st.columns(5)
       with col1:
           st.text(names[0])
           st.image(posters[0])
       with col2:
           st.text(names[1])
           st.image(posters[1])

       with col3:
           st.text(names[2])
           st.image(posters[2])
       with col4:
           st.text(names[3])
           st.image(posters[3])
       with col5:
           st.text(names[4])
           st.image(posters[4])


st.markdown("""
<hr>
<center>
<p style="opacity:0.7;">
Data from TMDB & OMDb | Made with Streamlit 🎥
</p>
</center>
""", unsafe_allow_html=True)