import filecmp
import os.path

__version__ = '0.1.0'


class DeepDirCmp(filecmp.dircmp):
    """
    A version of dircmp which does not compare files shallow, and has recursive getters.
    """

    def phase3(self):
        xx = filecmp.cmpfiles(self.left, self.right, self.common_files, shallow=False)
        self.same_files, self.diff_files, self.funny_files = xx

    # TODO: Remove once this is merged, released, and we move to it: https://github.com/python/cpython/pull/5088
    def phase4(self):
        self.subdirs = {}
        for x in self.common_dirs:
            a_x = os.path.join(self.left, x)
            b_x = os.path.join(self.right, x)
            self.subdirs[x] = type(self)(a_x, b_x, self.ignore, self.hide)

    def get_left_only_recursive(self):
        left_only = list(self.left_only)
        for name, subdir in self.subdirs.items():
            for file in subdir.get_left_only_recursive():
                left_only.append(os.path.join(name, file))
        return left_only

    def get_right_only_recursive(self):
        right_only = list(self.right_only)
        for name, subdir in self.subdirs.items():
            for file in subdir.get_right_only_recursive():
                right_only.append(os.path.join(name, file))
        return right_only

    def get_common_funny_recursive(self):
        common_funny = list(self.common_funny)
        for name, subdir in self.subdirs.items():
            for file in subdir.get_common_funny_recursive():
                common_funny.append(os.path.join(name, file))
        return common_funny

    def get_diff_files_recursive(self):
        diff_files = list(self.diff_files)
        for name, subdir in self.subdirs.items():
            for file in subdir.get_diff_files_recursive():
                diff_files.append(os.path.join(name, file))
        return diff_files

    # For our subclassed methods to be really used.
    methodmap = dict(filecmp.dircmp.methodmap,
        subdirs=phase4,
        same_files=phase3, diff_files=phase3, funny_files=phase3,
    )
