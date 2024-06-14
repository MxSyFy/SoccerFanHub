// src/components/CompetitionsList.jsx

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Header from './Header'; // Import the Header component

function CompetitionsList() {
  const [competitionsByCountry, setCompetitionsByCountry] = useState({});
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCompetitions = async () => {
      const response = await fetch('http://localhost:8000/api/competitions/');
      if (response.ok) {
        const data = await response.json();
        if (data && data.competitions) {
          const categorizedCompetitions = categorizeCompetitions(data.competitions);
          setCompetitionsByCountry(categorizedCompetitions);
        } else {
          setError('No competitions data found');
        }
      } else {
        setError('Failed to fetch competitions');
      }
      setLoading(false);
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

    const sortedCategories = Object.keys(categorized).sort((a, b) =>
      categorized[a].country.localeCompare(categorized[b].country)
    );

    const sortedCompetitionsByCountry = {};
    sortedCategories.forEach((country_code) => {
      sortedCompetitionsByCountry[country_code] = categorized[country_code];
      sortedCompetitionsByCountry[country_code].competitions.sort((a, b) =>
        a.name.localeCompare(b.name)
      );
    });

    return sortedCompetitionsByCountry;
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="CompetitionsList">
      <Header /> {/* Include the Header component */}
      <h2>List of Competitions</h2>
      {Object.keys(competitionsByCountry).map((countryCode) => (
        <div key={countryCode}>
          <h3>{competitionsByCountry[countryCode].country}</h3>
          <ul className="competition-list">
            {competitionsByCountry[countryCode].competitions.map((competition) => (
              <li key={competition.id}>
                <Link to={`/competitions/${competition.id}/competitors`}>
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
