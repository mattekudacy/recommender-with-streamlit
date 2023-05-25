import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def fetch_synopsis(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    synopsis = data['overview']
    return synopsis

def recommend(selected_movies):
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_synopsis = []
    recommended_movie_genres = []

    for movie in selected_movies:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        for i in distances[1:6]:
            # fetch the movie poster, synopsis, and genres
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_synopsis.append(fetch_synopsis(movie_id))
            recommended_movie_genres.append(movies.iloc[i[0]].genres)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_synopsis, recommended_movie_genres


st.set_page_config(layout="wide")  # Set the layout to occupy full width

# Add custom CSS styles to occupy the available space
st.markdown(
    """
    <style>
    .stApp {
        max-width: 100%;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header('Movie Recommender System')

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movies = st.multiselect(
    "Select movies for recommendations",
    movie_list
)

show_recommendation = st.button('Show Recommendation')

if show_recommendation:
    recommended_movie_names, recommended_movie_posters, recommended_movie_synopsis, recommended_movie_genres = recommend(selected_movies)
    st.markdown('**Recommended Movies:**')
    cols = st.columns(5)
    for i in range(len(recommended_movie_names)):
        with cols[i % 5]:
            with st.expander(recommended_movie_names[i]):
                st.image(recommended_movie_posters[i], use_column_width=True)
                st.write(recommended_movie_synopsis[i])
                st.write("Genres: ", ", ".join(recommended_movie_genres[i]))
                add_to_watchlist = st.checkbox(f'Add to Watchlist {recommended_movie_names[i]}', key=f'checkbox_{i}')
                if add_to_watchlist:
                    if 'watchlist' not in st.session_state:
                        st.session_state.watchlist = []  # Initialize an empty watchlist
                    st.session_state.watchlist.append(recommended_movie_names[i])

selected_movie_posters = []
for movie in selected_movies:
    index = movies[movies['title'] == movie].index[0]
    movie_id = movies.iloc[index].movie_id
    selected_movie_posters.append(fetch_poster(movie_id))

st.markdown('**Selected Movies Posters:**')
st.image(selected_movie_posters, width=150)
