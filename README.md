# Soccer Fan Hub

Welcome to Women's Soccer Hub! This platform is dedicated to providing enthusiasts of women's professional soccer with all the information they need about matches, schedules, and scores. 

## Features

- **User Authentication**: Users can create accounts and log in.
- **Match Details**: Access detailed information about upcoming and past matches, including team lineups, match statistics, and more.
- **Live Scores**: Stay up-to-date with live scores of ongoing matches.
- **Filtering Options**: Easily find matches by country, location, league, and date.
- **Favorite Teams and Matches**: Users can manage their favorite teams and matches to quickly access relevant information.

## Technologies Used

- **Frontend**: React
- **Backend**: Django
- **Database**: Postgres
- **Authentication**: JSON Web Tokens (JWT)
- **APIs**: Integration with soccer data APIs including Sportradar Soccer and API-Football for live scores and match details.


### Database Schema

| Collection | Field               | Description                                     |
|------------|---------------------|-------------------------------------------------|
| Users      | _id                 | Primary Key                                     |
|            | username            | User's username                                 |
|            | email               | User's email                                    |
|            | password            | User's hashed password                          |
|            | favoriteTeams       | Array of teamIds the user favorited             |
|            | favoriteMatches     | Array of matchIds the user favorited            |
| Teams      | _id                 | Primary Key                                     |
|            | teamName            | Name of the team                                |
|            | country             | Country of the team                             |
|            | league              | League the team belongs to                      |
|            | logoURL             | URL of the team's logo                          |
|            | players             | Array of playerIds in the team                  |
| Matches    | _id                 | Primary Key                                     |
|            | homeTeamId          | Foreign Key referencing Teams for home team     |
|            | awayTeamId          | Foreign Key referencing Teams for away team     |
|            | startTime           | Start time of the match                         |
|            | endTime             | End time of the match                           |
|            | location            | Location of the match                           |
|            | league              | League of the match                             |
|            | score               | Score of the match                              |
|            | status              | Status of the match (e.g., 'scheduled', 'in progress', 'finished') |
|            | events              | Array of event objects, such as goals, cards, etc. |



