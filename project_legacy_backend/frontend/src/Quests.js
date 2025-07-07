import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Quests.css';

const API_BASE_URL = '';

function Quests() {
    const [quests, setQuests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeQuestId, setActiveQuestId] = useState(null); // State to track the quest being attempted

    // Function to get CSRF token from cookies
    const getCsrfToken = () => {
        const csrfCookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
        return csrfCookie ? csrfCookie.split('=')[1] : null;
    };

    const fetchQuests = async () => {
        try {
            const authToken = localStorage.getItem('authToken');
            if (!authToken) {
                throw new Error('Auth token not found. Please log in again.');
            }

            const response = await fetch(`http://localhost:8000/rpg/api/quests/daily/`, {
                headers: {
                    'Authorization': `Token ${authToken}`,
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
            const authToken = localStorage.getItem('authToken');
            if (!authToken) {
                throw new Error('Auth token not found. Please log in again.');
            }

            const response = await fetch(`http://localhost:8000/rpg/api/quests/complete/${playerQuestId}/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${authToken}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            alert(data.message); // Show success message

            // --- START of the change ---
            // Update the local state to reflect the quest completion
            setQuests(currentQuests =>
                currentQuests.map(q =>
                    q.id === playerQuestId ? { ...q, is_completed: true } : q
                )
            );
            // --- END of the change ---

            setActiveQuestId(null); // Reset active quest

        } catch (e) {
            setError(e.message);
            alert(`Failed to complete quest: ${e.message}`);
        }
    };

    const handleCancelQuest = (playerQuestId) => {
        setQuests(currentQuests =>
            currentQuests.map(q =>
                q.id === playerQuestId ? { ...q, failed: true } : q
            )
        );
        setActiveQuestId(null); // Reset active quest
    };

    const groupQuestsByTimeOfDay = (quests) => {
        const groupedQuests = {
            Morning: [],
            Afternoon: [],
            Night: [],
        };

        quests.forEach(quest => {
            const timeOfDay = quest.quest.time_of_day;
            if (timeOfDay in groupedQuests) {
                groupedQuests[timeOfDay].push(quest);
            }
        });

        return groupedQuests;
    };

    const renderQuests = (quests) => {
        const groupedQuests = groupQuestsByTimeOfDay(quests);

        return Object.entries(groupedQuests).map(([timeOfDay, quests]) => (
            quests.length > 0 && (
                <div key={timeOfDay}>
                    <h2>{timeOfDay} Quests</h2>
                    <div className="quest-list">
                        {quests.map(playerQuest => (
                            <div key={playerQuest.id} className={`quest-item ${playerQuest.is_completed ? 'completed' : ''} ${playerQuest.failed ? 'failed' : ''}`}>
                                <h3>{playerQuest.quest.name}</h3>
                                <p>{playerQuest.quest.description}</p>
                                <p><strong>Type:</strong> {playerQuest.quest.quest_type.name}</p>
                                <p><strong>Reward:</strong> {playerQuest.quest.xp_reward} XP</p>
                                {!playerQuest.is_completed && !playerQuest.failed && (
                                    activeQuestId === playerQuest.id ? (
                                        <div className="quest-actions">
                                            <button onClick={() => handleCompleteQuest(playerQuest.id)}>Done</button>
                                            <button onClick={() => handleCancelQuest(playerQuest.id)}>Couldn't do it</button>
                                        </div>
                                    ) : (
                                        <button onClick={() => handleQuestClick(playerQuest.id)}>Begin Quest</button>
                                    )
                                )}
                                {playerQuest.is_completed && <p className="completed-message">Completed!</p>}
                                {playerQuest.failed && <p className="failed-message">Failed!</p>}
                            </div>
                        ))}
                    </div>
                </div>
            )
        ));
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
                <>
                    {renderQuests(quests)}
                    <div className="back-link">
                        <Link to="/">Return to Ship (Profile)</Link>
                    </div>
                </>
            )}
        </div>
    );
}

export default Quests;