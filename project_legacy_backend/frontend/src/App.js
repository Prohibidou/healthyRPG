import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import PirateProfile from './PirateProfile';
import Quests from './Quests';
import Login from './Login';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              localStorage.getItem('authToken') ? (
                <PirateProfile />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/quests"
            element={
              localStorage.getItem('authToken') ? (
                <Quests />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
