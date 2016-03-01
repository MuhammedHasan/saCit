def if_not_list_make_list(any_thing):
    if type(any_thing) != list:
        return [any_thing]
    return any_thing
