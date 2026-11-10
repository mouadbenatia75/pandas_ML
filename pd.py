import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

movies = pd.read_csv("movies.csv")
rating = pd.read_csv("ratings.csv")

#  Join the two tables of movie and the rating in a single table on thier movieId
df = pd.merge(movies , rating  , on="movieId")

df["genres"] = df["genres"].str.split("|")
dfExploded = df.explode("genres")
#  -------------------Group by genres and add the column mean_rating and total_rating----------------
genres_stats = (
    dfExploded.groupby("genres")
    .agg(mean_rating =("rating" , "mean") , total_rating = ("rating" , "count"))
    .reset_index()
)
#---------------------Group by titles and add the column mean_rating and total_rating----------------
movies_stats = (
    df.groupby("title")
    .agg(mean_rating = ("rating" , "mean") , total_rating =("rating" , "count"))
    .reset_index()
)

#---------------------Select the movies with heigher total of rating---------------------------------
#---------------------Sort the popular genres by their mean rating and take the top 10---------------

popularMovies = movies_stats[movies_stats["total_rating"] >= 50 ]
popularMoviesSorted = popularMovies.sort_values(by = "mean_rating" , ascending=False).head(10)

genres_statsSorted = genres_stats.sort_values(by ="mean_rating" , ascending=False)


top_genres = dfExploded["genres"].value_counts().head(10).index
filtered_df = dfExploded[dfExploded["genres"].isin(top_genres)]
print(genres_statsSorted)
print(df)
genres_statsSortedTop = genres_statsSorted.head(10)

plt.figure(figsize=(11,7))

bars = plt.bar(
    genres_statsSortedTop["genres"],
    genres_statsSortedTop["mean_rating"],
    color="#4C72B0",
    edgecolor="#2C3E50",
    alpha=0.85,
)

plt.xlabel("Movie genres" ,fontsize=11 , fontweight= "bold")
plt.ylabel("Mean rating out of 5 ",fontsize=11 , fontweight= "bold")
plt.ylim(0 , 5.2)
plt.gca().invert_xaxis()
plt.grid(axis="y", linestyle="--", alpha=0.5)


plt.figure(figsize=(11,7))

bars2 = plt.bar(
    popularMoviesSorted["title"],
    popularMoviesSorted["mean_rating"],
    color="#4C72B0",
    edgecolor="#2C3E50",
    alpha=0.85,
)

plt.xlabel("Movie title " ,fontsize=11 , fontweight= "bold")
plt.ylabel("Mean rating out of 5 ",fontsize=11 , fontweight= "bold")
plt.ylim(0 , 5.2)
plt.gca().invert_xaxis()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.xticks(rotation=45, ha="right", fontsize=9)




# 5. Set up the Matplotlib figure
plt.figure(figsize=(13, 6))

# 6. Create a Seaborn boxplot
sns.boxplot(
    x="genres",
    y="rating",
    data=filtered_df,
    palette="Set2",
    hue="genres",
    legend=False,
    showmeans=True,
    meanprops={
        "marker": "o",
        "markerfacecolor": "white",
        "markeredgecolor": "black",
    },
)

# 7. Customize the plot labels and layout
plt.title(
    "Rating Distribution Across Top 10 Movie Genres (White dot = Mean)",
    fontsize=13,
    fontweight="bold",
    pad=15,
)

plt.xlabel("Movie Genre", fontsize=11, fontweight="bold")
plt.ylabel("Rating Scale (0.5 to 5.0)", fontsize=11, fontweight="bold")

plt.xticks(rotation=30, fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.5)


# Adjust layout to prevent clipping of long titles and display
plt.tight_layout()
plt.show()