
import random
def clamp_months(m): return max(1, min(12, int(m)))
def build_amount(price_per_month, months):
    months = clamp_months(months)
    subtotal = price_per_month * months
    uniq = random.randint(1, 999)
    return subtotal + uniq
def order_ref(user_id, months): return f"ORD-{user_id}-{months}m"
