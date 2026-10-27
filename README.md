# fieldcut

Print selected whitespace-separated fields from stdin or file arguments.

## Install

Requires Python 3. No third-party dependencies.

```sh
git clone https://github.com/igorjpimenta/fieldcut.git
cd fieldcut
chmod +x fieldcut
```

Run it directly as `./fieldcut`, or copy/symlink it into your `PATH`.

## Usage

```
fieldcut --fields 1,3 [--delimiter DELIM] [FILE ...]
```

- Reads lines from stdin when no file args are given, otherwise reads each file arg in order.
- Splits each line on whitespace; empty lines are ignored.
- Missing fields on a line produce an empty string for that position.
- Order of the selected fields is preserved (e.g. `--fields 3,1` outputs field 3 first).

## Options

| Option | Description |
| --- | --- |
| `--fields FIELDS` | Comma-separated 1-based field numbers (required, e.g. `1,3`) |
| `--delimiter DELIM` | Output separator (default: TAB) |
| `--help` | Print usage and exit 0 |

## Examples

Pipe from stdin:

```sh
$ echo 'a b c d' | ./fieldcut --fields 1,3
a	c
```

Read from a file:

```sh
$ printf 'alpha beta\ngamma delta\n' > data.txt
$ ./fieldcut --fields 2 data.txt
beta
delta
```

Custom delimiter:

```sh
$ echo 'a b c d' | ./fieldcut --fields 1,3 --delimiter ', '
a, c
```

Invalid input exits 2 with a message on stderr:

```sh
$ echo 'x y' | ./fieldcut --fields 0
fieldcut: invalid --fields value: '0': must be >= 1
$ echo $?
2
```

## Tests

```sh
python3 -m unittest discover tests
```

All 12 tests should pass. `tests/smoke.sh` runs an end-to-end smoke check.

## License

MIT
