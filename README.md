# Strassen algorithm demo app (MT79)
Web application demonstrating a python implementation of Strassen algorithm (square matrices multiplication)
Use Flask python micro-framework as built-in server

# Getting started
* Prerequisite
    - Python 2.7 or later version
    
* Install and run
    - Clone the repository
    - Install 
        - https://pip.pypa.io/en/stable/installing/
            - python get-pip.py
          
    - Install Flask
        - http://flask.pocoo.org/
            - pip install Flask
            
    - Install numpy
        - pip install numpy
    
    - Run python server
        - set FLASK_APP=strassen_demo_app.py
        - flask run
            
    - Enjoy at http://127.0.0.1:5000/strassen 

# TODO
- Make front-end look better
- Add a inline database to store (matrix size, computation_time, nb_multiplication) for each algorithm
- Use a data representation framework to display simple graphics from database
