import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './PirateProfile.css';



function PirateProfile() {
    const [player, setPlayer] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Function to get CSRF token from cookies
        const getCsrfToken = () => {
            const csrfCookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
            return csrfCookie ? csrfCookie.split('=')[1] : null;
        };

        // Function to fetch player data from the Django API
        const fetchPlayerData = async () => {
            try {
                const authToken = localStorage.getItem('authToken');
                if (!authToken) {
                    throw new Error('Auth token not found. Please log in again.');
                }

                const response = await fetch(`http://localhost:8000/rpg/api/profile/`, {
                    headers: {
                        'Authorization': `Token ${authToken}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                setPlayer(data);
            } catch (e) {
                setError(e.message);
            } finally {
                setLoading(false);
            }
        };

        fetchPlayerData();
    }, []);

    if (loading) {
        return <div className="profile-container"><h1>Loading Crew Manifest...</h1></div>;
    }

    if (error) {
        return <div className="profile-container"><h1>Error: {error}</h1></div>;
    }

    if (!player) {
        return <div className="profile-container"><h1>No Player Data Found</h1></div>;
    }

    return (
        <div className="profile-container">
            <h1>Soldier's Log</h1>
            <div className="profile-stats">
                <p><strong>Rank:</strong> Level {player.level}</p>
                <p><strong>Bounty:</strong> {player.xp} XP</p>
                <p><strong>Rations Archetype:</strong> {player.nutritional_archetype?.name || 'Not Assigned'}</p>
                <p><strong>Training Regimen:</strong> {player.physical_archetype?.name || 'Not Assigned'}</p>
                <p><strong>Guiding Star:</strong> {player.spiritual_path?.name || 'Not Assigned'}</p>
            </div>
            <div className="profile-links">
                {/* This link will eventually go to the quests page */}
                <Link to="/quests">View a Treasure Map (Quests)</Link>
            </div>
        </div>
    );
}

export default PirateProfile;
