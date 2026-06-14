from review_pilot import ReviewPilot, ReviewPlatform, Review

def test_ingest_review():
    pilot = ReviewPilot()
    pilot.ingest_review(ReviewPlatform.GOOGLE_PLAY, 5, "Great app!")
    assert len(pilot.get_reviews()) == 1

def test_save_reviews():
    pilot = ReviewPilot()
    pilot.ingest_review(ReviewPlatform.GOOGLE_PLAY, 5, "Great app!")
    pilot.save_reviews("reviews.json")
    with open("reviews.json", "r") as f:
        data = f.read()
        assert "Great app!" in data

def test_load_reviews():
    pilot = ReviewPilot()
    pilot.ingest_review(ReviewPlatform.GOOGLE_PLAY, 5, "Great app!")
    pilot.save_reviews("reviews.json")
    pilot = ReviewPilot()
    pilot.load_reviews("reviews.json")
    assert len(pilot.get_reviews()) == 1

def test_unified_schema():
    pilot = ReviewPilot()
    pilot.ingest_review(ReviewPlatform.GOOGLE_PLAY, 5, "Great app!")
    pilot.ingest_review(ReviewPlatform.APPLE_APP_STORE, 4, "Good app!")
    reviews = pilot.get_reviews()
    assert reviews[0].platform == ReviewPlatform.GOOGLE_PLAY
    assert reviews[1].platform == ReviewPlatform.APPLE_APP_STORE
