import logging
import os
import copy
import re

from mkdocs.utils import yaml_load, warning_filter

log = logging.getLogger(__name__)
log.addFilter(warning_filter)

INCLUDE_STATEMENT = "!tf_modules_root "


class Parser:
    def __init__(self, config):
        self.initialNav = config['nav']
        self.config = config
        self.resolvedPaths = []

    def getResolvedPaths(self):
        return self.resolvedPaths

    def resolve(self, nav=None):
        if nav is None:
            nav = copy.deepcopy(self.initialNav)

        for index, item in enumerate(nav):
            if type(item) is str:
                key = None
                value = item
            elif type(item) is dict:
                key = list(item.keys())[0]
                value = list(item.values())[0]
            else:
                key = None
                value = None

            if type(value) is str and value.startswith(INCLUDE_STATEMENT):
                nav[index] = {}
                modNav = CreateModulesNav(
                    self.config,
                    value[len(INCLUDE_STATEMENT):]
                ).build()

                nav[index][key] = modNav.getNav()

                if nav[index][key] is None:
                    del nav[index][key]
                    continue
                else:
                    self.resolvedPaths = [*self.resolvedPaths, *modNav.getResolvedPaths()]

            elif type(value) is list:
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
    def __init__(self, config, modulePath):
        self.docsDir = os.path.normpath(os.path.join(
            os.getcwd(), config['docs_dir']))
        self.rootDir = os.path.normpath(os.path.join(
            os.getcwd(), config['config_file_path'], '../'))
        self.modulePath = modulePath
        self.absModulePath = os.path.normpath(
            os.path.join(self.docsDir, self.modulePath))
        self.moduleNav = None
        self.resolvedPaths = None

    def getAbsModulePath(self):
        return self.absModulePath

    def build(self):
        if not self.absModulePath.startswith(self.rootDir):
            log.critical(
                "[mkdocs-terraform-monorepo] The modules directory {} is outside of the current directory {}. ".format(self.absModulePath, self.rootDir) +
                "Please move it and try again."
            )
            raise SystemExit(1)

        for root, dirs, files in os.walk(self.absModulePath):
            for dir in dirs:
                for file in os.listdir(os.path.join(root, dir)):
                    # need to check for other *.tf files in the dir
                    # should make this a variable
                    if file.endswith("README.md"):
                        # need to check full path is not in an ignore list
                        fileKey = os.path.join(root, dir).replace(
                            self.absModulePath+'/', '')
                        docsDirPath = os.path.join(
                            root, dir, file).replace(self.rootDir+'/', '')
                        if self.moduleNav is None:
                          self.moduleNav = {}
                        self.moduleNav = self.__build_nested(
                            fileKey, docsDirPath, self.moduleNav)
                        if self.resolvedPaths is None:
                            self.resolvedPaths = []
                        self.resolvedPaths.append(
                            [docsDirPath, os.path.join(root, dir, file)])
        return self


    # need to sort this out better so it uses lists, not dicts, for sub dirs
    def __build_nested_helper(self, path, file, container):
        segs = path.split('/')
        head = segs[0]
        tail = segs[1:]
        if not tail:
            container[head] = file
        else:
            if head not in container:
                container[head] = {}
            self.__build_nested_helper('/'.join(tail), file, container[head])

    def __build_nested(self, path, file, container):
        self.__build_nested_helper(path, file, container)
        return container

    def getNav(self):
        return self.moduleNav

    def getResolvedPaths(self):
        return self.resolvedPaths
