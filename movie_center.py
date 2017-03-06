# import python libraries
import json
# import app libraries
import media
import fresh_tomatoes
import tmdb


joe = tmdb.User(api_key='d9b26b5a45c33d29291f6f2338a06b3f',
                username='joeamedeo',
                password='DontHackMePlease1')

favorite_movies = joe.favorite_movies()

movies = []
for movie in favorite_movies:
    # Getting a proper trailer from a list of videos.
    youtube_url = 'https://www.youtube.com/watch?v='
    for video in movie['videos']['results']:
        if video['type'] == 'Trailer':
            youtube_url = 'https://www.youtube.com/watch?v=%s' % video['key']
            break
    # Saving relevent movie information
    movies.append(
        media.Movie(movie['original_title'], movie['overview'],
                    'https://image.tmdb.org/t/p/w500%s' % movie['poster_path'],
                    youtube_url
                    )
    )

fresh_tomatoes.open_movies_page(movies)
