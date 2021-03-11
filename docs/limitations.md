# Caveats / Known Design Decisions

- In the modules directory, the only doc file searched for is README.md
- If a folder, with child documentation, also has a README.md in it, the Navigation item will be called `About`
- Due to how [backstage monorepo] manipulates the navigation and docs folder, the terraform-monorepo plugin should be listed after the monorepo plugin in order for nested mkdocs files to render
- if using the [backstage monorepo] in conjustion with this plugin, [backstage monorepo] plugin should be pinned to 0.4.5 to prevent an error in rendering the site - introduced in [this change](https://github.com/backstage/mkdocs-monorepo-plugin/pull/13/commits/3d5426c3e32e6e82764f6250dc1e11520af0fc16)


[backstage monorepo]: https://backstage.github.io/mkdocs-monorepo-plugin/
