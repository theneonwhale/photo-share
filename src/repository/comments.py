from datetime import date, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from src.database.models import Comment, Image, User
from src.schemas import ImageModel, CommentModel
from src.conf.messages import *
from src.repository import tags as repository_tags
# Leave a comment...
async def add_comment(
        body: CommentModel,
        image_id: int,  # !
        user: dict,
        db: Session
        ) -> Optional[Comment]:

        comment = Comment(comment=body.comment,
                          user_id=user['id'],
                          image_id=image_id)  # user_id=user.get('id'), image_id=image_id =already in body (CommentModel)
        db.add(comment)
        db.commit()
        db.refresh(comment)

        return comment


# EDIT comment
async def update_comment(
        comment_id: int,
        body: CommentModel,
        user: dict,  # !
        db: Session,
) -> Optional[Image]:
    comment: Comment = db.query(Comment).filter_by(id=comment_id, user_id=user['id']).first()
    if not comment or not body.comment:
        return None

    comment.comment = body.comment
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


async def remove_comment(
        comment_id: int,
        user: User,  # !
        db: Session
) -> Optional[Image]:
    comment: Comment = db.query(Comment).filter_by(id=comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
        # db.refresh(comment)

    return comment
