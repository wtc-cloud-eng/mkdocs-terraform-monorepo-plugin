# Contributing

We welcome contributions! We believe that by fostering a healthy, inclusive, and active open source community that we will be able to build better software for all. A large part of that is by having an enforced [code of conduct](./CODE-OF-CONDUCT.md) as well easy to use contributing guidelines.

## Prerequisites

- Python 3+ or above (with Pip)
- [Mkdocs](https://www.mkdocs.org) 1.0.4 or above
- Docker
- Git

## Build from source

This part should be easy. If it's not, let us know! The first thing you'll want to do is import the repository and open up the directory.

```terminal
$ git clone git@github.com:wtc-cloud-eng/mkdocs-terraform-monorepo-plugin.git
```

Then using the `--editable` flag, you can install the package locally. This points the actual plugin to the folder which allows you to make changes dynamically without having to re-install it every time you want to test a change.

```terminal
$ cd mkdocs-terraform-monorepo-plugin/
$ pip install --editable .
$ pip install -r requirements.txt
```

Great, now you have the `terraform-monorepo` plugin available in `Mkdocs`. This allows you to do the following in an `mkdocs.yml` without errors:

```yaml
site_name: Example Site

plugins:
  - terraform-monorepo
```

Of course, you'll need a folder to test it in. There is a conveniently folder named `sample-docs/` folder that you can use to test your changes, although you can run `mkdocs serve` in any project you want as long as the `mkdocs.yml` has `terraform-monorepo` mentioned in the `plugins` key.

```terminal
$ cd sample-docs/
$ mkdocs serve
```

Optionally, you can run it using [Mkdocs Material] which is what is powering the docs you're currently looking at. It makes Mkdocs really nice to work with. You can then simply pass through `--theme` to your `mkdocs serve` command like usual.

```terminal
$ pip install mkdocs-material
$ mkdocs serve --theme material
```

That's pretty much it. Experiment, play about, make the changes you need.

## How does it work?

Oh yes, that's worth mentioning! It works quite easily actually. There are two parts to the process: resolving the navigation, and merging the documentation folders.

### Resolving the navigation

This is responsible for making sure whenever you use the `!tf_modules_root` statement in `nav` inside our `mkdocs.yml` that we walk the folder looking for README.md files, and then appropriately import that into the `nav`. So to give you an example:

```yaml tab="Source mkdocs.yml files"
# mkdocs.yml
site_name: Example Site

plugins:
  - terraform-monorepo

nav:
  - Getting Started: README.md
  - Modules:
    - Convention: '!tf_modules_root convention'
  - Contributing: contributing.md
```

Any mid-level README found in the tree is treated as a general `About` document for the module.  For example, the directory tree might look like this for the above mkdocs.yaml:

```bash
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
│   │   ├── storage
│   │   │   └── bucket
│   │   │       ├── main.tf
│   │   │       └── README.md
│   │   └── README.md
│   └── tags
       └── README.md
```

The navigation would be:

```text
Convention -> naming -> About # and the tree path is convention/naming/README.md
Convention -> naming -> storage -> bucket # and the tree path is convention/naming/storage/bucket/README.md
```
This is to avoid repetition in naming of a module that has a tree - e.g. preventing a nav of Convention -> naming -> Naming, while allowing the `naming` node of the tree to have navigable children.

The Python code related to this component lives in `mkdocs_terraform_monorepo_plugin/parser.py`.

### Merging the docs folders

This takes the work the resolver does and applies it to reality. It is responsible for creating a temporary folder using Python's `TemporaryFolder()` and moves the `docs/` folder.

The Python code related to this component lives in `mkdocs_terraform_monorepo_plugin/merger.py`.

# Making a change

That's excellent! We're very happy that you'd like to contribute. We are very welcoming to any contributions. It is important to note a few things before you do so:

- **Consider opening an issue first.** It's easy to fall into the trap to create a bug for something that isn't agreed upon. GitHub issues is a great way to act as a validator for your contribution ideas. We try our best to engage in these as much as possible to make this as painless as possible, as it's easier to write the code than discuss it. It also significantly reduces the chances of us rejecting it.

- **Write tests.** Of course, shipping stuff is pretty cool. Especially when it's a really nice improvement. In this case, there will have many others depending on our source code. It is a small ask for ask you to test your code in a basic capacity, so that it isn't prone to being broken or removed in the future accidentally. Adding complete test coverage is something we will suggest on a case-by-case basis, depending on the type of change it is.

- **Not every contribution will be approved.** Of course, given how much volunteered time you and others spend, it is a great way of saying thank you for to accept and merge every pull request - but in reality, doing so is more harmful than valuable. We want to leverage open source to make software better for everyone rather than for a few. This means considering the long-term value of changes, as well as any impact it may have - will it break existing integrations? will it slow performance? is this a convention others will understand? As a general rule of thumb, we highly encourage you open a GitHub issue first to discuss your ideas. It will help everyone in the long run for just a little bit more time.

That out of the way, here's what you need to do:

```terminal
$ git checkout -b username/branch-name
# ... make your changes
$ code ./setup.py # make sure you bump up the version on line 6
$ git add --patch # validate your changes
$ git commit -m 'changed X and Y' # ensure you write a meaningful commit message
$ git push -u origin HEAD
```

It might say you don't have permissions to push to our repository. That's alright, using [hub fork](https://hub.github.com/hub-fork.1.html) you can fork the repository on GitHub and then replace the `origin` remote with your own directly from your Terminal:

```terminal
$ hub fork --remote-name origin
$ git remote rm origin
$ git remote add origin git@github.com:[USERNAME]/mkdocs-terraform-monorepo-plugin.git
$ git push -u origin HEAD
$ hub pull-request -b wtc-cloud-eng:main --message 'Pull request title' --browse # add --draft if you want to push it as a draft PR
```

This will create the pull request in our repository. You can of course do it through GitHub.com or their desktop clients too :)

# Running tests

The command below will use Docker to run our test suites in numerous Python versions. It may take some time on first run, but should be very fast afterwards. When you're done, feel free to run `docker prune` to clear them from your local cache. We use the `slim` versions of the public `python` images from [Docker Hub](https://hub.docker.com).

```terminal
$ ./__tests__/test-local.sh
```

For faster tests, you can opt to run in Python 3.7 rather than all supported Python versions:

```terminal
$ PYTHON_37_ONLY=1 ./__tests__/test-local.sh
```

[GitHub Actions] will always execute tests a little faster (due to parallelization) when you push your branch. Due to this, you can choose to opt of running them locally if you wish!

# Submitting a PR

Feel free to open up a PR and share why you think this change is valuable (unless it's something obvious, like a typo or confirmed bug). Assuming it is a change that is wanted, a maintainer will take a look to see if there's any changes needed.

[mkdocs material]: https://squidfunk.github.io/mkdocs-material/
[github actions]: https://github.com/features/actions
