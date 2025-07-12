
# Pending Features

## Group Quests by Time of Day

**User Request:** "i need a feature to show user his daily quests, but based on the current time. or at lest sorted by the time of the day, i mean a list of ' morning  --> listQuest ', ' afternoon --> listQuest' "

**Implementation Notes:**
- This will likely require adding a `time_of_day` attribute to the `Quest` model (e.g., 'Morning', 'Afternoon', 'Evening').
- The backend API (`/rpg/api/quests/daily/`) will need to be updated to return quests grouped by this new attribute.
- The frontend (`Quests.js`) will need to be updated to render the quests in their respective time-based groups.
