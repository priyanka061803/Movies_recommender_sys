import streamlit as st
import pickle
import pandas as pd

st.set_page_config(page_title="FilmFusion", layout="wide")

st.title("Movie Ratings & Feedback")
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


import streamlit as st

if "movie_feedback" not in st.session_state:
    st.session_state["movie_feedback"] = {}


selected_movie = st.selectbox(
'Type or select a movie from the dropdown',
movies['title'].values)

rating = st.slider("Rate the movie (1-5 stars)", 1, 5, 3)

# Movie feedback
feedback = st.text_area("Leave your feedback")

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

# Submit button
if st.button("Submit"):
    if selected_movie not in st.session_state["movie_feedback"]:
        st.session_state["movie_feedback"][selected_movie] = []
    st.session_state["movie_feedback"][selected_movie].append({"rating": rating, "feedback": feedback})
    st.success("Thanks for your feedback!")

# Display all ratings and feedback for selected movie
if selected_movie in st.session_state["movie_feedback"]:
    st.subheader("User Ratings & Feedback")
    ratings_list = st.session_state["movie_feedback"][selected_movie]
    avg_rating = sum(r['rating'] for r in ratings_list) / len(ratings_list)
    st.write(f"Average Rating: {avg_rating:.1f} ⭐")
    for r in ratings_list:
        st.write(f"Rating: {r['rating']} ⭐")
        st.write(f"Feedback: {r['feedback']}")
        st.write("---")
