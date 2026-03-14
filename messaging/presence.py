online_users = set()


def add_user(user_id):
    online_users.add(user_id)


def remove_user(user_id):
    online_users.discard(user_id)


def is_user_online(user_id):
    return user_id in online_users