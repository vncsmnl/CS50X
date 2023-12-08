-- Log SQL queries for reference
-- ...

-- Check Crime Report on the day of the crime (28/7/2020)
SELECT * FROM crime_scene_reports WHERE year = 2020 AND month = 7 AND day = 28;

-- Check witness interviews for mentions of the Courthouse
SELECT * FROM interviews WHERE year = 2020 AND month = 7 AND day = 28 AND transcript LIKE "%Courthouse%";

-- Extract potential getaway vehicles from Courthouse Security Logs
SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25;

-- Identify individuals withdrawing money from Fifer Street ATM on the day of the crime
SELECT people.name, atm_transactions.account_number FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw";

-- Cross-reference suspects from Security Logs and ATM Transactions
SELECT DISTINCT people.name FROM people
JOIN courthouse_security_logs ON people.license_plate = courthouse_security_logs.license_plate
WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25
INTERSECT
SELECT DISTINCT people.name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street";

-- Explore flights leaving the city on the day after the crime
SELECT * FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city LIKE "Fiftyville") AND year = 2020 AND month = 7 AND day = 29 ORDER BY hour;

-- Retrieve passenger information for the earliest flight
SELECT people.name, people.passport_number, people.phone_number FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id = (SELECT id FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city LIKE "Fiftyville") AND year = 2020 AND month = 7 AND day = 29 ORDER BY hour LIMIT 1);

-- Narrow down suspects based on flight information
SELECT DISTINCT people.name FROM people
JOIN courthouse_security_logs ON people.license_plate = courthouse_security_logs.license_plate
WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25
INTERSECT
SELECT DISTINCT people.name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street"
INTERSECT
SELECT DISTINCT people.name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id = (SELECT id FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city LIKE "Fiftyville") AND year = 2020 AND month = 7 AND day = 29 ORDER BY hour LIMIT 1);

-- Investigate phone records of remaining suspects
SELECT people.name, phone_calls.* FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE year = 2020 AND month = 7 AND day = 28
INTERSECT
SELECT people.name, phone_calls.* FROM phone_calls
JOIN people ON phone_calls.caller = people.phone_number
WHERE name IN ("Danielle", "Ernest");

-- Identify the thief's escape destination
SELECT airports.* FROM airports
JOIN flights ON airports.id = flights.destination_airport_id
WHERE flights.id = (SELECT id FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city LIKE "Fiftyville") AND year = 2020 AND month = 7 AND day = 29 ORDER BY hour LIMIT 1);

-- Determine the thief's accomplice
SELECT * FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE id = 233 ORDER BY duration LIMIT 1);
