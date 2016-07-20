# SQLAlchemy stuff
from database_setup import Base, Comment, Commenter, Vote
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///comments.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def get_comments_in_region(lat_start, lon_start, lat_end, lon_end):
    comments = _get_comments_in_region(lat_start, lon_start, lat_end, lon_end)
    out = []
    for c in comments:
        out.append({'text': c.text, 'lat': c.lat, 'lon': c.lon})
    return out


def get_demographics_in_region(lat_start, lon_start, lat_end, lon_end):
    comments = _get_comments_in_region(lat_start, lon_start, lat_end, lon_end)
    commenters = [c.commenter for c in comments]
    return get_demographics(commenters)


def get_demographics_who_agree(agree=True):
    commenters = {}
    votes = session.query(Vote).filter(voter_id=0, sentiment=agree).all()
    commenters = [v.comment.commenter for v in votes]
    return get_demographics(commenters)


def _get_comments_in_region(lat_start, lon_start, lat_end, lon_end):
    comments = session.query(Comment).filter(
                    Comment.lat > lat_start,
                    Comment.lon > lon_start,
                    Comment.lat < lat_end,
                    Comment.lon < lon_end).all()
    return comments

def get_demographics(commenters):
    seen_ids = set()
    nationality_counter = {'Israeli': 0, 'Palestinian': 0}
    gender_counter = {'Male': 0, 'Female': 0}
    for c in commenters:
        if c.id in seen_ids:
            continue
        else:
            seen_ids.add(c.id)
        nationality_counter[c.nationality] += 1
        gender_counter[c.gender] += 1
    return {'nationality': nationality_counter, 'gender': gender_counter}

