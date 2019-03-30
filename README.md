# Customer Scoring System 

This WebApp was created to serve as a method of tracking team progress throughout the BestCyberWarrior event. 

This App can be rewritten and customized for any event that requires points or team validated 

## Environment:
- Flask
- Jinja2 Templates
- Monogdb

For this app there are some important endpoints to discuss. the ends points can provide data from the database 
that can be crucial for 

## Key Features
- Response validation function 
- Position Tracking 
- Custom Game Entries 
- Live Leaderboard 

## Endpoints
- /register['POST'] - Registers a new team to the database. 
- /unregister['POST']  - unRegisters a team in the database.
- /getteamscore['POST']  - Gets the current score for the specified team
- /reset_response['POST']  - Resets the responses and clear the points for the name provided 
- /validate['POST']  - Validates the user input for the question located in the events database 
- /team_buzzed['POST']  - Creates buzzed record in the buzzer_tracker database. This function will timestamp each buzzed event.
- /clear_buzz['POST']  - Clears the buzz entry from the buzz tracker database.
- /onload_buzz_check['POST']  - Frontend function used to load the buzzer database onpage load.
- /new_event['POST']  - Adds a new event to the database.
- /new_event_question['POST']  - Adds new questions to the supplied event ID.
- /remove_event_question['POST']  - Removes a list of questions from an event.
- /remove_event['POST']  - Removes an event from the database.
- /leaderboard['GET']  - Retrieves the current team standings of the game.



## Data Models


#### Team Model
```json
{
    "name" : "",
    "passwd" : "",
    "responses" : [],
    "points" : 0
}
```

#### Buzzer Model
```json
{
    "team_name" : "",
    "response" : "",
    "time_stamp" : 1553420336.01914,
    "time" : "",
    "submitted" : true
}
```

#### Event Model
```json
{    
    "event_id" : "",
    "title" : "",
    "artifacts" : {},
    "questions" : []
	
	}
```
