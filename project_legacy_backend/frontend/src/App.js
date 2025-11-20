import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
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
          <Route path="/login" element={<Login />} />
          <Route path="/auth/callback" element={<AuthCallback />} />
          <Route
            path="/"
            element={
              localStorage.getItem('authToken') ? (
                <Navigate to="/profile" replace />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/profile"
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
