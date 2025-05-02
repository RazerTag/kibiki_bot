import os
import csv
from datetime import datetime

# Directory for CSV storage
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')

# File paths
USERS_FILE = os.path.join(DATA_DIR, 'users.csv')
EVENTS_FILE = os.path.join(DATA_DIR, 'events.csv')
HISTORY_FILE = os.path.join(DATA_DIR, 'history.csv')
POINTS_FILE = os.path.join(DATA_DIR, 'points.csv')
ANNOUNCEMENTS_FILE = os.path.join(DATA_DIR, 'announcements.csv')


def init_csv_files():
    """
    Initialize the data directory and CSV files with headers if they do not exist.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    files = {
        USERS_FILE: ['user_id', 'username', 'first_name', 'last_name', 'registered_at'],
        EVENTS_FILE: ['event_id', 'name', 'date', 'location', 'points'],
        HISTORY_FILE: ['user_id', 'event_id', 'timestamp'],
        POINTS_FILE: ['user_id', 'points'],
        ANNOUNCEMENTS_FILE: ['announcement_id', 'timestamp', 'text'],
    }
    for path, headers in files.items():
        if not os.path.exists(path):
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)


def add_user(user_id: int, username: str, first_name: str, last_name: str) -> None:
    """
    Register a new user and initialize their points to 0.
    """
    if not is_user_registered(user_id):
        now = datetime.utcnow().isoformat()
        # Append to users file
        with open(USERS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([user_id, username, first_name, last_name, now])
        # Initialize points
        with open(POINTS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([user_id, 0])


def is_user_registered(user_id: int) -> bool:
    """
    Check if a user is already registered.
    """
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['user_id']) == user_id:
                return True
    return False


def get_all_users() -> list[dict]:
    """
    Return a list of all registered users as dicts.
    """
    users = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(row)
    return users


def save_event(name: str, date: str, location: str, points: int) -> int:
    """
    Create a new event and return its generated event_id.
    """
    # Determine next event_id
    next_id = 1
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            ids = [int(row['event_id']) for row in reader]
            if ids:
                next_id = max(ids) + 1
    # Append to events file
    with open(EVENTS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([next_id, name, date, location, points])
    return next_id


def get_all_events() -> list[dict]:
    """
    Return a list of all events as dicts.
    """
    events = []
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                events.append(row)
    return events


def add_history(user_id: int, event_id: int) -> None:
    """
    Record a check-in event for a user.
    """
    now = datetime.utcnow().isoformat()
    with open(HISTORY_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, event_id, now])


def get_user_history(user_id: int) -> list[dict]:
    """
    Return a list of history records for a given user.
    """
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['user_id']) == user_id:
                    history.append(row)
    return history


def get_user_points(user_id: int) -> int:
    """
    Return current points for a user.
    """
    if not os.path.exists(POINTS_FILE):
        return 0
    with open(POINTS_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['user_id']) == user_id:
                return int(row['points'])
    return 0


def set_user_points(user_id: int, points: int) -> None:
    """
    Set a user's points to a specific value.
    """
    rows = []
    if os.path.exists(POINTS_FILE):
        with open(POINTS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    updated = False
    for row in rows:
        if int(row['user_id']) == user_id:
            row['points'] = points
            updated = True
            break
    if not updated:
        rows.append({'user_id': user_id, 'points': points})
    with open(POINTS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['user_id', 'points'])
        for row in rows:
            writer.writerow([row['user_id'], row['points']])


def increment_user_points(user_id: int, delta: int) -> None:
    """
    Increment a user's points by delta.
    """
    current = get_user_points(user_id)
    set_user_points(user_id, current + delta)


def get_leaderboard() -> list[tuple]:
    """
    Return a sorted list of (user_id, points) descending.
    """
    board = []
    if os.path.exists(POINTS_FILE):
        with open(POINTS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                board.append((int(row['user_id']), int(row['points'])))
    return sorted(board, key=lambda x: x[1], reverse=True)


def save_announcement(text: str) -> int:
    """
    Save a new announcement and return its ID.
    """
    if not os.path.exists(ANNOUNCEMENTS_FILE):
        init_csv_files()
    next_id = 1
    if os.path.exists(ANNOUNCEMENTS_FILE):
        with open(ANNOUNCEMENTS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            ids = [int(row['announcement_id']) for row in reader]
            if ids:
                next_id = max(ids) + 1
    timestamp = datetime.utcnow().isoformat()
    with open(ANNOUNCEMENTS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([next_id, timestamp, text])
    return next_id


def get_all_announcements() -> list[dict]:
    """
    Return a list of all announcements as dicts.
    """
    announcements = []
    if os.path.exists(ANNOUNCEMENTS_FILE):
        with open(ANNOUNCEMENTS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                announcements.append(row)
    return announcements
