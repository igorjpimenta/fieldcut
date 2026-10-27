#!/usr/bin/env python3
"""Automated tests for fieldcut CLI (stdlib unittest, subprocess)."""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIELDCUT = str(REPO_ROOT / "fieldcut")


def run(args, input_text=None):
    """Run fieldcut, return CompletedProcess with text captured."""
    return subprocess.run(
        [sys.executable, FIELDCUT] + args,
        input=input_text,
        capture_output=True,
        text=True,
    )


class TestFieldcut(unittest.TestCase):
    def test_stdin_selection_1_3(self):
        p = run(["--fields", "1,3"], input_text="a b c\n")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout, "a\tc\n")

    def test_custom_delimiter(self):
        p = run(["--fields", "2", "--delimiter", ","], input_text="a b c\n")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout, "b\n")

    def test_default_delimiter_is_tab(self):
        p = run(["--fields", "1,2"], input_text="a b c\n")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("\t", p.stdout)
        self.assertEqual(p.stdout, "a\tb\n")

    def test_file_argument_input(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("x y\np q r\n")
            path = f.name
        try:
            p = run(["--fields", "1,3", path])
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(p.stdout, "x\t\np\tr\n")
        finally:
            os.unlink(path)

    def test_multiple_files_concatenated_in_order(self):
        paths = []
        try:
            for content in ("m n o\n", "p q r\n"):
                tf = tempfile.NamedTemporaryFile(
                    mode="w", suffix=".txt", delete=False, encoding="utf-8"
                )
                tf.write(content)
                tf.close()
                paths.append(tf.name)
            p = run(["--fields", "1,2"] + paths)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(p.stdout, "m\tn\np\tq\n")
        finally:
            for path in paths:
                os.unlink(path)

    def test_invalid_field_zero_exits_2(self):
        p = run(["--fields", "0"], input_text="a b c\n")
        self.assertEqual(p.returncode, 2)
        self.assertIn("invalid", p.stderr.lower())

    def test_invalid_field_negative_exits_2(self):
        p = run(["--fields", "-1"], input_text="a b c\n")
        self.assertEqual(p.returncode, 2)
        self.assertIn("invalid", p.stderr.lower())

    def test_invalid_field_abc_exits_2(self):
        p = run(["--fields", "abc"], input_text="a b c\n")
        self.assertEqual(p.returncode, 2)
        self.assertIn("invalid", p.stderr.lower())

    def test_out_of_range_yields_empty_slot(self):
        p = run(["--fields", "1,3"], input_text="x y\n")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout, "x\t\n")

    def test_empty_lines_ignored(self):
        p = run(["--fields", "1"], input_text="a b\n\n   \nc d\n")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout, "a\nc\n")

    def test_help_exits_0(self):
        p = run(["--help"])
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("Usage", p.stdout)

    def test_missing_fields_exits_2(self):
        p = run([], input_text="a b c\n")
        self.assertEqual(p.returncode, 2)
        self.assertIn("--fields", p.stderr)


if __name__ == "__main__":
    unittest.main()
