from datetime import date

import pytest

from query_maker import db
from query_maker.db import Operators


class SomeTable(db.Table):
    id = db.IntegerColumn(name='id')
    url = db.StringColumn(name='url', allowed_operators=[Operators.EQ.value])
    date = db.DateColumn(name='date')
    rating = db.IntegerColumn(name='rating')

    class Meta:
        table_name = 'some_table'


def test_generate_sql_query():
    query = SomeTable.generate_sql_query(SomeTable.id == 3)
    assert query == 'SELECT * FROM "some_table" WHERE id = 3;'

    query = SomeTable.generate_sql_query(SomeTable.id.eq(5))
    assert query == 'SELECT * FROM "some_table" WHERE id = 5;'

    query = SomeTable.generate_sql_query(SomeTable.id == 3, SomeTable.id == 5)
    assert query == 'SELECT * FROM "some_table" WHERE id = 3 AND id = 5;'

    query = SomeTable.generate_sql_query(SomeTable.id.in_([3]))
    assert query == 'SELECT * FROM "some_table" WHERE id IN (3);'

    query = SomeTable.generate_sql_query(SomeTable.id.not_in([3, 5]))
    assert query == 'SELECT * FROM "some_table" WHERE id NOT IN (3, 5);'

    query = SomeTable.generate_sql_query(SomeTable.id > 3, SomeTable.url == 'abc@abc.com')
    assert query == 'SELECT * FROM "some_table" WHERE id > 3 AND url = "abc@abc.com";'

    query = SomeTable.generate_sql_query(SomeTable.id < 3, SomeTable.id > 0)
    assert query == 'SELECT * FROM "some_table" WHERE id < 3 AND id > 0;'

    query = SomeTable.generate_sql_query(SomeTable.id > 0, SomeTable.id < 100, SomeTable.rating.gt(50))
    assert query == 'SELECT * FROM "some_table" WHERE id > 0 AND id < 100 AND rating > 50;'

    query = SomeTable.generate_sql_query(SomeTable.rating.gt(25))
    assert query == 'SELECT * FROM "some_table" WHERE rating > 25;'

    query = SomeTable.generate_sql_query(SomeTable.date > date(2016, 1, 1))
    assert query == 'SELECT * FROM "some_table" WHERE date > "2016-01-01";'


def test_generate_sql_query_limited_operators():
    with pytest.raises(db.NotAllowedOperatorError):
        query = SomeTable.generate_sql_query(SomeTable.url > 'test@test.com')
