import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PirateProfile from './PirateProfile';
import Quests from './Quests';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<PirateProfile />} />
          <Route path="/quests" element={<Quests />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;