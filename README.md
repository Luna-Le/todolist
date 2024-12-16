# To-Do List App

This is a To-Do List app that helps users keep track of tasks they need to complete. Users can see, add, edit, and delete tasks. The backend is developed using FastAPI and deployed on Docker, while the database is PostgreSQL. The frontend is developed using React, but it has not been deployed due to financial constraints.

## Table of Contents
- [Prerequisites](#prerequisites)
- [How to Run](#how-to-run)
- [Demo](#demo)
- [Running Tests](#running-tests)
- [Deploying Backend](#deploying-backend)


## Prerequisites
- Python 3.12 or higher
- Node.js version 18 or higher
- Docker and Docker Compose

## How to Run

1. **Clone the project from GitHub:**
   ```bash
   git clone https://github.com/Luna-Le/todolist.git
   cd todolist
   ```

2. **Open a terminal.**

   ### 2.1 Run Backend
   1. Navigate to the backend directory and create a virtual environment:
      ```bash
      cd backend
      python3 -m venv venv
      ```
   2. Activate the virtual environment:
      ```bash
      source venv/bin/activate
      ```
   3. Install all requirements:
      ```bash
      pip install -r requirements.txt
      ```
   4. Create an `.env` file with the necessary environment variables:
      ```plaintext
      DATABASE_HOSTNAME=localhost
      DATABASE_PORT=5432
      DATABASE_PASSWORD=your_password_here
      DATABASE_NAME=todolist
      DATABASE_USERNAME=postgres
      SECRET_KEY=your_secret_key_here
      ALGORITHM=HS256
      ACCESS_TOKEN_EXPIRE_MINUTES=60
      ```

   5. Run the backend:
      ```bash
      uvicorn app.main:app
      ```

   ### 2.2 Run Frontend
   1. Navigate to the frontend directory and install all requirements:
      ```bash
      cd ../frontend
      npm install
      ```
      Ensure Node.js is of version `>=18`.
      
   2. Run the frontend:
      ```bash
      npm run dev
      ```


## Demo
1. Upon opening the website, you will be asked to log in or register.
   - Click on "Register" if you have not created an account.
      ![Register](images/image.png)
   - After creating an account, you will be redirected to the login page to login.
      ![Login](images/image-1.png)

2. Once logged in, you will be on the home page where you can:
   - Add a task by typing in the task and clicking the "Add" button.
      ![Add Task](images/image-2.png)
   
   - Delete a task by clicking the "Delete" button.
      ![Delete Task](images/image-3.png)
   
   - Edit a task by clicking the "Edit" button, making your changes, and clicking "OK" to update it.
      ![Edit Task](images/image-4.png)

      ![Edit Task Confirmation](images/image-5.png)
   
   - Mark a task as done by clicking the checkbox, which will move it to the completed tasks.
      ![Mark Task Done](images/image-6.png)

      ![Completed Tasks](images/image-7.png)

3. To log out, click on the "Log Out" link in the navigation bar.
      ![Log Out](images/image-8.png)


## Running Tests
1. Stay in the main directory.
2. Create a `docker-compose.test.yml` file with the following content:
   ```yaml
   services:
     test_db:
       image: postgres:15
       ports:
         - "5434:5432"
       env_file:
         - backend/.env
       environment:
         - POSTGRES_USER=${DATABASE_USERNAME}
         - POSTGRES_PASSWORD=${DATABASE_PASSWORD}
         - POSTGRES_DB=${DATABASE_NAME}_test
       healthcheck:
         test: ["CMD-SHELL", "pg_isready -U postgres"]
         interval: 5s
         timeout: 5s
         retries: 5
   ```

3. Create a `Makefile` with the following content:
   ```makefile
   .PHONY: test-docker

   test-docker:
       docker-compose --env-file backend/.env -f docker-compose.test.yml up -d
       sleep 5
       pytest backend/tests
       docker-compose --env-file backend/.env -f docker-compose.test.yml down
   ```

4. Move to the main directory and run:
   ```bash
   make test-docker
   ```

## Deploying Backend
1. Stay in the main directory.
2. Create a `docker-compose.yml` file in the main directory with the following content:
   ```yaml
   services:
     api:
       build: ./backend
       ports:
         - "8000:80"
       env_file:
         - backend/.env
       depends_on:
         - postgres

     postgres:
       image: postgres:15
       ports:
         - "5433:5432"
       env_file:
         - backend/.env
       volumes:
         - postgres-db:/var/lib/postgresql/data

   volumes:
     postgres-db:
   ```

3. Run the command below to deploy:
   ```bash
   docker-compose --env-file backend/.env up --build -d
   ```