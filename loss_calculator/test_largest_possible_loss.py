from random import randint

import pytest

from loss_calculator.loss import get_largest_possible_loss, NotEnoughItemsError, NoLossError, NegativePriceError


def test_get_largest_possible_loss():
    prices = [1, 4, 6, 12, 2, 2, 9, 1]

    result = get_largest_possible_loss(prices)

    assert result == -10


def test_get_largest_possible_loss_many_items():
    prices = [1, 4, 6, 200, 2, 2, 9, 1] + [randint(0, 100) for v in range(100000)]

    result = get_largest_possible_loss(prices)

    assert result == -198


def test_get_largest_possible_loss_incorrect_negative_price():
    prices = [1, 4, 6, -12, 2, 2, 9, 1]

    with pytest.raises(NegativePriceError):
        result = get_largest_possible_loss(prices)


def test_get_largest_possible_loss_not_enough_prices():
    prices = [1]

    with pytest.raises(NotEnoughItemsError):
        result = get_largest_possible_loss(prices)


def test_get_largest_possible_loss_no_loss():
    prices = [1, 2, 3, 4, 5, 5, 6]

    with pytest.raises(NoLossError):
        result = get_largest_possible_loss(prices)
