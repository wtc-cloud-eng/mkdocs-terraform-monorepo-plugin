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

### Example root /mkdocs.yml"

```
site_name: terraform monorepo

nav:
  - Intro: 'index.md'
  - Modules:
    - AWS: '!tf_modules_root ./aws'
    - Azure: '!tf_modules_root ./azurerm'
    - GCP: '!tf_modules_root ./gcp'

plugins:
  - terraform-monorepo

```

An example filetree when using the Mkdocs Terraform Monorepo plugin looks like this:

```terminal
$ tree .
.
├── aws
│   ├── README.md
│   └── s3
│       └── private_bucket
│           └── README.md
├── azurerm
│   ├── blob_storage
│   │   └── container
│   │       └── README.md
│   └── README.md
├── docs
│   └── index.md
├── gcp
│   └── README.md
└── mkdocs.yml

8 directories, 7 files

```

## Supported Versions

- Python 3 &mdash; 3.6, 3.7
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
