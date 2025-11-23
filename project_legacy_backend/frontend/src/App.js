import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import PirateProfile from './PirateProfile';
import Login from './components/Login';
import AuthCallback from './components/AuthCallback';
import Quests from './Quests';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/PrivateRoute';
import Navbar from './components/Navbar';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Navbar />
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/auth/callback" element={<AuthCallback />} />
            <Route
              path="/"
              element={<Navigate to="/profile" replace />}
            />
            <Route
              path="/profile"
              element={
                <PrivateRoute>
                  <PirateProfile />
                </PrivateRoute>
              }
            />
            <Route
              path="/quests"
              element={
                <PrivateRoute>
                  <Quests />
                </PrivateRoute>
              }
            />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
