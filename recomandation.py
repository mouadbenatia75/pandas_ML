import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
#  Get recommendation using cosine similarity 
movies = pd.read_csv("movies.csv")
rating = pd.read_csv("ratings.csv")

df = pd.merge(movies , rating , on="movieId")

user_movie_matrix = df.pivot_table(
    index="userId",columns="title",values="rating"
).fillna(0)
movie_similarity = cosine_similarity(user_movie_matrix.T)
movie_sim_df = pd.DataFrame(
    movie_similarity,
    index=user_movie_matrix.columns,
    columns= user_movie_matrix.columns
)

def recommend_movies(movie_title , n = 5):
    if movie_title not in movie_sim_df.columns:
        return f"{movie_title} not found in dataset "
    print(f"Because you liked {movie_title} , you might also like")
    similar_scores = movie_sim_df[movie_title].sort_values(ascending=False)
    top_recommendations = similar_scores.iloc[1:n+1]
    for title, score in top_recommendations.items():
        print(f" - {title} (Similarity Score: {score:.2f})")
print( recommend_movies("Toy Story (1995)", n=5))
