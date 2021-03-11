from tempfile import TemporaryDirectory
from distutils.dir_util import copy_tree
import shutil

import logging
import os
# from os.path import join
# from pathlib import Path

from mkdocs.utils import warning_filter

log = logging.getLogger(__name__)
log.addFilter(warning_filter)


class TfMerger:
    def __init__(self, config):
        self.config = config
        self.root_docs_dir = config['docs_dir']
        self.docs_dirs = list()
        self.files_source_dir = dict()

    def append(self, docs_path, abs_path):
        self.docs_dirs.append([docs_path, abs_path])

    def merge(self):
        self.temp_docs_dir = TemporaryDirectory('', 'docs_')
        # log.critical("temp_docs_dir = %s" % self.temp_docs_dir.name)
        # log.critical("root_docs_dir = %s" % self.root_docs_dir)

        # log.critical("ls root_docs_dir = %s" % list(Path(self.root_docs_dir).glob('**/*')))

        copy_tree(self.root_docs_dir, self.temp_docs_dir.name)

        # log.critical("ls temp_docs_dir = %s" % list(Path(self.temp_docs_dir.name).glob('**/*')))

        for docs_path, abs_path in self.docs_dirs:
            destination = os.path.join(
                self.temp_docs_dir.name, docs_path)
            destinationfolder = os.path.dirname(destination)
            if not os.path.exists(destinationfolder):
                os.makedirs(destinationfolder)
            shutil.copy(abs_path, destination)

        return str(self.temp_docs_dir.name)

    def getFilesSourceFolder(self):
        return self.files_source_dir

    def cleanup(self):
        return self.temp_docs_dir.cleanup()
