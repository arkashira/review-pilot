import pytest
from src.review_aggregator import Review, aggregate_reviews, load_reviews_from_file

def test_aggregate_reviews():
    reviews = [
        Review('Google Play', 'App1', 4.5, 'Great app!'),
        Review('Google Play', 'App1', 4.5, 'Great app!'),
        Review('Apple App Store', 'App2', 4.0, 'Good app.')
    ]
    aggregated_reviews = aggregate_reviews(reviews)
    assert aggregated_reviews == {
        'Google Play': [
            {'app_name': 'App1', 'rating': 4.5, 'text': 'Great app!'},
            {'app_name': 'App1', 'rating': 4.5, 'text': 'Great app!'}
        ],
        'Apple App Store': [
            {'app_name': 'App2', 'rating': 4.0, 'text': 'Good app.'}
        ]
    }

def test_load_reviews_from_file():
    reviews = load_reviews_from_file('reviews.json')
    assert len(reviews) == 0  # No reviews.json file
