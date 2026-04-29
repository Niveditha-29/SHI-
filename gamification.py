user_points = {}
user_badges = {}

def add_points(user_id: str, action: str="query"):
    pts_map = {"query":5, "report":15, "tip":10}
    pts = pts_map.get(action, 5)
    user_points[user_id] = user_points.get(user_id, 0) + pts
    total = user_points[user_id]
    badges = []
    if total >= 200:
        badges.append("Gold Contributor")
    elif total >= 100:
        badges.append("Silver Contributor")
    elif total >= 50:
        badges.append("Bronze Contributor")
    user_badges[user_id] = badges
    return {"points": total, "badges": badges}

def get_leaderboard():
    items = sorted(user_points.items(), key=lambda x: x[1], reverse=True)
    return [{"user_id":u, "points":p, "badges": user_badges.get(u, [])} for u,p in items]


