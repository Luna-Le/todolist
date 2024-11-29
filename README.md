## Testing Setup

1. Copy `docker-compose.test.template.yml` to `docker-compose.test.yml`
2. Create `.env.test` file and update the credentials:
    - Template for `.env.test` is:
    ```
    DB_USER=postgres
    DB_PASSWORD=your_secure_password
    DB_NAME=todolist

    ```
3. Update Makefile to use the env file:
    ```
    --env-file .env.test
    ```
4. Run tests with `make test-docker`
