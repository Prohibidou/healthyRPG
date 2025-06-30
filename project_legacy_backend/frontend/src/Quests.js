import React, { useState, useEffect } from 'react';
import './Quests.css';

function Quests() {
    const [quests, setQuests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchQuests = async () => {
            try {
                const token = localStorage.getItem('authToken');
                if (!token) {
                    throw new Error('Authentication token not found. Please log in.');
                }

                const response = await fetch('/rpg/api/quests/daily/', {
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                setQuests(data);
            } catch (e) {
                setError(e.message);
            } finally {
                setLoading(false);
            }
        };

        fetchQuests();
    }, []);

    if (loading) {
        return <div className="quests-container"><h1>Loading Quests...</h1></div>;
    }

    if (error) {
        return <div className="quests-container"><h1>Error: {error}</h1></div>;
    }

    return (
        <div className="quests-container">
            <h1>daily missiones !! come on buddy you can do it, time to improve yourself !</h1>
            {quests.length === 0 ? (
                <p>No quests found. Time to relax on the deck!</p>
            ) : (
                <div className="quest-list">
                    {quests.map(quest => (
                        <div key={quest.id} className="quest-item">
                            <h2>{quest.name}</h2>
                            <p>{quest.description}</p>
                            <p><strong>Type:</strong> {quest.quest_type}</p>
                            <p><strong>Reward:</strong> {quest.xp_reward} XP</p>
                            {/* Add a button to complete quest later */}
                        </div>
                    ))}
                </div>
            )}
            <div className="back-link">
                <a href="/">Return to Ship (Profile)</a>
            </div>
        </div>
    );
}

export default Quests;
