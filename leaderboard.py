
# backend/services/leaderboard.py
from .gamification import get_leaderboard
def fetch_leaderboard():
    return get_leaderboard()