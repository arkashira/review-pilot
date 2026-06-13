from dataclasses import dataclass
from typing import List
import json

@dataclass
class Review:
    platform: str
    app_name: str
    rating: float
    text: str

def aggregate_reviews(reviews: List[Review]) -> dict:
    aggregated_reviews = {}
    for review in reviews:
        if review.platform not in aggregated_reviews:
            aggregated_reviews[review.platform] = []
        aggregated_reviews[review.platform].append({
            'app_name': review.app_name,
            'rating': review.rating,
            'text': review.text
        })
    return aggregated_reviews

def load_reviews_from_file(file_path: str) -> List[Review]:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            reviews = []
            for review in data:
                reviews.append(Review(
                    platform=review['platform'],
                    app_name=review['app_name'],
                    rating=review['rating'],
                    text=review['text']
                ))
            return reviews
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []
