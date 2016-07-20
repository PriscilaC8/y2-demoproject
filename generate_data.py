import random
import sys
import string
import numpy as np

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Commenter, Comment, Vote

MEAN = [31.779457, 35.22052]

def mixture_sample(side):
    if np.random.random() > .5:
        return side_sample(MEAN, side)
    else:
        return np.random.multivariate_normal(MEAN, .008*np.eye(2))

def side_sample(mean, side=None):
    assert side in [-1, 1]
    # Rejection sampling to get only things east (-1) or west (+1) of mean
    while True:
        data = np.random.multivariate_normal(
                    mean,
                    .008*np.eye(2))
        if (data[1] - mean[1]) * side > 0:
            break
    return data

def generate_random_name(nat):
    length = random.randint(4, 8)
    return ''.join([random.choice(string.ascii_lowercase) for i in xrange(length)])

nationalities = ['Israeli', 'Palestinian', 'American', 'French', 'British',
        'Turkish', 'Greek', 'Egyptian', 'Brazilian', 'German']

foods = ['hummus', 'falafel', 'shawarma', 'mansaf', 'shakshuka', 'labneh',
        'pizza', 'burgers', 'kebab', 'pasta', 'sushi', 'schnitzel', 'tacos',
         'escargot', 'sabich', 'mjaddara', 'quinoa', 'twinkies', 'ice cream',
         'natto', 'salad', 'ramen', 'pho', 'udon', 'sandwich', 'mango', 'broccoli',
         'lychee', 'okra', 'watermelon', 'mashed potatoes', 'eggs', 'pancakes',]

def generate_all_comments():
    comments = []
    for nat in nationalities:
        comments.append('I met a nice {} today!'.format(nat))
        comments.append('I hate {}s'.format(nat))
        comments.append('I wish I knew more {}s'.format(nat))
    for food in foods:
        comments.append('I love eating {}'.format(food))
        comments.append('Just had some delicious {}'.format(food))
        comments.append('I want to learn how to make {}'.format(food))
        for i in xrange(25):
            comments.append('I think {} is the best food ever'.format(food))
            comments.append('{} is so good!'.format(food))
            comments.append("I don't like {} very much...".format(food))
        for i in xrange(5):
            comments.append('{} is not that good'.format(food))
        for nat in nationalities:
            comments.append('Do {} people like {}?'.format(nat, food))
            comments.append('Enjoying some {} with my {} friend'.format(food, nat))
            comments.append('Enjoying some {} with my {} friend'.format(food, nat))
            comments.append('Enjoying some {} with my {} friend'.format(food, nat))
    return comments

ALL_COMMENTS = generate_all_comments()

def generate_commenter():
    nat = random.choice(['Palestinian', 'Israeli'])
    gender = random.choice(['Female', 'Male'])
    name = generate_random_name(nat)
    return Commenter(nationality=nat, name=name, gender=gender)

def generate_comments(commenter, N):
    comments = []
    for i in xrange(N):
        if commenter.nationality == 'Palestinian':
            location = mixture_sample(1)
        elif commenter.nationality == 'Israeli':
            location = mixture_sample(-1)
        else:
            raise ValueError
        text = random.choice(ALL_COMMENTS)
        comments.append(Comment(lat=location[0], lon=location[1], text=text, commenter=commenter))
    return comments

def generate_votes(comments, commenters, N):
    votes = []
    for i in xrange(N):
        comment = random.choice(comments)
        voter = random.choice(commenters)
        if comment.commenter.id == voter.id:
            continue
        if comment.commenter.nationality == voter.nationality:
            threshold = .8
        else:
            threshold = .2

        sentiment = random.random() < threshold
        votes.append(Vote(comment=comment, voter=voter, sentiment=sentiment))
    return votes

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print "Usage: generate_data.py <n_commenters> <n_comments_per_commenter> <n_votes>"
        sys.exit(1)
    engine = create_engine('sqlite:///comments.db')
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    n_commenters, n_comments_per_commenter, n_votes = map(int, sys.argv[1:4])

    comments = []
    commenters = []
    for i in xrange(n_commenters):
        commenter = generate_commenter()
        commenters.append(commenter)
        comments.extend(generate_comments(commenter, n_comments_per_commenter))
    for c in commenters + comments:
        session.add(c)
    session.commit()
    votes = generate_votes(comments, commenters, n_votes)
    for v in votes:
        session.add(v)
    session.commit()

