import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Quests.css';

const API_BASE_URL = 'http://localhost:8000';

function Quests() {
    const [quests, setQuests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeQuestId, setActiveQuestId] = useState(null); // State to track the quest being attempted

    const fetchQuests = async () => {
        try {
            const token = localStorage.getItem('authToken');
            if (!token) {
                throw new Error('Authentication token not found. Please log in.');
            }

            const response = await fetch(`${API_BASE_URL}/rpg/api/quests/daily/`, {
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

    useEffect(() => {
        fetchQuests();
    }, []);

    const handleQuestClick = (playerQuestId) => {
        setActiveQuestId(playerQuestId);
    };

    const handleCompleteQuest = async (playerQuestId) => {
        console.log('Attempting to complete quest with ID:', playerQuestId);
        try {
            const token = localStorage.getItem('authToken');
            if (!token) {
                throw new Error('Authentication token not found. Please log in.');
            }

            const response = await fetch(`${API_BASE_URL}/rpg/api/quests/complete/${playerQuestId}/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            alert(data.message); // Show success message
            setActiveQuestId(null); // Reset active quest
            fetchQuests(); // Re-fetch quests to update status and player stats

        } catch (e) {
            setError(e.message);
            alert(`Failed to complete quest: ${e.message}`);
        }
    };

    const handleCancelQuest = () => {
        setActiveQuestId(null); // Simply reset active quest
    };

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
                    {quests.map(playerQuest => (
                        <div key={playerQuest.id} className={`quest-item ${playerQuest.is_completed ? 'completed' : ''}`}>
                            <h2>{playerQuest.quest.name}</h2>
                            <p>{playerQuest.quest.description}</p>
                            <p><strong>Type:</strong> {playerQuest.quest.quest_type.name}</p>
                            <p><strong>Reward:</strong> {playerQuest.quest.xp_reward} XP</p>
                            {!playerQuest.is_completed && (
                                activeQuestId === playerQuest.id ? (
                                    <div className="quest-actions">
                                        <button onClick={() => handleCompleteQuest(playerQuest.id)}>Done</button>
                                        <button onClick={handleCancelQuest}>Couldn't do it</button>
                                    </div>
                                ) : (
                                    <button onClick={() => handleQuestClick(playerQuest.id)}>Begin Quest</button>
                                )
                            )}
                            {playerQuest.is_completed && <p className="completed-message">Completed!</p>}
                        </div>
                    ))}
                </div>
            )}
            <div className="back-link">
                <Link to="/">Return to Ship (Profile)</Link>
            </div>
        </div>
    );
}

export default Quests;