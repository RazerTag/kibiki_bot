import os
import csv
from datetime import datetime

# Directory for CSV storage\BASE_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')

# File paths
ANNOUNCEMENTS_FILE = os.path.join(DATA_DIR, 'announcements.csv')
USERS_FILE         = os.path.join(DATA_DIR, 'users.csv')
EVENTS_FILE        = os.path.join(DATA_DIR, 'events.csv')
HISTORY_FILE       = os.path.join(DATA_DIR, 'history.csv')
POINTS_FILE        = os.path.join(DATA_DIR, 'points.csv')


def init_csv_files():
    """
    Initialize the data directory and CSV files with headers if they do not exist.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    files = {
        ANNOUNCEMENTS_FILE: ['announcement_id', 'timestamp', 'text'],
        USERS_FILE:         ['user_id', 'username', 'first_name', 'last_name', 'registered_at', 'group'],
        EVENTS_FILE:       ['event_id', 'name', 'date', 'location', 'points'],
        HISTORY_FILE:      ['user_id', 'event_id', 'timestamp'],
        POINTS_FILE:       ['user_id', 'points'],
    }
    for path, headers in files.items():
        if not os.path.exists(path):
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)


def save_announcement(text: str) -> int:
    """
    Save a new announcement and return its ID.
    """
    init_csv_files()
    next_id = 1
    if os.path.exists(ANNOUNCEMENTS_FILE):
        with open(ANNOUNCEMENTS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            ids = [int(row['announcement_id']) for row in reader]
            if ids:
                next_id = max(ids) + 1
    ts = datetime.utcnow().isoformat()
    with open(ANNOUNCEMENTS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([next_id, ts, text])
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


def add_user(user_id: int, username: str, first_name: str, last_name: str) -> None:
    """
    Register a new user and initialize their points and group to defaults.
    """
    if not is_user_registered(user_id):
        now = datetime.utcnow().isoformat()
        # Append to users file
        with open(USERS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([user_id, username, first_name, last_name, now, ''])
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
        return any(int(row['user_id']) == user_id for row in reader)


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


def get_user_group(user_id: int) -> str:
    """
    Return the group of a user, or empty string if not set.
    """
    if not os.path.exists(USERS_FILE):
        return ''
    with open(USERS_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['user_id']) == user_id:
                return row.get('group', '')
    return ''


def set_user_group(user_id: int, group: str) -> bool:
    """
    Set the group for a user. Returns True if updated.
    """
    if not os.path.exists(USERS_FILE):
        return False
    rows = []
    updated = False
    with open(USERS_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['user_id']) == user_id:
                row['group'] = group
                updated = True
            rows.append(row)
    if updated:
        with open(USERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'username', 'first_name', 'last_name', 'registered_at', 'group'])
            for row in rows:
                writer.writerow([row['user_id'], row['username'], row['first_name'], row['last_name'], row['registered_at'], row['group']])
    return updated


def save_event(name: str, date: str, location: str, points: int) -> int:
    """
    Create a new event and return its generated event_id.
    """
    next_id = 1
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            ids = [int(row['event_id']) for row in reader]
            if ids:
                next_id = max(ids) + 1
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


def delete_event(event_id: int) -> bool:
    """Delete event by ID. Returns True if deleted."""
    if not os.path.exists(EVENTS_FILE):
        return False
    rows = []
    deleted = False
    with open(EVENTS_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['event_id']) == event_id:
                deleted = True
            else:
                rows.append(row)
    if deleted:
        with open(EVENTS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['event_id', 'name', 'date', 'location', 'points'])
            for row in rows:
                writer.writerow([row['event_id'], row['name'], row['date'], row['location'], row['points']])
    return deleted


def edit_event(event_id: int, *, name: str = None, date: str = None,
               location: str = None, points: int = None) -> bool:
    """Edit an event's fields. Returns True if updated."""
    if not os.path.exists(EVENTS_FILE):
        return False
    rows = []
    updated = False
    with open(EVENTS_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['event_id']) == event_id:
                if name is not None:     row['name']     = name
                if date is not None:     row['date']     = date
                if location is not None: row['location'] = location
                if points is not None:   row['points']   = str(points)
                updated = True
            rows.append(row)
    if updated:
        with open(EVENTS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['event_id', 'name', 'date', 'location', 'points'])
            for row in rows:
                writer.writerow([row['event_id'], row['name'], row['date'], row['location'], row['points']])
    return updated


def add_history(user_id: int, event_id: int) -> None:
    """Record a check-in event for a user."""
    ts = datetime.utcnow().isoformat()
    with open(HISTORY_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, event_id, ts])


def get_user_history(user_id: int) -> list[dict]:
    """Return a list of history records for a user."""
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['user_id']) == user_id:
                    history.append(row)
    return history


def get_user_points(user_id: int) -> int:
    """Return current points for a user."""
    if not os.path.exists(POINTS_FILE):
        return 0
    with open(POINTS_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['user_id']) == user_id:
                return int(row['points'])
    return 0


def set_user_points(user_id: int, points: int) -> None:
    """Set a user's points."""
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
    """Increment a user's points by delta."""
    current = get_user_points(user_id)
    set_user_points(user_id, current + delta)


def get_leaderboard() -> list[tuple]:
    """Return leaderboard sorted desc by points."""
    board = []
    if os.path.exists(POINTS_FILE):
        with open(POINTS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                board.append((int(row['user_id']), int(row['points'])))
    return sorted(board, key=lambda x: x[1], reverse=True)


def delete_user(user_id: int) -> bool:
    """Delete user and all related data. Returns True if found and deleted."""
    deleted = False
    # 1) users.csv
    rows = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                if int(r['user_id']) == user_id:
                    deleted = True
                else:
                    rows.append(r)
        if deleted:
            with open(USERS_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['user_id','username','first_name','last_name','registered_at','group'])
                for r in rows:
                    writer.writerow([r['user_id'],r['username'],r['first_name'],r['last_name'],r['registered_at'],r.get('group','')])
    # 2) points.csv
    rows = []
    if os.path.exists(POINTS_FILE):
        with open(POINTS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                if int(r['user_id']) != user_id:
                    rows.append(r)
                else:
                    deleted = True
        if deleted:
            with open(POINTS_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['user_id','points'])
                for r in rows:
                    writer.writerow([r['user_id'],r['points']])
    # 3) history.csv
    rows = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                if int(r['user_id']) != user_id:
                    rows.append(r)
                else:
                    deleted = True
        if deleted:
            with open(HISTORY_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['user_id','event_id','timestamp'])
                for r in rows:
                    writer.writerow([r['user_id'],r['event_id'],r['timestamp']])
    return deleted
