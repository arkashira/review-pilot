# src/review_processor.py

def process_review(review):
    """
    Processes a user review, prioritizes it, and generates an action plan.
    Returns a structured dict on success, or a descriptive error string on failure.
    """
    try:
        if not review.get('text') or not review.get('product_id'):
            return "Unable to process review: missing required fields (text or product_id)"

        if not is_valid_product_id(review['product_id']):
            return f"Unable to process review: invalid product ID '{review['product_id']}'"

        category    = categorize_review(review['text'])
        priority    = calculate_priority(category, review.get('rating', 'low'))
        action_plan = generate_action_plan(category, priority)

        return {
            "status": "success",
            "category": category,
            "priority": priority,
            "action_plan": action_plan,
        }

    except Exception as exc:
        log_error(f"Error processing review: {exc}")
        return "Unable to process review: unexpected error occurred"


def is_valid_product_id(product_id):
    """Returns True if the product ID is known to the portfolio."""
    return product_id in {"prod-123", "prod-456"}


def categorize_review(text):
    lowered = text.lower()
    if "bug" in lowered:
        return "bug"
    if "feature" in lowered:
        return "feature request"
    return "general feedback"


def calculate_priority(category, rating):
    priority_map = {
        "bug":              {"low": 1, "medium": 2, "high": 3},
        "feature request":  {"low": 1, "medium": 2, "high": 3},
        "general feedback": {"low": 1, "medium": 2, "high": 3},
    }
    return priority_map.get(category, {}).get(rating.lower(), 1)


def generate_action_plan(category, priority):
    """Returns a human-readable action plan string."""
    urgency = {3: "immediately", 2: "this sprint", 1: "in the backlog"}.get(priority, "in the backlog")
    return f"Address {category} {urgency}."