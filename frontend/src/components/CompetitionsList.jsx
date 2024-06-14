// src/components/CompetitionsList.jsx

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function CompetitionsList() {
  const [competitionsByCountry, setCompetitionsByCountry] = useState({});

  useEffect(() => {
    const fetchCompetitions = async () => {
      const response = await fetch('http://localhost:8000/api/competitions/');
      if (response.ok) {
        const data = await response.json();
        if (data && data.competitions) {
          const categorizedCompetitions = categorizeCompetitions(data.competitions);
          setCompetitionsByCountry(categorizedCompetitions);
        } else {
          console.error('No competitions data found in response');
        }
      } else {
        console.error('Failed to fetch competitions');
      }
    };

    fetchCompetitions();
  }, []);

  const categorizeCompetitions = (competitions) => {
    const categorized = {};

    competitions.forEach((competition) => {
      const { country_code, name } = competition.category;

      if (!categorized[country_code]) {
        categorized[country_code] = {
          country: name,
          competitions: []
        };
      }

      categorized[country_code].competitions.push(competition);
    });

    // Sort competitions alphabetically by country name
    const sortedCategories = Object.keys(categorized).sort((a, b) =>
      categorized[a].country.localeCompare(categorized[b].country)
    );

    // Create a new object with sorted competitions by country
    const sortedCompetitionsByCountry = {};
    sortedCategories.forEach((country_code) => {
      sortedCompetitionsByCountry[country_code] = categorized[country_code];
      sortedCompetitionsByCountry[country_code].competitions.sort((a, b) =>
        a.name.localeCompare(b.name)
      );
    });

    return sortedCompetitionsByCountry;
  };

  return (
    <div className="CompetitionsList">
      <h1>List of Competitions</h1>
      {Object.keys(competitionsByCountry).map((countryCode) => (
        <div key={countryCode}>
          <h2>{competitionsByCountry[countryCode].country}</h2>
          <ul className="competition-list">
            {competitionsByCountry[countryCode].competitions.map((competition) => (
              <li key={competition.id}>
                <Link to={`/competitors/${competition.id}`}>
                  <strong>{competition.name}</strong>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

export default CompetitionsList;
