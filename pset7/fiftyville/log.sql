-- Keep a log of any SQL queries you execute as you solve the mystery.
-- It happened July 28 and took place on Chamberlin Street
-- airports, atm_transactions, bank_accounts, courthousr_security_logs, crimie_scene_reports, flights, interviews, passengers, people,
-- and phone_calls

-- First got the information from the crime report
SELECT * FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = "Chamberlin Street";
-- Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
-- Interviews were conducted today with three witnesses who were present at the time —
-- each of their interview transcripts mentions the courthouse.

--lets take a look at the interviews
SELECT * FROM interviews WHERE month =7 AND day = 28;
--10 minuites of theft the theft run with his car from the parking lot
--earlier the teft was at the ATM at Fifer Street
-- (as leaving court house and less than 1 minute)planning to take earliest flight the next day out of fiftyville and
-- ask accomplance to but flight ticket

-- Select all the licenses plate from suspect people
SELECT license_plate FROM courthouse_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25;

-- have the first list of suspects
SELECT name FROM people WHERE license_plate IN (SELECT license_plate
FROM courthouse_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25);

-- now lets check the second clue at the atm and get the bank accounts
SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw";

-- now lets cross the bank accounts with appropriate database and get their name (second list of suspects)
SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE bank_accounts.account_number IN (SELECT account_number FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw");

--lets update our suspect list by intersecting both (now have 4 suspects)
SELECT name FROM people WHERE license_plate IN (SELECT license_plate
FROM courthouse_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25)
INTERSECT
SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE bank_accounts.account_number IN (SELECT account_number FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw");

--lets cross the 3 clue and get all the callers suspect number
SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration <= 60;

-- now lets cross the phone number with the id
SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration <= 60);

-- crossing the 3 suspects list
SELECT name FROM people WHERE license_plate IN (SELECT license_plate
FROM courthouse_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25)
INTERSECT
SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE bank_accounts.account_number IN (SELECT account_number FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw")
INTERSECT
SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration <= 60);
-- now we have to names Ernest or Russel. Lets check the flights 

-- LETS GET ALL THE FLIGHTS LEAVING FROM FIFTYVILLE
SELECT id FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE month = 7 AND day = 29
ORDER BY hour
LIMIT 1;

-- lets get the passager list
SELECT passport_number FROM passengers
WHERE flight_id = (SELECT flights.id FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE month = 7 AND day = 29
ORDER BY hour
LIMIT 1);

-- CROSSING WITH PEOPLE
SELECT name FROM people 
WHERE passport_number IN (SELECT passport_number FROM passengers
WHERE flight_id = (SELECT flights.id FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE month = 7 AND day = 29
ORDER BY hour
LIMIT 1));

--cross with suspect list last time
SELECT name FROM people WHERE license_plate IN (SELECT license_plate
FROM courthouse_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25)
INTERSECT
SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE bank_accounts.account_number IN (SELECT account_number FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw")
INTERSECT
SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration <= 60)
INTERSECT
SELECT name FROM people 
WHERE passport_number IN (SELECT passport_number FROM passengers
WHERE flight_id = (SELECT flights.id FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE month = 7 AND day = 29
ORDER BY hour
LIMIT 1));
--Ernest

--lets get the helper
SELECT name FROM people
WHERE phone_number = (SELECT receiver FROM phone_calls
WHERE month = 7 AND day = 28 AND duration <= 60
AND caller = (SELECT phone_number FROM people WHERE name = "Ernest"));