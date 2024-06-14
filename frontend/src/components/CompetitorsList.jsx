// src/components/CompetitorsList.jsx

import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function CompetitorsList() {
  const { competitionId } = useParams();
  const [competitors, setCompetitors] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(`http://localhost:8000/api/competitions/${competitionId}/competitors/`);

      if (response.ok) {
        const data = await response.json();
        if (data && data.competitors) {
          const sortedCompetitors = data.competitors.sort((a, b) => a.name.localeCompare(b.name));
          setCompetitors(sortedCompetitors);
        } else {
          console.error('No competitors data found in response');
        }
      } else {
        console.error('Failed to fetch competitors');
      }
    };

    fetchData();
  }, [competitionId]);

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
