// src/components/CompetitorsList.jsx

import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function CompetitorsList() {
  const { competitionId } = useParams();
  const [competitors, setCompetitors] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const url = `http://localhost:8000/api/competitions/${competitionId}/competitors/`;
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        if (data && data.competitors) {
          const sortedCompetitors = data.competitors.sort((a, b) => a.name.localeCompare(b.name));
          setCompetitors(sortedCompetitors);
        } else {
          setError('No competitors data found');
        }
      } else {
        setError('Failed to fetch competitors');
      }
    };

    fetchData();
  }, [competitionId]);

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="CompetitorsList">
      <h1>List of Competitors</h1>
      <ul>
        {competitors.map((competitor) => (
          <li key={competitor.id}>{competitor.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default CompetitorsList;
