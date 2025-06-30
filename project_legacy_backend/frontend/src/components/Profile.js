
import React from 'react';
import './Profile.css';

const Profile = () => {
    return (
        <div className="profile-container">
            <div className="profile-header">
                <h1>Captain "Redbeard" Vera</h1>
                <img src="https://i.imgur.com/tP3Q2gE.png" alt="Pirate Avatar" className="profile-avatar" />
            </div>
            <div className="profile-body">
                <h2>Ship's Log</h2>
                <p>Sailed the seven seas, plundered treasures, and lived a life of adventure. Feared by many, respected by all. Currently seeking a new quest.</p>
                <h2>Stats</h2>
                <ul>
                    <li>Gold Doubloons: 1,000,000</li>
                    <li>Ships Sunk: 42</li>
                    <li>Reputation: Legendary</li>
                </ul>
            </div>
        </div>
    );
};

export default Profile;
