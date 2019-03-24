# CyberWarrior Scoring System 

This WebApp was created to serve as a method of tracking team progress throughout the BestCyberWarrior event. 

This App can be rewritten and customized for any event that requires points or team validated 

## Environment:
- Flask
- Jinja2 Templates
- Monogdb

For this app there are some important endpoints to discuss. the ends points can provide data from the database 
that can be crucial for 

## Key Features
- Instant Validation
- Position Tracking 
- Custom Game Entries 
- Live Leaderboard 

## Endpoints
- /getscore - Gets the score of the the provided team. 
- /validate_resp - validates the question field of the provide user team
- /buzzed - Represents a user using the buzzing feature 

## Data Models


#### Team Model
```json
{
    "name" : "team1",
    "passwd" : "team1",
    "responses" : [
        {
            "event_id" : "",
            "q_id" : "",
            "response" : "",
            "points_awarded" : false,
            "point_value": 0
        }
    ],
    "points" : 0
}
```

#### Buzzer Model
```json
{
  "event_id": "",
  "team_responses": [
    {
      "team_name": "",
      "response": "",
      "time_stamp": 0,
      "submitted": false
    }
  ]
}
```

#### Event Model
```json
{    
    "event_id" : "",
    "artifacts" : {
        "file" : ""
    },
    "questions" : [ 
        {
            "q_id" : "",
            "text" : "",
            "answer" : "",
            "point_value" : 0,
            "validation" : []
        }
    ]
	
	}
```
