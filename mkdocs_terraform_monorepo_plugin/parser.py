import logging
import os
import copy
from pathlib import Path

from mkdocs.utils import warning_filter

log = logging.getLogger(__name__)
log.addFilter(warning_filter)

INCLUDE_STATEMENT = "!tf_modules_root "
# TODO should make these config variables in mkdocs.yml
DOCUMENT_FILE_NAME = 'README.md'
NAVIGATION_KEY_NAME = 'About'


class TfParser:
    def __init__(self, config):
        self.initialNav = config['nav']
        self.config = config
        self.resolvedPaths = []

    def getResolvedPaths(self):
        return self.resolvedPaths

    def resolve(self, nav=None):  # noqa: C901
        if nav is None:
            nav = copy.deepcopy(self.initialNav)
        # log.critical("nav: {} ".format(nav))
        for index, item in enumerate(nav):
            if type(item) is str:
                key = None
                value = item
                # log.critical("value1 = {}".format(value))
            elif type(item) is dict:
                key = list(item.keys())[0]
                value = list(item.values())[0]
                # log.critical("value2 = {}".format(value))
            else:
                key = None
                value = None
            if type(value) is str and INCLUDE_STATEMENT in value:
                # log.critical("value3 = {}".format(value))
                nav[index] = {}
                alias = value.split(INCLUDE_STATEMENT)[0]
                if alias is INCLUDE_STATEMENT:
                    alias == ""
                else:
                    alias = alias.rstrip('/')
                modPath = value.split(INCLUDE_STATEMENT)[-1]
                modNav = CreateModulesNav(
                    self.config,
                    alias,
                    modPath
                ).build()
                # log.critical("modNav = {}".format(modNav.getNav()))
                # log.critical("key = {}".format(key))
                nav[index][key] = modNav.getNav()
                if nav[index][key] is None:
                    del nav[index][key]
                    continue
                else:
                    self.resolvedPaths = [*self.resolvedPaths, *modNav.getResolvedPaths()]
            elif type(value) is list:
                # log.critical("value4 = {}".format(value))
                nav[index] = {}
                nav[index][key] = self.resolve(value)
                if nav[index][key] is None:
                    del nav[index][key]
                    continue
        for index, item in enumerate(nav):
            if nav[index] == {}:
                del nav[index]
        return nav


class CreateModulesNav:
    def __init__(self, config, alias, modulePath):
        # log.critical("config = {}".format(config))
        # log.critical("alias = {}".format(alias))
        # log.critical("modulePath = {}".format(modulePath))
        # log.critical("cwd = {}".format(os.getcwd()))
        # log.critical("config[config_file_path] = {}".format(config['config_file_path']))
        self.rootDir = os.path.normpath(os.path.join(
            os.getcwd(), os.path.dirname(config['config_file_path']), modulePath, '../'))
        # log.critical("rootDir = {}".format(self.rootDir))
        self.alias = alias
        self.modulePath = modulePath
        p = Path(self.modulePath)
        basePath = modulePath
        if len(p.parts) > 1:  # this is if we are in a nested mkdocs for monorepo etc
            basePath = p.relative_to(*p.parts[:1])
        # log.critical("basePath = {}".format(basePath))
        self.absModulePath = os.path.normpath(
            os.path.join(self.rootDir, basePath))
        # log.critical("absModulePath = {}".format(self.absModulePath))
        self.moduleNav = None
        self.resolvedPaths = None

    def getAbsModulePath(self):
        return self.absModulePath

    def build(self):
        if not os.path.exists(self.absModulePath):
            log.critical(
                "[mkdocs-terraform-monorepo] The path {} is not valid. ".format(self.absModulePath) +
                "Please update your 'nav' with a valid path (relative to the mkdocs.yml file).")
            raise SystemExit(1)

        allPaths = []
        for path in Path(self.absModulePath+'/').rglob(DOCUMENT_FILE_NAME):
            allPaths.append(str(path.relative_to(Path(self.absModulePath).parent)))
        # log.critical("allPaths = {}".format(allPaths))
        # TODO need to check full path is not in an ignore list

        allPaths = sorted(allPaths)
        for file in allPaths:
            if self.moduleNav is None:
                self.moduleNav = {}
            self.moduleNav = self.__build_nested(
                os.path.join(self.alias, file), self.moduleNav)
            if self.resolvedPaths is None:
                self.resolvedPaths = []
            self.resolvedPaths.append(
                [os.path.join(self.alias, file), os.path.join(self.rootDir, file)])
        # log.critical("moduleNav = {}".format(self.moduleNav))
        # log.critical("resolvedPaths = {}".format(self.resolvedPaths))
        return self

    def __build_nested_helper(self, path, file, container):
        segs = Path(path).parts
        head, tail = segs[0], segs[1:]
        if len(tail) == 1 or not tail:
            if head == DOCUMENT_FILE_NAME:
                head = NAVIGATION_KEY_NAME
            container[head] = file
            # container = [file]
        else:
            if head not in container:
                container[head] = self.__build_nested_helper(os.path.join(*tail), file, {})
            else:
                if type(container[head]) is str:
                    container[head] = {NAVIGATION_KEY_NAME: container[head]}
                    # container = [container[head]]
                    # send it round again, avoiding the file loop
                container[head] = self.__build_nested_helper(os.path.join(*tail), file, container[head])
        return container

    def __build_nested(self, file, container):
        return self.__build_nested_helper(os.path.join(*(Path(file).parts[1:])), file, container)

    def getNav(self):
        return self.moduleNav

    def getResolvedPaths(self):
        return self.resolvedPaths
