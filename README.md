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

### Competitions

- **id:** Primary Key (string)
- **name:** Name of the competition (string)
- **gender:** Gender category (string)
- **category_id:** Category ID (string)
- **category_name:** Category name (string)
- **country_code:** Country code (nullable string)

### Competitors

- **id:** Primary Key (string)
- **name:** Name of the competitor (string)
- **country:** Country of the competitor (nullable string)
- **abbreviation:** Abbreviation of the competitor (nullable string)
- **gender:** Gender category (nullable string)

### Matches

- **id:** Primary Key (string)
- **competition_id:** Foreign Key referencing Competitions (string)
- **season_id:** Season ID (string)
- **start_time:** Start time of the match (DateTime)
- **home_team_id:** Foreign Key referencing Competitors for home team (string)
- **away_team_id:** Foreign Key referencing Competitors for away team (string)
- **home_score:** Score of the home team (integer)
- **away_score:** Score of the away team (integer)
- **status:** Status of the match (string, e.g., 'scheduled', 'in progress', 'finished')
- **winner_id:** Foreign Key referencing Competitors for the winner team (nullable string)

## Stretch Goals

- **User Authentication:** Allow users to register and log in.
- **Favorite Teams and Matches:** Let users choose and manage their favorite teams.
