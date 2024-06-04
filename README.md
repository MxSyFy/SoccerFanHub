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

#### Users:

- **_id**: Primary Key
- **username**
- **email**
- **password**: (hashed)
- **favoriteTeams**: Array of teamIds
- **favoriteMatches**: Array of matchIds

#### Teams:

- **_id**: Primary Key
- **teamName**
- **country**
- **league**
- **logoURL**
- **players**: Array of playerIds

#### Matches:

- **_id**: Primary Key
- **homeTeamId**: Foreign Key referencing Teams
- **awayTeamId**: Foreign Key referencing Teams
- **startTime**
- **endTime**
- **location**
- **league**
- **score**
- **status**: (e.g., 'scheduled', 'in progress', 'finished')
- **events**: Array of event objects, such as goals, cards, etc.


