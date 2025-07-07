# RPG App Tests Documentation

This document outlines the purpose and functionality of the tests located in `rpg/tests.py`.

## Purpose

The `QuestFilteringTests` class in `rpg/tests.py` is designed to verify the correct filtering of daily quests based on the time of day. It ensures that the API endpoint `/rpg/api/quests/daily/` returns the appropriate quests for 'Morning', 'Afternoon', and 'Night' time slots.

## Test Methodology

Each test method within `QuestFilteringTests` follows a similar pattern:

1.  **Time Mocking**: The `django.utils.timezone.now` function is mocked using `@patch` to simulate specific times of the day (e.g., 9 AM for morning, 2 PM for afternoon, 9 PM for night). This allows for consistent testing of time-dependent logic.
2.  **User Authentication**: A test user is authenticated to simulate a logged-in player making a request to the API.
3.  **API Call**: A GET request is made to the `/rpg/api/quests/daily/` endpoint.
4.  **Assertions**:
    *   The HTTP status code of the response is asserted to be 200 (OK).
    *   The **number of quests** returned in the response is asserted to match the expected count for that specific time of day.
    *   For each returned quest, its `time_of_day` field is asserted to match the expected time slot (e.g., 'Morning' for `test_morning_quests`).

## Flexibility

These tests are designed to be flexible and robust. Unlike previous iterations, they **do not rely on specific quest names** (e.g., "Morning Jog", "Healthy Breakfast"). Instead, they focus on:

*   **Quantity**: Ensuring the correct number of quests are returned for each time slot.
*   **Structure**: Verifying that all returned quests for a given time slot correctly indicate that `time_of_day`.

This approach makes the tests more resilient to future changes in quest content or naming conventions, as long as the core filtering logic and the expected number of quests per time slot remain consistent.
