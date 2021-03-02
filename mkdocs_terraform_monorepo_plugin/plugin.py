from mkdocs.plugins import BasePlugin
from .parser import TfParser
from .merger import TfMerger
from collections import OrderedDict
# from pathlib import Path

import logging

from mkdocs.utils import warning_filter

log = logging.getLogger(__name__)
log.addFilter(warning_filter)

known_nav_special_syntax_plugins = ["monorepo"]


class TerraformMonorepoPlugin(BasePlugin):
    def __init__(self):
        self.parser = None
        self.merger = None
        self.originalDocsDir = None
        self.resolvedPaths = []
        self.files_source_dir = {}

    # need to add config for file readme and ignore regex list
    # would be good to add a check for terrafrom-docs html comment and remove it
    # before render event so we can use the page title in the nav

    def on_config(self, config):
        # If no 'nav' defined, we don't need to run.
        if not config.get('nav'):
            return config

        # terraform-monorepo has to be before monorepo in the plugins list
        # taken from https://github.com/timvink/mkdocs-enumerate-headings-plugin/blob/ef8b0931890b12455b53ccd52f41fcb3104eb89c/mkdocs_enumerate_headings_plugin/plugin.py#L46  # noqa: E501
        plugins = [*OrderedDict(config["plugins"])]

        for p in known_nav_special_syntax_plugins:
            if p in plugins:
                if plugins.index("terraform-monorepo") < plugins.index(p):
                    log.critical(
                        "[mkdocs-terraform-monorepo] terraform-monorepo should be defined after the %s plugin in your mkdocs.yml file"   # noqa: E501
                        % p
                    )
                    raise SystemExit(1)

        # Handle !tf_modules_root statements
        self.parser = TfParser(config)
        resolvedNav = self.parser.resolve()
        resolvedPaths = self.parser.getResolvedPaths()
        config['nav'] = resolvedNav

        # Generate a new "docs" directory
        self.merger = TfMerger(config)
        for docsPath, absPath in resolvedPaths:
            self.merger.append(docsPath, absPath)
        new_docs_dir = self.merger.merge()

        # Update the docs_dir with our temporary one!
        self.originalDocsDir = config['docs_dir']
        config['docs_dir'] = new_docs_dir

        # Store resolved paths for later.
        self.resolvedPaths = resolvedPaths

        # Store source directory of copied files for later
        self.files_source_dir = self.merger.getFilesSourceFolder()
        return config

    def on_pre_page(self, page, config, files):
        # Update page source attribute to point to source file
        # Only in case any files were moved.
        if len(self.files_source_dir) > 0:
            if page.file.abs_src_path in self.files_source_dir:
                page.file.abs_src_path = self.files_source_dir[page.file.abs_src_path]
        return page

    def on_serve(self, server, config, **kwargs):
        buildfunc = list(server.watcher._tasks.values())[0]['func']

        # still watch the original docs/ directory
        if self.originalDocsDir is not None:
            server.watch(self.originalDocsDir, buildfunc)

        # watch all the sub docs/ folders
        for watch_file, _ in self.resolvedPaths:
            server.watch(watch_file, buildfunc)

    def post_build(self, config):
        self.merger.cleanup()
