from review_pilot import Review, ReviewPilot

def test_add_review():
    review_pilot = ReviewPilot()
    review = Review(5, "Great product!")
    review_pilot.add_review(review)
    assert len(review_pilot.reviews) == 1

def test_aggregate_reviews():
    review_pilot = ReviewPilot()
    review_pilot.add_review(Review(5, "Great product!"))
    review_pilot.add_review(Review(4, "Good product!"))
    average_rating = review_pilot.aggregate_reviews()
    assert average_rating == 4.5

def test_save_and_load_reviews():
    review_pilot = ReviewPilot()
    review_pilot.add_review(Review(5, "Great product!"))
    review_pilot.save_reviews("reviews.json")
    review_pilot.reviews = []
    review_pilot.load_reviews("reviews.json")
    assert len(review_pilot.reviews) == 1
