Project builds a REST API for an events platform. The API will allow users to register, browse events, RSVP, and manage their attendance. Organisers will be able to create and manage events, and view statistics about their audience.

## DATABASE SET UP 
1. Create a venv and install all required packages from requirements.txt
2. Create the local Postgres database:
   ```bash
   createdb nc_plus_one
   ```
3. Run the setup script:
   ```bash
   psql -f db/setup.sql 
   ```

## CONNECTING TO THE DATABASE
A local .env.development should be created, with the keys listed in .env.example containing local database credentials
