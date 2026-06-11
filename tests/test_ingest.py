from src.ingest import parse_reviews

def test_parse_reviews_structure():
    reviews = parse_reviews(apple_id="123", package_name="com.example")
    assert isinstance(reviews, list)
    assert all(isinstance(r, dict) for r in reviews)
    assert "id" in reviews[0]