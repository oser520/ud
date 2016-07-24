#!/usr/bin/env python

from media import Movie
import fresh_tomatoes


avatar = Movie(
    'Avatar', 'A marine on an alien planet.',
    'http://upload.wikimedia.org/wikipedia/id/b/b0/Avatar-Teaser-Poster.jpg',
    'https://www.youtube.com/watch?v=5PSNL1qE6VY')

ghd = Movie(
    'Groundhog Day', 'A man re-lives the same day until he gets it right.',
    'http://upload.wikimedia.org/wikipedia/en/b/b1/Groundhog_Day_(movie_poster).jpg',
    'https://www.youtube.com/watch?v=wE8nNUASSCo')

imitation_game = Movie(
    'The Imitation Game', 'A man invents computer science and a computer to win a war.',
    'http://upload.wikimedia.org/wikipedia/fi/a/a1/The_Imitation_Game.jpg',
    'https://www.youtube.com/watch?v=S5CjKEFb-sM')

matrix = Movie(
    'The Matrix', 'A computer hacker takes the wrong colored pill.',
    'http://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg',
    'https://www.youtube.com/watch?v=m8e-FF8MsqU')

wizard = Movie('The Wizard of Oz',
    'Transported to sureal landscape, a young girl kills the first person she meets and then teams up with three strangers to kill again.',
    'http://ia.media-imdb.com/images/M/MV5BMTU0MTA2OTIwNF5BMl5BanBnXkFtZTcwMzA0Njk3OA@@._V1_SX640_SY720_.jpg',
    'https://www.youtube.com/watch?v=VNugTWHnSfw')

live = Movie('Live Nude Girls',
    'A chick flick (without nudity) yet named to make it easier to get your boyfriend to watch it with you.',
    'http://upload.wikimedia.org/wikipedia/en/5/53/Live_nude_girls.jpg',
    'https://www.youtube.com/watch?v=8vXCajxxPcY')

#creates a list of the movies defined above and launches the web site.
movies = [avatar, ghd, imitation_game, matrix, live, wizard]
fresh_tomatoes.open_movies_page(movies)
