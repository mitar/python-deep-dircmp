import os.path
import unittest
from pathlib import Path

from deep_dircmp import DeepDirCmp


class DeepDirCmpUnittest(unittest.TestCase):

    def test_get_left_only_recursive(self):
        deep_cmp = DeepDirCmp(Path("test/test_a"), Path("test/test_b"))
        file_in_a = deep_cmp.get_left_only_recursive()
        self.assertEqual(
            set(file_in_a),
            {
                "directory_in_a",
                "file_only_in_a.md",
                os.path.join('common_directory',
                             'deep_file_in_a_common_directory.md')

            }
        )

    def test_iter_left_only_recursive(self):
        deep_cmp = DeepDirCmp(Path("test/test_a"), Path("test/test_b"))
        self.assertEqual(
            deep_cmp.get_left_only_recursive(),
            list(deep_cmp.iter_left_only_recursive()),
        )

    def test_iter_right_only_recursive(self):
        deep_cmp = DeepDirCmp(Path("test/test_a"), Path("test/test_b"))
        self.assertEqual(
            deep_cmp.get_right_only_recursive(),
            list(deep_cmp.iter_right_only_recursive()),
        )

    def test_get_same_files_recursive(self):
        deep_cmp = DeepDirCmp(Path("test/test_a"), Path("test/test_b"))
        same_files = deep_cmp.get_same_files_recursive()
        self.assertEqual(
            set(same_files),
            {
                'file_both_in_a_b.md',
                os.path.join('common_directory', 'common_deep_file.md'),
            }
        )

    def test_iter_same_files_recursive(self):
        deep_cmp = DeepDirCmp(Path("test/test_a"), Path("test/test_b"))
        self.assertEqual(
            deep_cmp.get_same_files_recursive(),
            list(deep_cmp.get_same_files_recursive()),
        )


if __name__ == '__main__':
    unittest.main()
