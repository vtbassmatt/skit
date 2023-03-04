# How to ship

1. Bump version number in pyproject.toml, commit the change
2. `git tag -am "v<version>" v<version>`
3. `git push --tags`
4. `poetry build && poetry publish`
