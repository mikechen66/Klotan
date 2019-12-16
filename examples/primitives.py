from klotan import match, criteria

print(match.match(1, 1).to_string())
assert match.match(1, 1)

print(match.match(int, 1).to_string())
assert match.match(int, 1)

print(match.match({1: 1}, {1: 1}).to_string())
assert match.match({1: 1}, {1: 1})