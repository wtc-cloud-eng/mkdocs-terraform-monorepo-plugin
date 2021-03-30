import setuptools


setuptools.setup(
    name='mkdocs-terraform-monorepo-plugin',
    version='0.1.3',
    description='Plugin for adding doc tree for terraform monorepos.',
    long_description_content_type='text/plain',
    long_description="""
        This introduces support for the !tf_modules_root syntax in mkdocs.yml, allowing you to import trees of README.md files for terraform modules directories that also contains a \*.tf file.
        It enables large or complex repositories to have their own tree of modules folders, whilst generating only a single Mkdocs site.
        This is built and maintained by the engineering community at Wunderman Thompson Commerce.
        It was, however, inspired by and adapted from the Spotify backstage monorepo plugin.
    """,  # noqa: E501
    keywords='mkdocs terraform monorepo plugin',
    url='https://github.com/wtc-cloud-eng/mkdocs-terraform-monorepo-plugin',
    author='Richard Wittrick',
    author_email='richard.wittrick@wundermanthompson.com',
    license='Apache-2.0',
    python_requires='>=3',
    install_requires=[
        'mkdocs>=1.1.1'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=setuptools.find_packages(),
    entry_points={
        'mkdocs.plugins': [
            "terraform-monorepo = mkdocs_terraform_monorepo_plugin.plugin:TerraformMonorepoPlugin"
        ]
    }
)
