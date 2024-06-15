// src/components/MatchesList.jsx

import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Header from './Header';

function MatchesList() {
    const { competitionId, competitorId } = useParams();
    const [matches, setMatches] = useState([]);

    useEffect(() => {
        const fetchMatches = async () => {
            const url = `http://localhost:8000/api/competitions/${competitionId}/competitors/${competitorId}/matches/`;
            const response = await fetch(url);
            const data = await response.json();
            const sortedMatches = data.matches.sort((a, b) => new Date(a.start_time) - new Date(b.start_time));
            setMatches(sortedMatches);
        };

        fetchMatches();
    }, [competitionId, competitorId]);

    // Separate matches into upcoming and past matches based on their status
    const upcomingMatches = matches.filter(match => match.status === 'not_started' || match.status === 'postponed');
    const pastMatches = matches.filter(match => match.status === 'closed');

    return (
        <div className="MatchesList">
            <Header />
            <h2>Matches of Competitor</h2>

            {/* Upcoming Matches */}
            <section>
                <h3>Upcoming Matches</h3>
                <ul className="match-list">
                    {upcomingMatches.map((match) => (
                        <li key={match.id} className="match">
                            <div className="match-date">{new Date(match.start_time).toLocaleString()}</div>
                            <div className="match-teams">
                                {match.home_team} <br />
                                <strong>vs</strong> <br />
                                {match.away_team}
                            </div>
                        </li>
                    ))}
                </ul>
            </section>

            {/* Past Matches */}
            <section>
                <h3>Past Matches</h3>
                <ul className="match-list">
                    {pastMatches.map((match) => (
                        <li key={match.id} className="match">
                            <div className="match-date">{new Date(match.start_time).toLocaleString()}</div>
                            <div className="match-teams">
                                {match.home_team} {match.home_score !== null ? match.home_score : '-'} <br />
                                <strong>vs</strong> <br />
                                {match.away_team} {match.away_score !== null ? match.away_score : '-'}
                            </div>
                        </li>
                    ))}
                </ul>
            </section>
        </div>
    );
}

export default MatchesList;
