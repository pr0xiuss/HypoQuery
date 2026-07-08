from __future__ import annotations

import re


class PredicateParser:
    """
    Extracts candidate column names from PostgreSQL predicate
    expressions.
    """

    _IDENTIFIER = re.compile(
        r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    )

    _STRING_LITERAL = re.compile(
        r"'(?:''|[^'])*'",
    )

    _TYPE_CAST = re.compile(
        r"::[a-zA-Z_][a-zA-Z0-9_]*",
    )

    _FUNCTION_CALL = re.compile(
        r"\b[a-zA-Z_][a-zA-Z0-9_]*\s*\(",
    )

    _KEYWORDS = {
        "and",
        "or",
        "not",
        "null",
        "true",
        "false",
        "like",
        "ilike",
        "similar",
        "is",
        "in",
        "between",
        "exists",
        "case",
        "when",
        "then",
        "else",
        "end",
        "as",
    }

    def extract_columns(
        self,
        predicate: str | None,
    ) -> list[str]:

        if not predicate:
            return []

        predicate = self._strip_string_literals(
            predicate,
        )

        predicate = self._strip_type_casts(
            predicate,
        )

        predicate = self._strip_function_names(
            predicate,
        )

        columns: list[str] = []

        for token in self._IDENTIFIER.findall(
            predicate,
        ):

            lower = token.lower()

            if lower in self._KEYWORDS:
                continue

            if token.isdigit():
                continue

            if token not in columns:
                columns.append(
                    token,
                )

        return columns

    def _strip_string_literals(
        self,
        predicate: str,
    ) -> str:

        return self._STRING_LITERAL.sub(
            "",
            predicate,
        )

    def _strip_type_casts(
        self,
        predicate: str,
    ) -> str:

        return self._TYPE_CAST.sub(
            "",
            predicate,
        )

    def _strip_function_names(
        self,
        predicate: str,
    ) -> str:

        return self._FUNCTION_CALL.sub(
            "(",
            predicate,
        )