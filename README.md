# fieldcut

Print selected whitespace-separated fields from stdin or file arguments.

## Usage

```
fieldcut --fields 1,3 [--delimiter DELIM] [FILE ...]
```

- Reads lines from stdin when no file args are given, otherwise concatenates each file arg in order.
- Splits each line on whitespace; empty lines are ignored.
- `--fields` is **required**: comma-separated 1-based integers (e.g. `1,3`), order preserved.
- `--delimiter` sets the output separator (default: TAB).
- Missing fields on a line produce an empty string for that position.
- Invalid `--fields` values print a message to stderr and exit 2.
- `--help` prints usage and exits 0.

## Examples

```sh
echo 'a b c' | ./fieldcut --fields 1,3
# a	c

echo 'a b c' | ./fieldcut --fields 2 --delimiter ,
# b

./fieldcut --fields 1,3 data.txt
```

## License

MIT
