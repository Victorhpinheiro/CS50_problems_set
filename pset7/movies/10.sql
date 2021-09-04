SELECT DISTINCT people.name FROM people
jOIN directors ON people.id = directors.person_id
JOIN ratings ON directors.movie_id = ratings.movie_id
WHERE ratings.rating > 8.9;