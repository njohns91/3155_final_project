from src.models.models import Listing

class listing_repository:

    def get_all_listing(self):
        return Listing.query

    def specific_listing(self, listing_id):
        return Listing.query.get(listing_id)

    def get_user_listings(self, person_id):
        return Listing.query.filter_by(person_id=person_id)

listing_repository_singleton = listing_repository()