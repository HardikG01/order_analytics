import json
import redis


r = redis.Redis(host='redis', port=6379, decode_responses=False)

def validate_order(order: dict) -> bool:
    """
    Validate that required fields exist and types are correct.
    Also check if order_value matches the calculated total from items.
    """
    try:
        # Check required fields exist
        if not all(k in order for k in ("order_id", "user_id", "order_value", "items")):
            print("Missing required fields")
            return False

        # Check data types
        if not isinstance(order["order_id"], str):
            print("Invalid order_id type")
            return False
        if not isinstance(order["user_id"], str):
            print("Invalid user_id type")
            return False
        if not isinstance(order["order_value"], (int, float)):
            print("Invalid order_value type")
            return False
        if not isinstance(order["items"], list):
            print("Invalid items type")
            return False

        # Recalculate order value from items
        calculated_value = 0.0
        for item in order["items"]:
            if not all(k in item for k in ("quantity", "price_per_unit")):
                print("Invalid item format")
                return False
            quantity = item["quantity"]
            price = item["price_per_unit"]
            if not isinstance(quantity, int) or not isinstance(price, (int, float)):
                print("Invalid quantity or price_per_unit type")
                return False
            calculated_value += quantity * price

        # Compare with provided order_value (with a tolerance for floating point precision)
        if abs(calculated_value - order["order_value"]) > 0.01:
            print(f"Order value mismatch: expected {calculated_value}, got {order['order_value']}")
            return False

        return True

    except Exception as e:
        print("Validation error:", e)
        return False


def update_user_stats(user_id, order_value):
    key = f"user:{user_id}"
    r.hincrby(key, "order_count", 1)
    r.hincrbyfloat(key, "total_spend", order_value)


def update_global_stats(order_value):
    key = "global:stats"
    r.hincrby(key, "total_orders", 1)
    r.hincrbyfloat(key, "total_revenue", order_value)

def update_leaderboards(user_id, order_value):
    r.zincrby("leaderboard:spend", order_value, user_id)    # Sorted set for top spenders
    r.zincrby("leaderboard:count", 1, user_id)    # Sorted set for most active users (by order count)


def process_message(message_body: str):
    try:
        order = json.loads(message_body)
        if not validate_order(order):
            print("Invalid order, skipping.")
            return

        # Extract essential fields
        user_id = order["user_id"]
        order_value = float(order["order_value"])
        order_timestamp = order.get("order_timestamp")  # Optional: log or future use

        update_user_stats(user_id, order_value)
        update_global_stats(order_value)
        update_leaderboards(user_id, order_value)

    except Exception as e:
        print("Failed to process order:", e)
