# Soccer Fan Hub

This website will be all about women's professional soccer.


## Main Features

- **Match Details:** Get info on upcoming and past matches, including lineups and stats.
- **Live Scores:** Stay updated with ongoing match scores.
- **Filtering Options:** Find matches by country, location, league, or date.

## Technologies Used

- **Frontend:** React
- **Backend:** Django
- **Database:** Postgres
- **APIs:** Integrated soccer data APIs for live scores and match details.
- **Containerization:** Docker, Docker Compose

## Database Schema

### Teams

- **_id:** Primary Key
- **teamName:** Name of the team
- **country:** Country of the team
- **league:** League the team belongs to
- **logoURL:** URL of the team's logo
- **players:** Array of playerIds in the team

### Matches

- **_id:** Primary Key
- **homeTeamId:** Foreign Key referencing Teams for home team
- **awayTeamId:** Foreign Key referencing Teams for away team
- **startTime:** Start time of the match
- **endTime:** End time of the match
- **location:** Location of the match
- **league:** League of the match
- **score:** Score of the match
- **status:** Status of the match (e.g., 'scheduled', 'in progress', 'finished')
- **events:** Array of event objects, such as goals, cards, etc.

## Stretch Goals

- **User Authentication:** Allow users to register and log in.
- **Favorite Teams and Matches:** Let users choose and manage their favorite teams.
