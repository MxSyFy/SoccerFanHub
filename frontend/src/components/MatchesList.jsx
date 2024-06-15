// src/components/MatchesList.jsx

import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Header from './Header';

function MatchesList() {
    const { competitionId, competitorId } = useParams();
    const [matches, setMatches] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchMatches = async () => {
            const url = `http://localhost:8000/api/competitions/${competitionId}/competitors/${competitorId}/matches/`;
            try {
                const response = await fetch(url);
                if (response.ok) {
                    const data = await response.json();
                    if (data && data.matches) {
                        // Sort matches by start_time (assuming start_time is in ISO format)
                        const sortedMatches = data.matches.sort((a, b) => new Date(a.start_time) - new Date(b.start_time));
                        setMatches(sortedMatches);
                    } else {
                        setError('No matches data found');
                    }
                } else {
                    setError('Failed to fetch matches');
                }
            } catch (error) {
                setError('Failed to fetch matches');
            }
        };

        fetchMatches();
    }, [competitionId, competitorId]);

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="MatchesList">
            <Header />
            <h2>Matches of Competitor</h2>
            <ul className="match-list">
                {matches.map((match) => (
                    <li key={match.id} className="match">
                        <div className="match-date">{new Date(match.start_time).toLocaleString()}</div>
                        <div className="match-teams">
                            {match.home_team} {match.home_score} <br />
                            {match.away_team} {match.away_score}
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default MatchesList;
