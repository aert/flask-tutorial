from hashlib import md5
import re
from ..extensions import db
from microblog.models import Post


ROLE_USER = 0
ROLE_ADMIN = 1


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(180))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%s' % (
            md5(self.email).hexdigest(),
            str(size))

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id) \
                   .count() > 0

    def followed_posts(self):
        return Post.query.join(followers,
                               (followers.c.followed_id == Post.user_id)) \
                         .filter(followers.c.follower_id == self.id) \
                         .order_by(Post.timestamp.desc())

    @staticmethod
    def check_nickname_exists(nickname):
        return User.query.filter_by(nickname=nickname).first() is not None

    @staticmethod
    def make_unique_nickname(nickname):
        if not User.check_nickname_exists(nickname):
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if not User.check_nickname_exists(new_nickname):
                break
            version += 1
        return new_nickname

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-9_\.]', '', nickname)

    def __repr__(self):
        return "<User %r>" % self.nickname
