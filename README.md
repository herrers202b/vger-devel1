
# VGER: Virtual Guide for Educational Readiness

  

VGER is a web application written in django framework with a mariadb backend. The purpose of VGER is to survey

college students about their covid-19 experience and its relations to their eduction.

  

## Dependencies

The only dependecy required before running is docker which will subsequently build the images required for running

* Docker

    * Django

    * Mariadb

  

## Usage

  

### How to spin up the server

```shell

python3 run.py build

python3 run.py up

```

open your browser and go to localhost:8000

  

---

### ``run.py`` usage

this is to help navigate project functionality.

  **migrate**   
> makes migrations and applies them
  
**up [-d]**   
> spins up the djangosite [runs quietly]

**down** 
> brings the docker container down

**build** 
> builds docker-compose images

**admin ** 
> creates a new superuser

**inspectdb** 
> inspects the django database setups

**own** 
> changes current user to new owner of all subdirectors

**startapp 'name'** 
> creates a new app subdirectory with given name (required)

**test** 
> runs all test files in project apps, optional app name to test specific app

---

### ``runInitial.py`` usage
> Initial Install Script: initializes/installs the database, in order to start running the product

---

### ``runVger.py`` usage
> NOTE: it is REQUIRED that the initialization script has been run before the start script

> Run System Start Script: starts the system. 

> To spin the system back down make sure you either run 'docker-compose down' or you run 'closeVger.py'

---

### ``runTests.py`` usage
> NOTE: it is REQUIRED that the initialization script has been run before the tests script

> Run Tests Script: runs all test files in project apps for all Operating Systems

---

### ``closeVger.py`` usage
> spins the system down, preferably used after 'runVger.py'



