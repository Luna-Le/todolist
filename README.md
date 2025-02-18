# To-Do List Web App

This is a To-Do List web app that helps users keep track of tasks they need to complete. Users can see, add, edit, and delete tasks. The backend is developed using FastAPI and the frontend is developed using React. The database is PostgreSQL. The app is deployed on docker containers in an AWS EC2 with Nginx as a reverse proxy. The url is https://todolistnow.com.



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


