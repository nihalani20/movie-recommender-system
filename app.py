from http.client import responses

import streamlit as st
import pickle
import pandas as pd
import time
import requests
from requests.exceptions import ConnectionError, HTTPError

# def fetch_poster(movie_id):
#     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=13eab87763863b68e22721c63e842eb6&language=en-US'.format(movie_id))
#     data = response.json()
#     print(data)
#     return   "https://image.tmdb.org/t/p/w185/" +  data['poster_path']

#below code is to resolve the connection error

def fetch_poster(movie_id, retries=3, delay=5):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=13eab87763863b68e22721c63e842eb6&language=en-US'.format(movie_id)
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            data = response.json()
            return "https://image.tmdb.org/t/p/w185/" + data['poster_path']
        except (ConnectionError, HTTPError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise  # Re-raise the exception if out of retries

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Pick your favorite movie:",
 movies['title'].values)



#st.button("Reset", type="primary")
if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        #st.header(names[1][:15])
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