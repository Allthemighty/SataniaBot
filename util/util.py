import validators


def url_remove(reaction_list, keep_url=True):
    if keep_url:
        for idx, item in enumerate(reaction_list):
            if not validators.url(item[1]):
                reaction_list.pop(idx)
    else:
        for idx, item in enumerate(reaction_list):
            if validators.url(item[1]):
                reaction_list.pop(idx)
    return reaction_list