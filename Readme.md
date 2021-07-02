## Instructions to run the code

1. Docker Process
    
    a. Create Docker Image
    ```
    docker build <Docker File Path> -t <Name of Image(Say Order)>
    ```

    b. Run Docker Image
    ```
    docker run -p 5000:5000 -d <Name of Image>
    ```

2. Normal Process

    a. Install dependencies
    ```
     pip install -r <PAth of requirements.txt>
    ```

    b. Run the Flask App
    
    ```
    python run <Path of app.py>
    ```

## Technical Decisions Made

1. Flask Api was used instead of Django framework \
    Reason: Since it was single api not involving model per se.

2. Library flask_expects_json \
    Reason: Incoming json schema was known

3. Schema for stored as a yaml \
    Reason: Make it more readable and clean 