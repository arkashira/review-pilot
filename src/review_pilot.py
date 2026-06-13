import json
from dataclasses import dataclass
from typing import List

@dataclass
class Review:
    rating: int
    comment: str

class ReviewPilot:
    def __init__(self):
        self.reviews = []

    def add_review(self, review: Review):
        self.reviews.append(review)

    def aggregate_reviews(self):
        total_rating = sum(review.rating for review in self.reviews)
        average_rating = total_rating / len(self.reviews) if self.reviews else 0
        return average_rating

    def save_reviews(self, filename: str):
        reviews_data = [{"rating": review.rating, "comment": review.comment} for review in self.reviews]
        with open(filename, "w") as file:
            json.dump(reviews_data, file)

    def load_reviews(self, filename: str):
        try:
            with open(filename, "r") as file:
                reviews_data = json.load(file)
                self.reviews = [Review(review["rating"], review["comment"]) for review in reviews_data]
        except FileNotFoundError:
            pass
