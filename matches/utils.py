def calculate_match_score(profile1, profile2):
    genres1 = set(profile1.favorite_genres)
    genres2 = set(profile2.favorite_genres)
    genre_score = len(genres1 & genres2)

    artist_score = int(profile1.favorite_artists == profile2.favorite_artists)
    return genre_score + artist_score
