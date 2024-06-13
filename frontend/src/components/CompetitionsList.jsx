import React, { useState, useEffect } from 'react';

function CompetitionsList() {
  const [competitions, setCompetitions] = useState([]);

  useEffect(() => {
    const fetchCompetitions = async () => {
      const response = await fetch('http://localhost:8000/api/competitions/')
        .catch(error => {
          console.error('Error fetching competitions:', error);
        });

      if (!response || !response.ok) {
        console.error('Failed to fetch competitions');
        return;
      }

      const data = await response.json().catch(error => {
        console.error('Error parsing JSON:', error);
      });

      if (data && data.competitions) {
        setCompetitions(data.competitions);
      }
    };

    fetchCompetitions();
  }, []);

  return (
    <div className="CompetitionsList">
      <h1>List of Competitions</h1>
      <ul className="competition-list">
        {competitions.map(competition => (
          <li key={competition.id}>
            <strong>{competition.name}</strong> - {competition.category.name} ({competition.gender})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CompetitionsList;
