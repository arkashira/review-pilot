import json
from dataclasses import dataclass
from enum import Enum
from typing import List

class ReviewPlatform(Enum):
    GOOGLE_PLAY = "Google Play"
    APPLE_APP_STORE = "Apple App Store"
    G2 = "G2"
    CAPTERRA = "Capterra"

@dataclass
class Review:
    platform: ReviewPlatform
    rating: int
    text: str

class ReviewPilot:
    def __init__(self):
        self.reviews = []

    def ingest_review(self, platform: ReviewPlatform, rating: int, text: str):
        review = Review(platform, rating, text)
        self.reviews.append(review)

    def get_reviews(self):
        return self.reviews

    def save_reviews(self, filename: str):
        data = []
        for review in self.reviews:
            data.append({
                "platform": review.platform.value,
                "rating": review.rating,
                "text": review.text
            })
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_reviews(self, filename: str):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for review_data in data:
                    platform = ReviewPlatform(review_data["platform"])
                    rating = review_data["rating"]
                    text = review_data["text"]
                    self.ingest_review(platform, rating, text)
        except FileNotFoundError:
            pass
