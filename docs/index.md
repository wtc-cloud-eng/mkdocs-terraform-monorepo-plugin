# wtc-cloud-eng/mkdocs-terraform-monorepo-plugin

[![](https://github.com/wtc-cloud-eng/mkdocs-terraform-monorepo-plugin/workflows/Build%2C%20Test%20%26%20Deploy/badge.svg)](https://github.com/wtc-cloud-eng/mkdocs-terraform-monorepo-plugin/actions)
[![PyPI](https://img.shields.io/pypi/v/mkdocs-terraform-monorepo-plugin)](https://pypi.org/project/mkdocs-terraform-monorepo-plugin/)
![](https://img.shields.io/badge/lifecycle-beta-509bf5.svg)
[![PyPI - License](https://img.shields.io/pypi/l/mkdocs-terraform-monorepo-plugin)](LICENSE)

> **Note: This plugin is in beta.** Whilst it is not expected to significantly change in functionality, it may not yet be fully compatible with other Mkdocs configuration and thus may break with some advanced configurations. Once these have been resolved and all bugs have been ironed out, we will move this to a stable release.

✚ This plugin enables you to build multiple sets of documentation in a single Mkdocs. It is designed to address writing documentation for Terraform monorepos, particularly when used with [terraform-docs].

🐍 [Python Package](https://pypi.org/project/mkdocs-terraform-monorepo-plugin/) | ✚ [Demo](https://spotify.github.io/mkdocs-monorepo-plugin/monorepo-example/) | 📕 [Docs](https://wtc-cloude-eng.github.io/mkdocs-terraform-monorepo-plugin/)

> **Note:  This project was adapted from the Spotify [backstage monorepo] plugin.** It follows the same structure, test patterns, principles and release patterns.

## Features

- **Support for multiple module root folders in Mkdocs.** Having a single `docs/` folder in a terraform codebase is hard to maintain. Who owns which documentation? What code is it associated with? Bringing docs closer to the associated code enables you to update them better, as well as leverage folder-based features such as [GitHub Codeowners] and documentation tooling such as [terraform-docs]

- **Limited support for [backstage monorepo] plugin navigations.** In Spotify, large repositories typically are split up by multiple owners. These are split by folders. By introducing multiple `mkdocs.yml` files along with multiple `docs/` folder, each team can take ownership of their own navigation. This plugin then intelligently merges of the documentation together into a single repository.

- **The same great Mkdocs developer experience.** It is possible to run `mkdocs serve` in the root to merge all of your documentation together, or in a subfolder to build specific documentation. Autoreload still works as usual. No more using [symlinks](https://devdojo.com/tutorials/what-is-a-symlink)!

## Install

It's easy to get started using [PyPI] and `pip` using Python:

```terminal
$ pip install mkdocs-terraform-monorepo-plugin
```

## Usage

Take a look at [our sample project](https://github.com/wtc-cloud-eng/mkdocs-terraform-monorepo-plugin/tree/master/sample-docs) or do the following:

- In the root, add `terraform-monorepo` to your `plugins` key in `mkdocs.yml`
- Create a subfolder, with a `mkdocs.yml` with a `site_name` and `nav`, as well as a `docs/` folder with an `index.md`
- Back in in the root `mkdocs.yml`, use the `!tf_modules_root` syntax in your `nav` to link to to a folder containing terraform markdown documentation.

!!! info "Example root /mkdocs.yml"

            site_name: Cats API

            # You can declare "!include" statements here. This enables you
            # to include mkdocs.yml that are located in subfolders. In this
            # case we have two folders (v1/ and v2/) and wish to merge them
            # into this single navigation. The 'Intro' and 'Authentication'
            # files are located in the root docs/ folder as usual.

            nav:
              - Intro: 'index.md'
              - Authentication: 'authentication.md'
              - API:
                - v1: '!include ./v1/mkdocs.yml'
                - v2: '!include ./v2/mkdocs.yml'

            plugins:
              - monorepo

!!! info "Example submodule /v1/mkdocs.yml"
            # In this case, we use the site_name to figure out how we should merge
            # this with the root documentation. It should refer to a folder structure.
            # The example below will merge documentation as following:
            #
            #   reference.md -> docs/versions/v1/reference.md -> http://localhost:8000/versions/v1/reference/
            #   changelog.md -> docs/versions/v1/changelog.md -> http://localhost:8000/versions/v1/changelog/
            #

            site_name: versions/v1

            nav:
              - Reference: "reference.md"
              - Changelog: "changelog.md"

            nav:
              - code-samples.md

!!! info "Example submodule /v2/mkdocs.yml"

            # It works the same as above, but with relative to the site_name we use here:
            #
            #   migrating.md -> docs/versions/v2/migrating.md -> http://localhost:8000/versions/v2/migrating/
            #   reference.md -> docs/versions/v2/reference.md -> http://localhost:8000/versions/v2/reference/
            #   changelog.md -> docs/versions/v2/changelog.md -> http://localhost:8000/versions/v2/changelog/

            site_name: versions/v2

            nav:
              - Migrating to v2: "migrating.md"
              - Reference: "reference.md"
              - Changelog: "changelog.md"

An example filetree when using the Mkdocs Monorepo plugin looks like this:

```terminal
$ tree .

├── docs
│   ├── authentication.md
│   └── index.md
├── mkdocs.yml
├── v1
│   ├── docs
│   │   ├── changelog.md
│   │   └── reference.md
│   └── mkdocs.yml
└── v2
    ├── docs
    │   ├── changelog.md
    │   ├── migrating.md
    │   └── reference.md
    └── mkdocs.yml

5 directories, 10 files
```

## Supported Versions

- Python 3 &mdash; 3.5, 3.6, 3.7
- [Mkdocs] 1.1.1 and above.
- [monorepo plugin] 0.4.5.

## License

Released under the Apache 2.0 License. See [here](https://github.com/wtc-cloud-eng/mkdocs-terraform-monorepo-plugin/blob/master/LICENSE) for more details.

Also see [backstage monorepo](https://github.com/backstage/mkdocs-monorepo-plugin/blob/master/LICENSE) for more details.

## Contributing

Check out our [CONTRIBUTING](./CONTRIBUTING.md) for more details.

## Extra Reading

- [mkdocs][mkdocs/mkdocs] on GitHub
- [Mkdocs] documentation
- This was built using the [mkdocs-plugin-template]

[mkdocs/mkdocs]: https://github.com/mkdocs/mkdocs
[mkdocs-plugin-template]: https://github.com/byrnereese/mkdocs-plugin-template
[pypi]: https://pypi.org
[mkdocs]: https://www.mkdocs.org
[backstage monorepo]: https://backstage.github.io/mkdocs-monorepo-plugin/
[github codeowners]: https://help.github.com/en/articles/about-code-
[terraform-docs]: https://terraform-docs.io/
