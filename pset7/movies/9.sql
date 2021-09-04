SELECT DISTINCT people.name FROM people
jOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE movies.year = 2004
ORDER BY people.birth;