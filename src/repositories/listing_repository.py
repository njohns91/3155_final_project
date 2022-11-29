from src.models.models import SQLAlchemy
from src.models.models import db, Listing

class listing_repository:

    def get_all_listing(self):
        return Listing.query.all()

    def specific_listing(self, listing_id):
        return Listing.query.get(listing_id)


listing_repository_singleton = listing_repository()