## Directions to run the application locally
**Note**: I am assuming everything I was told to set up in the instructions has already been set up for you.
This includes the ```okcapplicant``` role, the ```okc``` database, and the ```app``` schema. 
Also, do not forget to grant all relevant permission to the ```okcapplicant``` user.
However, unlike the instructions, I am using a traditional python environment (Python 3.9.12 in this application).\

For the frontend, I am assuming you have Node.js version 16.x.x like the instructions specified.
Also, you need Angular installed globally (like the instructions specified).

Here is step-by-step directions:

- Change directory into the backend portion of the application:
  ```
  cd /path/to/backend
  ```
- Create a Python virtual environment (it must be named 'okc'):
  ```
  python -m virtualenv okc
  ```
- Activate the virtual environment:
    - If on Windows:
        ```
        okc\Scripts\activate
        ```
    - If on Mac/Linux:
        ```
        source okc/bin/activate
        ```
- Install dependencies (everything will install in the virtual environment):
  ```
  pip install -r requirements.txt
  ```
- If your 'okc' database does not have the proper tables and relations, then we can use Django models and migrations to easily fill it:
  ```
  python manage.py makemigrations
  ```
  ```
  python manage.py migrate
  ```
- If your 'okc' database is not yet populated according to the JSON data, we can use a script to populate it.
  The script is located in ```backend/scripts/data.py``` and we can run it using a runscript command in Django:
  ```
  python manage.py runscript data
  ```
  It is completely safe to run this script more than once; no duplicates will be added to the database.
- Now, we can start the Django server:
  ```
  python manage.py runserver
  ```
  The server should be running on port 8000 on your local machine and should be retrieving data from a PostgreSQL database hosted on port 5432 on your local machine.
- Now, we start the Angular application. First cd in the frontend portion of the application:
  ```
  cd /path/to/frontend
  ```
- Install the dependencies if you have not done so already:
  ```
  npm install --force
  ```
- Start the Angular application which will run on port 4200 on your local machine:
  ```
  npm start
  ```
Now the frontend should be running on port 4200, the backend should be running on port 8000, and the database should be hosted on port 5432.

You can test out the application by visiting ```http://localhost:4200/player-summary```

Check out ```screenshots``` folder for UI demonstration. Visit each image in order for a solid grasp of how the UI is laid out.

Also, my answer to the system design prompt is located in the folder ```/system_design_prompt```.


[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/UDc3mhmF)

# OKC Technical Project Deliverable

### Internship Program Disclosures

* You must be eligible to work in the United States to be able to qualify for this internship.
  
* The pay for this internship is the greater of your local minimum wage and $13/hour.

* This application is for the purposes of an internship taking place in the Spring, Summer, or Fall of 2025.

### 1. Backend Engineering

* Architect and implement a normalized PostgreSQL database to store the data provided in `backend/raw_data`. All information from the original data should be accessible via the database.

* Write a brief description of your database architecture (<250 words). Feel free to provide a visual representation as an aide. Submit relevant responses in the `written_responses` folder provided.

* In the programming language of your choice, write a process to load the dataset into your PostgreSQL database. Ensure that this process can run repeatedly without duplicating or obscuring references in the database. Include the source code of your process in the `backend/scripts` folder. Note: You can feel free to utilize the power of Django models and migrations to achieve this step.

* After loading the data, export the state of your database using `pg_dump -U okcapplicant okc > dbexport.pgsql`. Include `dbexport.psql` in the `backend/scripts` folder.

* The skeleton of an API View `PlayerSummary` can be found in `backend/app/views/players.py`. Implement this API to return a player summary that mimics the structure of `backend/app/views/sample_response/sample_response.json`. Feel free to import additional modules/libraries in order to do this, but ensure that the `backend/requirements.txt` is updated accordingly. Viewing http://localhost:4200/player-summary-api allows you to see the output of your API, given the playerID parameter provided in the user input.

### 2. Frontend Engineering

* The `player-summary` component, which is viewable at http://localhost:4200/player-summary, makes a call to an API endpoint at `/api/v1/playerSummary/{playerID}` that returns player summary data. One component of the player summary data are the player's shots in each game, note that:

   * The shot's x and y coordinates are provided and are measured in feet
   * The location of each shot is relative to the center of the basket, per `court_diagram.jpg` in this repository

* Within the `player-summary` component found in `frontend/src/app/player-summary/`, create an interface that describes the player summary data returned from the API.

* Feel free to import additional modules of your choice, and design the interface however you wish. Just make sure that the `package.json` and `package-lock.json` are updated accordingly.

* Upon completion of the Frontend Engineering deliverable, please upload to this repo screenshots or screen captures that demonstrate your UI.


# Application Setup
In order to complete the Backend Engineering or Frontend Engineering deliverables, you will need to do all of the following setup items. Please follow the instructions below, from top to bottom sequentially, to ensure that you are set up to run the app. The app is run on an Angular frontend, Django backend, and a PostgreSQL database.

## Set up database
1. Download and install PostgreSQL from https://www.postgresql.org/download/
2. Ensure PostgreSQL is running, and in a terminal run
    ```
    createuser okcapplicant --createdb;
    createdb okc;
    ```
3. connect to the okc database to grant permissions `psql okc`
    ```
    create schema app;
    alter user okcapplicant with password 'thunder';
    grant all on schema app to okcapplicant;
    ```


## Backend

### 1. Install pyenv and virtualenv

Read about pyenv here https://github.com/pyenv/pyenv as well as info on how to install it.
You may also need to install virtualenv in order to complete step 2.

### 2. Installing Prerequisites
The steps below attempt to install Python version 3.10.1 within your pyenv environment. If you computer is unable to install this particular version, you can feel free to use a version that works for you, but note that you may also be required to update existing parts of the codebase to make it compatible with your installed version.
```
cd root/of/project
pyenv install 3.10.1
pyenv virtualenv 3.10.1 okc
pyenv local okc
eval "$(pyenv init -)" (may or may not be necessary)
pip install -r backend/requirements.txt
```

### 3. Starting the Backend
Start the backend by running the following commands
```
cd /path/to/project/backend
python manage.py runserver
```
The backend should run on http://localhost:8000/.


## Frontend

### 1. Installing Prerequisites
Install Node.js (16.x.x), then run the following commands
```
cd /path/to/project/frontend
# Install Angular-Cli
npm install -g @angular/cli@12.1.0 typescript@4.6.4 --force
# Install dependencies
npm install --force
```

### 2. Starting the Frontend
Start the frontend by running the following commands
```
cd /path/to/project/frontend
npm start
```
The frontend should run on http://localhost:4200/. Visit this address to see the app in your browser.


# SUBMISSION.md
Please fill out the SUBMISSION.md file to ensure we have your name attached to the project.


# Questions?

Email datasolutions@okcthunder.com
