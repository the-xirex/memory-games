"""Utility functions for application settings and configuration."""
import os
import sys
import json


def _get_app_folder():
    """Get the application data folder path."""
    if sys.platform == 'win32':
        app_data = os.getenv('APPDATA')
        app_folder = os.path.join(app_data, 'MemoryGames')
    else:
        app_folder = os.path.join(os.path.expanduser('~'), '.memorygames')
    
    if not os.path.exists(app_folder):
        os.makedirs(app_folder)
    
    return app_folder


def _get_records_file():
    """Get the path to the records JSON file."""
    return os.path.join(_get_app_folder(), 'records.json')


def load_records():
    """Load records from JSON file."""
    try:
        records_file = _get_records_file()
        if os.path.exists(records_file):
            with open(records_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading records: {e}")
    
    return {
        'Spatial Memory Game': 0,
        'Corsi Block Test': 0,
        'Memory Span': 0
    }


def save_records(records):
    """Save records to JSON file."""
    try:
        records_file = _get_records_file()
        with open(records_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving records: {e}")


def update_record(records, game_name, score):
    """
    Update record if new score is better.
    
    Args:
        records: Dictionary of game records
        game_name: Name of the game
        score: New score to compare
        
    Returns:
        Updated records dictionary
    """
    if score > records.get(game_name, 0):
        records[game_name] = score
        save_records(records)
    return records


def reset_records():
    """Reset all records to zero."""
    records = {
        'Spatial Memory Game': 0,
        'Corsi Block Test': 0,
        'Memory Span': 0
    }
    save_records(records)
    return records


def get_icon_path():
    """Get path to application icon."""
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(__file__))
        
        icon_path = os.path.join(base_path, 'brainstorm.ico')
        if os.path.exists(icon_path):
            return icon_path
    except Exception:
        pass
    return None

