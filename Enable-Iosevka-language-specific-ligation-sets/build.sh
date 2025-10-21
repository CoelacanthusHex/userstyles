#!/usr/bin/zsh

ruff format generate.py
ruff check \
    --show-fixes \
    generate.py
mypy \
    --disallow-untyped-defs \
    --check-untyped-defs \
    --disallow-incomplete-defs \
    --disallow-any-explicit \
    --no-implicit-optional \
    --strict-optional \
    --warn-return-any \
    --warn-redundant-casts \
    --strict-equality \
    --show-error-context \
    --show-column-numbers \
    --pretty \
    generate.py

./generate.py
