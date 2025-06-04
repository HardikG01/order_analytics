from fastapi import APIRouter, HTTPException
from redis_client import r

router = APIRouter()

@router.get("/users/{user_id}/stats")
def get_user_stats(user_id: str):
    key = f"user:{user_id}"
    if not r.exists(key):
        raise HTTPException(status_code=404, detail="User not found")

    data = r.hgetall(key)
    return {
        "user_id": user_id,
        "order_count": int(data.get(b"order_count", 0)),
        "total_spend": float(data.get(b"total_spend", 0.0))
    }

@router.get("/stats/global")
def get_global_stats():
    key = "global:stats"
    data = r.hgetall(key)
    return {
        "total_orders": int(data.get(b"total_orders", 0)),
        "total_revenue": float(data.get(b"total_revenue", 0.0))
    }

@router.get("/leaderboard/spend")
def get_top_spenders(n: int = 2):
    top_users = r.zrevrange("leaderboard:spend", 0, n - 1, withscores=True)
    return [
        {"user_id": user_id.decode(), "total_spend": score}
        for user_id, score in top_users
    ]

@router.get("/leaderboard/count")
def get_top_orderers(n: int = 2):
    top_users = r.zrevrange("leaderboard:count", 0, n - 1, withscores=True)
    return [
        {"user_id": user_id.decode(), "order_count": int(score)}
        for user_id, score in top_users
    ]
