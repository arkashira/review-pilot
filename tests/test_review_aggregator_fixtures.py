import pytest
from src.review_aggregator import load_reviews_from_file, aggregate_reviews

@pytest.fixture
def reviews():
    return load_reviews_from_file('reviews.json')

def test_aggregate_reviews_with_fixtures(reviews):
    aggregated_reviews = aggregate_reviews(reviews)
    assert aggregated_reviews == {}  # No reviews.json file
