# mkdocs-terraform-monorepo-plugin

[![](https://github.com/wtc-cloud-eng/mkdocs-terraform-monorepo-plugin/workflows/Build%2C%20Test%20%26%20Deploy/badge.svg)](https://github.com/wtc-cloud-eng/mkdocs-terraform-monorepo-plugin/actions)
[![PyPI](https://img.shields.io/pypi/v/mkdocs-terraform-monorepo-plugin)](https://pypi.org/project/mkdocs-terraform-monorepo-plugin/)
![](https://img.shields.io/badge/lifecycle-beta-509bf5.svg)
[![PyPI - License](https://img.shields.io/pypi/l/mkdocs-terraform-monorepo-plugin)](LICENSE)


> **Note: This plugin is in beta.** Whilst it is not expected to significantly change in functionality, it may not yet be fully compatible with other Mkdocs configuration and thus may break with some advanced configurations. Once these have been resolved and all bugs have been ironed out, we will move this to a stable release.

✚ This plugin enables you to build multiple sets of documentation in a single Mkdocs. It is intended to auto discover documentation in a terraform modules monorepo.

## Motivation

In mkdocs, adding and combining docs into the nav from both the `docs` default directory and terraform modules directories, in a terraform monorepo, can be easily automated.  If documentation for a monorepo is auto generated using terrafrom-docs in nested submodule trees, we can build the tree automatically and add it to the mkdocs site through mkdocs configuration.

This module was totally inspired by the backstage [mkdocs-monorepo-plugin](https://github.com/backstage/mkdocs-monorepo-plugin) and shares much of the same structure.

## Install

It's easy to get started using [PyPI] and `pip` using Python:

```terminal
$ pip install mkdocs-terraform-monorepo-plugin
```

Or include it in a requirements.txt file in your project

```python
mkdocs==1.1.2
mkdocs-material==5.4.0
mkdocs-material-extensions==1.0
markdown-include==0.5.1
mkdocs-terraform-monorepo-plugin==0.1.0
```

and run

```terminal
pip install -r requirements.txt
```

## Usage

This plugin introduces the `!tf_modules_root` syntax in your Mkdocs navigation structure and then merges them into the output.  The value of `!tf_modules_root` is relative to the project config file (mkdocs.yml), not the docs directory.

```yaml
# /mkdocs.yml
site_name: MyProject

nav:
    - Home: index.md
    - User Guide:
        - Testing: user-guide/testing.md
        - Changelog: user-guide/changelog.md
    - Modules:
        - Convention: '!tf_modules_root convention'
    - Examples: '!tf_modules_root examples'
    - About:
        - Release Notes: about/release-notes.md
        - Contributing: about/contributing.md
        - License: about/license.md
        - Code of Conduct: about/code-of-conduct.md

plugins:
  - terraform-monorepo
  - search
  # if you include another plugin, and want search you have to add it again

```

### Example Source Filetree

```terminal
$ tree .
├── convention
│   ├── naming
│   │   ├── compute
│   │   │   ├── faas
│   │   │   │   ├── main.tf
│   │   │   │   └── README.md
│   │   │   └── machine
│   │   │       ├── main.tf
│   │   │       └── README.md
│   │   ├── dns
│   │   │   ├── main.tf
│   │   │   └── README.md
│   │   └── storage
│   │       └── bucket
│   │           ├── main.tf
│   │           └── README.md
│   ├── README.md
│   └── tags
│       └── README.md
├── docs
│   ├── about
│   │   ├── code-of-conduct.md
│   │   ├── contributing.md
│   │   ├── license.md
│   │   └── release-notes.md
│   ├── index.md
│   └── user-guide
│       ├── changelog.md
│       └── testing.md
├── examples
│   └── var_types
│       ├── inputs.tf
│       ├── main.tf
│       ├── Makefile
│       ├── outputs.tf
│       ├── README.md
├── mkdocs.yml

```

### Example Rendered Filetree

```terminal
├── 404.html
├── about
│   ├── code-of-conduct
│   │   └── index.html
│   ├── contributing
│   │   └── index.html
│   ├── license
│   │   └── index.html
│   └── release-notes
│       └── index.html
├── assets
│   ├── images
│   │   └── favicon.png
│   ├── javascripts
│   │   ├── bundle.b39636ac.min.js
│   │   ├── bundle.b39636ac.min.js.map
│   │   ├── lunr
│   │   │   ├── min
│   │   │   │   ├── lunr.multi.min.js
│   │   │   │   ├── lunr.stemmer.support.min.js
│   │   │   └── tinyseg.min.js
│   │   ├── vendor.d710d30a.min.js
│   │   ├── vendor.d710d30a.min.js.map
│   │   └── worker
│   │       ├── search.a68abb33.min.js
│   │       └── search.a68abb33.min.js.map
│   └── stylesheets
│       ├── main.fe0cca5b.min.css
│       ├── main.fe0cca5b.min.css.map
│       ├── palette.a46bcfb3.min.css
│       └── palette.a46bcfb3.min.css.map
├── convention
│   ├── naming
│   │   ├── compute
│   │   │   ├── faas
│   │   │   │   └── index.html
│   │   │   └── machine
│   │   │       └── index.html
│   │   ├── dns
│   │   │   └── index.html
│   │   └── storage
│   │       └── bucket
│   │           └── index.html
│   └── tags
│       └── index.html
├── examples
│   └── var_types
│       └── index.html
├── img
│   ├── favicon.png
│   ├── logo.png
│   └── wtc-logo.svg
├── index.html
├── search
│   └── search_index.json
├── sitemap.xml
├── sitemap.xml.gz
└── user-guide
    ├── about
    │   └── index.html
    ├── changelog
    │   └── index.html
    ├── development
    │   └── index.html
    ├── setup
    │   └── index.html
    ├── standards
    │   └── index.html
    └── testing
        └── index.html

```
