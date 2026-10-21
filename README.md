Project builds a REST API for an events platform. The API will allow users to register, browse events, RSVP, and manage their attendance. Organisers will be able to create and manage events, and view statistics about their audience.

## DATABASE SET UP 
1. Create the local Postgres database:
   ```bash
   createdb nc_plus_one
   ```
2. Run the setup script:
   ```bash
   psql -f db/setup.sql 
   ```