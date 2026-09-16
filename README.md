# Movie Recommendation Engine

A content-based movie recommender built with Streamlit. Pick a movie you
like and get back the most similar titles, ranked by a weighted similarity
score across genre, cast, director, keywords, release year, and rating —
no collaborative filtering or external ML model required, just interpretable
feature similarity you can see and reason about.

## How the similarity score works

Each candidate movie is scored against the selected one on six weighted
factors:

| Factor | Weight | Comparison |
|---|---|---|
| Genre | 23% | Exact match on primary genre |
| Cast | 18.5% | Jaccard similarity of cast sets |
| Director | 16% | Exact match |
| Keywords | 15.5% | Jaccard similarity of extracted keywords |
| Release year | 14% | Linear decay over a 10-year window |
| Rating | 12.5% | Linear decay over a 10-point scale |

The weighted sum ranks all other movies in the dataset, and the app returns
the top N.

## Running it

```bash
pip install -r requirements.txt
streamlit run movie.py
```

Opens at `http://localhost:8501`. The dataset (`Updated_Movie_Data_with_Keywords4.csv`)
ships in the repo, so it runs out of the box.

## Stack

Python, Streamlit, pandas.
