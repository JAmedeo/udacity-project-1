"""
tmdb.py relys on data provided by www.themoviedb.org.  Specific documentions
can be found at https://www.themoviedb.org/documentation/api.

"""



# import Python libraries
import http.client
import json

# Establishing a connection to TMDB's API.
conn = http.client.HTTPSConnection("api.themoviedb.org")


def _tmdb_api_call(tmdb_url, **kwargs):
    """ _tmdb_api_call is an internal function that accepts a TMDB API URL and
            parameters associated with the URL.  _tmdb_api_call will return a
            Dictonary. """

    tmdb_api_urls = {
        'request_token': '/3/authentication/token/new?api_key=%(api_key)s',  # NOQA
        'auth_token': '/3/authentication/token/validate_with_login?api_key=%(api_key)s&username=%(username)s&password=%(password)s&request_token=%(request_token)s',  # NOQA
        'session_id': '/3/authentication/session/new?api_key=%(api_key)s&request_token=%(request_token)s',  # NOQA
        'favorite_movies': '/3/account/%(username)s/favorite/movies?language=en-US&api_key=%(api_key)s&session_id=%(session_id)s',  # NOQA
        'movie_details': '/3/movie/%(movie_id)s?api_key=%(api_key)s&append_to_response=videos',  # NOQA
        'movie_trailer': '/3/movie/%(movie_id)s/videos?api_key=%(api_key)s',  # NOQA
    }
    # Sending a request to TMDB's API based upon the user's request.
    conn.request("GET", tmdb_api_urls[tmdb_url] % kwargs)
    res = conn.getresponse()
    data = res.read()
    # Converting the JSON object to a dictonary.
    return json.loads(data.decode("utf-8"))


class User():
    """ User class stores information for a User to carry a tmdb session.
            For grading purposes a generic tmdb account is provided. """

    def __init__(self, api_key, username, password):
        self.api_key = api_key
        self.username = username
        self.password = password
        self.__request_token(api_key)
        self.__session_id(api_key, username, password, self.request_token)

    def __request_token(self, api_key):
        """ When a user accesses TMDB's API a request token is generated for
                authentication purposes. """
        request_token = _tmdb_api_call('request_token', api_key=api_key)
        self.request_token = request_token['request_token']

    def __session_id(self, api_key, username, password, request_token):
        # Authenticating the User's request_token prior to creating a session_id.
        auth_token = _tmdb_api_call('auth_token', api_key=api_key,
                                    username=username,
                                    password=password,
                                    request_token=request_token)
        # Creating a TMDB session_id used for API calls.
        session_id = _tmdb_api_call('session_id', api_key=api_key,
                                    request_token=request_token)
        self.session_id = session_id['session_id']

    def favorite_movies(self):
        """ favorite_movies returns a dict containing the User's favorite
                movies. """

        movies = _tmdb_api_call('favorite_movies', api_key=self.api_key,
                                username=self.username,
                                session_id=self.session_id)
        # Getting the User's favorite movie's IDs.
        """ NOTE: TMDB favorite movie's request does not return all the required
                movie details.  An additional API call is required. """
        movie_ids = []
        for movie in movies['results']:
            movie_ids.append(str(movie['id']))

        # Getting the details for the User's favorite movies.
        movies = []
        for movie_id in movie_ids:
            movies.append(_tmdb_api_call('movie_details',
                                         api_key=self.api_key,
                                         movie_id=movie_id))
        return movies


# Below are depreciated functions that will be removed during production.

def _get_movie_trailer(movie_id, api_key):
    """ _get_movie_trailer returns the YouTube URL for a movie. """

    trailers = _tmdb_api_call('movie_trailer', api_key=api_key,
                              movie_id=str(movie_id))

    youtube_url = "https://www.youtube.com/watch?v={key}".format(
        key=trailers['results'][0]['key'])

    return youtube_url
