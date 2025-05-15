class Post:

    def __init__(self, post_id, uri, timestamp, text, username, repost):
        self.post_id = post_id
        self.uri = uri
        self.timestamp = timestamp
        self.text = text
        self.username = username
        self.repost = repost

    def __repr__(self):
        return (f'Post('
                f'post_id={self.post_id}, '
                f'uri={self.uri}, '
                f'timestamp={self.timestamp}, '
                f'text={self.text}, '
                f'username={self.username}, '
                f'repost={self.repost}')
