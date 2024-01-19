import pickle
import pandas as pd
import streamlit as st
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=62e6915f9db9a03352dc663b7e1449f4".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = df[df['original_title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity_score[index])), reverse=True, key=lambda x: x[1])
    rec_mn = []
    rec_mp = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = df.iloc[i[0]].id
        rec_mp.append(fetch_poster(movie_id))
        rec_mn.append(df.iloc[i[0]].original_title)

    return rec_mn, rec_mp


st.title("Movie Recommender System")
movies_dict = pickle.load(open('netflix_df.pkl', 'rb'))
df = pd.DataFrame(movies_dict)
similarity_score = pickle.load(open('similarity1.pkl', 'rb'))

option = st.selectbox("Select any Movie", df['original_title'].values)

if st.button('Show Recommendation'):
    rec_mn, rec_mp = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(rec_mn[0])
        st.image(rec_mp[0])
    with col2:
        st.text(rec_mn[1])
        st.image(rec_mp[1])
    with col3:
        st.text(rec_mn[2])
        st.image(rec_mp[2])
    with col4:
        st.text(rec_mn[3])
        st.image(rec_mp[3])
    with col5:
        st.text(rec_mn[4])
        st.image(rec_mp[4])
