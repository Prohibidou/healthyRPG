import React, { useState, useEffect } from 'react';

const PlayerProfile = () => {
    const [playerData, setPlayerData] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Function to get CSRF token from cookies
        const getCsrfToken = () => {
            const csrfCookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
            return csrfCookie ? csrfCookie.split('=')[1] : null;
        };

        const fetchPlayerProfile = async () => {
            try {
                const csrfToken = getCsrfToken();
                if (!csrfToken) {
                    throw new Error('CSRF token not found. Please ensure you are logged in.');
                }

                const response = await fetch('http://localhost:8000/rpg/api/profile/', { 
                    credentials: 'include',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                    }
                });
                if (response.status === 403) {
                    window.location.href = 'http://localhost:8000/admin/login/';
                    return;
                }
                if (response.redirected) {
                    window.location.href = response.url;
                    return;
                }
                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({ detail: 'Failed to parse error response.' }));
                    throw new Error(`HTTP error! status: ${response.status}, details: ${JSON.stringify(errorData)}`);
                }
                const data = await response.json();
                setPlayerData(data);
            } catch (err) {
                setError('Could not fetch player profile. See console for details.');
                console.error(err.message);
            }
        };

        fetchPlayerProfile();
    }, []);

    if (error) {
        return <div className="player-profile-error">{error}</div>;
    }

    if (!playerData) {
        return <div>Loading profile...</div>;
    }

    return (
        <div className="player-profile-container">
            <h1>Player Profile</h1>
            <div className="player-stats">
                <h2>Stats</h2>
                <p><strong>Level:</strong> {playerData.level}</p>
                <p><strong>XP:</strong> {playerData.xp}</p>
            </div>
            <div className="player-archetypes">
                <h2>Archetypes</h2>
                <div className="archetype">
                    <h3>Nutritional Archetype: {playerData.nutritional_archetype?.name}</h3>
                    <p>{playerData.nutritional_archetype?.description}</p>
                </div>
                <div className="archetype">
                    <h3>Physical Archetype: {playerData.physical_archetype?.name}</h3>
                    <p>{playerData.physical_archetype?.description}</p>
                </div>
                <div className="archetype">
                    <h3>Spiritual Path: {playerData.spiritual_path?.name}</h3>
                    <p>{playerData.spiritual_path?.description}</p>
                </div>
            </div>
        </div>
    );
};

export default PlayerProfile;