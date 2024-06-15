// src/App.jsx

import React from 'react';
import './App.css';
import CompetitionsList from './components/CompetitionsList';
import CompetitorsList from './components/CompetitorsList';
import MatchesList from './components/MatchesList';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/" element={<CompetitionsList />} />
                    <Route path="/competitions/:competitionId/competitors" element={<CompetitorsList />} />
                    <Route path="/competitions/:competitionId/competitors/:competitorId/matches" element={<MatchesList />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
