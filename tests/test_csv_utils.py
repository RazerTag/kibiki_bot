from __future__ import annotations

from pathlib import Path

import csv_utils


def configure_storage(tmp_path: Path) -> None:
    csv_utils.DATA_DIR = str(tmp_path)
    csv_utils.ANNOUNCEMENTS_FILE = str(tmp_path / "announcements.csv")
    csv_utils.USERS_FILE = str(tmp_path / "users.csv")
    csv_utils.EVENTS_FILE = str(tmp_path / "events.csv")
    csv_utils.HISTORY_FILE = str(tmp_path / "history.csv")
    csv_utils.POINTS_FILE = str(tmp_path / "points.csv")


def test_init_csv_files_creates_expected_headers(tmp_path: Path) -> None:
    configure_storage(tmp_path)

    csv_utils.init_csv_files()

    assert (tmp_path / "users.csv").read_text(encoding="utf-8").startswith(
        "user_id,username,first_name,last_name,registered_at,group"
    )
    assert (tmp_path / "events.csv").read_text(encoding="utf-8").startswith("event_id,name,date,location,points")
    assert (tmp_path / "points.csv").read_text(encoding="utf-8").startswith("user_id,points")


def test_user_points_and_leaderboard_flow(tmp_path: Path) -> None:
    configure_storage(tmp_path)
    csv_utils.init_csv_files()

    csv_utils.add_user(101, "alice", "Alice", "Smith")
    csv_utils.add_user(202, "bob", "Bob", "Jones")
    csv_utils.increment_user_points(101, 10)
    csv_utils.set_user_points(202, 15)

    assert csv_utils.get_user_points(101) == 10
    assert csv_utils.get_user_points(202) == 15
    assert csv_utils.get_leaderboard() == [(202, 15), (101, 10)]


def test_event_lifecycle_and_history(tmp_path: Path) -> None:
    configure_storage(tmp_path)
    csv_utils.init_csv_files()

    event_id = csv_utils.save_event("Demo", "2026-01-01T12:00:00", "Online", 5)

    assert event_id == 1
    assert csv_utils.edit_event(event_id, location="Remote", points=7)
    assert csv_utils.get_all_events()[0]["location"] == "Remote"
    assert csv_utils.get_all_events()[0]["points"] == "7"

    csv_utils.add_history(101, event_id)
    assert csv_utils.get_user_history(101)[0]["event_id"] == str(event_id)

    assert csv_utils.delete_event(event_id)
    assert csv_utils.get_all_events() == []


def test_delete_user_removes_related_points_and_history(tmp_path: Path) -> None:
    configure_storage(tmp_path)
    csv_utils.init_csv_files()

    csv_utils.add_user(101, "alice", "Alice", "Smith")
    event_id = csv_utils.save_event("Demo", "2026-01-01T12:00:00", "Online", 5)
    csv_utils.add_history(101, event_id)
    csv_utils.set_user_points(101, 42)

    assert csv_utils.delete_user(101)
    assert not csv_utils.is_user_registered(101)
    assert csv_utils.get_user_points(101) == 0
    assert csv_utils.get_user_history(101) == []
