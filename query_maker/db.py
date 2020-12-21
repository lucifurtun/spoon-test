import abc
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Any


class NotAllowedOperatorError(Exception):
    pass


class Operators(Enum):
    EQ = '='
    GT = '>'
    LT = '<'
    IN = 'IN'
    NOT_IN = 'NOT IN'

    @classmethod
    def get_all(cls) -> list:
        return [item.value for item in cls]


LIST_OPERATORS = (Operators.IN.value, Operators.NOT_IN.value)


@dataclass
class Filter:
    column: 'Column'
    value: Any
    operator: str

    def get_value(self) -> str:
        value = self.value

        return f'{self.column.name} {self.operator} {value}'


class ListFilter(Filter):
    def get_value(self) -> str:
        value = ', '.join([str(v) for v in self.value])
        value = f'({value})'

        return f'{self.column.name} {self.operator} {value}'


class Column(abc.ABC):
    name: str

    def __init__(self, name: str, allowed_operators: list = None) -> None:
        super().__init__()
        self.name = name

        if allowed_operators is None:
            self.allowed_operators = Operators.get_all()
        else:
            self.allowed_operators = allowed_operators

    def to_sql(self, value):
        if isinstance(value, list):
            return [self.py_value_to_sql_value(item) for item in value]

        return self.py_value_to_sql_value(value)

    @abc.abstractmethod
    def py_value_to_sql_value(self, value):
        pass

    def eq(self, value) -> Filter:
        return self._get_filter(value=value, operator=Operators.EQ.value)

    def gt(self, value) -> Filter:
        return self._get_filter(value=value, operator=Operators.GT.value)

    def lt(self, value) -> Filter:
        return self._get_filter(value=value, operator=Operators.LT.value)

    def in_(self, value) -> Filter:
        return self._get_filter(value=value, operator=Operators.IN.value)

    def not_in(self, value) -> Filter:
        return self._get_filter(value=value, operator=Operators.NOT_IN.value)

    def __eq__(self, value):
        return self.eq(value)

    def __gt__(self, value):
        return self.gt(value)

    def __lt__(self, value):
        return self.lt(value)

    def _get_filter(self, value, operator) -> Filter:
        if operator not in self.allowed_operators:
            raise NotAllowedOperatorError()

        if operator in LIST_OPERATORS:
            return ListFilter(
                column=self,
                value=self.to_sql(value),
                operator=operator
            )

        return Filter(
            column=self,
            value=self.to_sql(value),
            operator=operator
        )


class IntegerColumn(Column):
    def py_value_to_sql_value(self, value: int):
        return int(value)


class StringColumn(Column):
    def py_value_to_sql_value(self, value: str):
        return f'"{value}"'


class DateColumn(Column):
    def py_value_to_sql_value(self, value: date):
        return f'"{value.isoformat()}"'


class Table:
    @classmethod
    def generate_sql_query(cls, *filters) -> str:
        final_query = cls._compose_sql_query(*filters)
        final_query += ';'

        return final_query

    @classmethod
    def _compose_sql_query(cls, *filters) -> str:
        table_name = cls.Meta.table_name if hasattr(cls, 'Meta') else cls.__name__

        # Assume that we always select *.
        query = f'SELECT * FROM "{table_name}"'

        if not filters:
            return query

        # Assume that we only use AND operator.
        where_expression = ' AND '.join([f.get_value() for f in filters])

        query += ' WHERE ' + where_expression

        return query
