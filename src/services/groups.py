"""Group rules. Slice 1: the groups the signed-in user belongs to."""


def list_my_groups(store, user):
    return store.list_groups_for_user(user["id"])
