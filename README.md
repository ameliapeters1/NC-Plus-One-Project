Project builds a REST API for an events platform. The API will allow users to register, browse events, RSVP, and manage their attendance. Organisers will be able to create and manage events, and view statistics about their audience.

## SET UP 
1. Fork and clone this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the Postgres database:
   Create the local database
   ```bash
   createdb nc_plus_one
   ```
   Run the database setup script to create the required tables:
    ```bash
   psql -f db/setup.sql
   ```
5. Create a .env.development file in the project root. 
   Use .env.example as a template to add local database credentials. 
   Add .env.development to .gitignore to ensure sensitive information is not commited to the repo.
6. Seed the database
   Populate the database with the given data
    ```bash
   python seed.py
   ```
7. Run the server
    ```bash
   uvicorn main:app --reload
   ```
   Once running, the API will be available at http://127.0.0.1:8000
8. Visit the docs
   Once the server is running, visit the automatically generated FastAPI docs at  http://127.0.0.1:8000/docs to see all available end points and test requests through Swagger UI.

## RUNNING TESTS
For tests, create a separate test database (for example nc_plus_one_test).
Create a .env.test file pointing to the test database.
To run tests use:
```bash
pytest
```
