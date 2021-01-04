from mkdocs.plugins import BasePlugin
from .parser import Parser
from .merger import Merger

import logging

from mkdocs.utils import warning_filter

log = logging.getLogger(__name__)
log.addFilter(warning_filter)


class TerraformMonorepoPlugin(BasePlugin):
    def __init__(self):
        self.parser = None
        self.merger = None
        self.originalDocsDir = None
        self.resolvedPaths = []

    # need to add config for file readme and ignore regex list
    # would be good to add a check for terrafrom-docs html comment and remove it before render event so we can use the page title in the nav

    def on_config(self, config):
        # If no 'nav' defined, we don't need to run.
        if not config.get('nav'):
            return config

        # Handle !tf_docroot statements
        self.parser = Parser(config)
        resolvedNav = self.parser.resolve()
        resolvedPaths = self.parser.getResolvedPaths()

        log.info("plugin.on_config resolvedPaths = {}".format(resolvedPaths))

        config['nav'] = resolvedNav

        # Generate a new "docs" directory
        self.merger = Merger(config)
        for docsPath, absPath in resolvedPaths:
            self.merger.append(docsPath, absPath)
        new_docs_dir = self.merger.merge()

        # Update the docs_dir with our temporary one!
        self.originalDocsDir = config['docs_dir']
        config['docs_dir'] = new_docs_dir

        # Store resolved paths for later.
        self.resolvedPaths = resolvedPaths

        return config

    def on_serve(self, server, config, **kwargs):
        buildfunc = list(server.watcher._tasks.values())[0]['func']

        # still watch the original docs/ directory
        server.watch(self.originalDocsDir, buildfunc)

        # watch all the sub docs/ folders
        for watch_file, _ in self.resolvedPaths:
            server.watch(watch_file, buildfunc)

    def post_build(self, config):
        self.merger.cleanup()
