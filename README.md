# Overview
There are totally three services, one is about useage statistics one is about prediction according to features that user input and last one is about the relationship which user want to observe.
# Insatllation
For backend you need do in the root directory:  

Step 1  

    pip3 install -r requirements.txt  
    
Step 2  

    python3  
    
    from rest import db, create_app  
    
    db.create_all(app=create_app())  
    
    exit()  
    
Step 3  

    export FLASK_APP=backend-select  
    
    export FLASK_ENV=development  
    
    flask run  
    
