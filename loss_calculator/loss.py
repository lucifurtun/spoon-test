class NotEnoughItemsError(Exception):
    pass


class NoLossError(Exception):
    pass


class NegativePriceError(Exception):
    pass


def get_largest_possible_loss(lst: list):
    try:
        largest = lst[1] - lst[0]
    except IndexError:
        raise NotEnoughItemsError()

    for index in range(len(lst) - 1):
        current_item = lst[index]
        next_item = lst[index + 1]

        if (current_item < 0) or (next_item < 0):
            raise NegativePriceError()

        loss = next_item - current_item

        if loss < largest:
            largest = loss

    if largest >= 0:
        raise NoLossError()

    return largest
