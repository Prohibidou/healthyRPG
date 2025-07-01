import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PirateProfile from './PirateProfile';
import Login from './components/Login';
import AuthCallback from './components/AuthCallback';
import Quests from './Quests';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/profile" element={<PirateProfile />} />
          <Route path="/auth/callback" element={<AuthCallback />} />
          <Route path="/quests" element={<Quests />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;