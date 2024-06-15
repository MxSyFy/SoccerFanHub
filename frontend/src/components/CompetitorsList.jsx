// src/components/CompetitorsList.jsx

import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import Header from './Header';

function CompetitorsList() {
    const { competitionId } = useParams();
    const [competitors, setCompetitors] = useState([]);

    useEffect(() => {
        const fetchCompetitors = async () => {
            const url = `http://localhost:8000/api/competitions/${competitionId}/competitors/`;
            const response = await fetch(url);
            const data = await response.json();
            if (data && data.competitors) {
                setCompetitors(data.competitors);
            }
        };

        fetchCompetitors();
    }, [competitionId]);

    return (
        <div className="CompetitorsList">
            <Header />
            <h2>Competitors in Competition</h2>
            <ul>
                {competitors.map((competitor) => (
                    <li key={competitor.id} className="competitor">
                        <Link to={`/competitions/${competitionId}/competitors/${competitor.id}/matches`}>
                            {competitor.name}
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default CompetitorsList;
