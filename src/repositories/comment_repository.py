from src.models.models import Comment

class comment_repository:

    def get_listing_comments(self, listing_id):
        return Comment.query.filter_by(listing_id=listing_id)

    def get_user_comments(self, person_id):
        return Comment.query.filter_by(person_id=person_id)
    
    def get_single_comment(self, comment_id):
        return Comment.query.filter_by(comment_id = comment_id).first()

comment_repository_singleton = comment_repository()