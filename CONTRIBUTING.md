# Contributing

Contributions are very welcome! Any existing issues labeled ["help wanted"](https://github.com/devshawn/kafka-shell/labels/help%20wanted) or ["good first issue"](https://github.com/devshawn/kafka-shell/labels/good%20first%20issue) are free to be pursued.

## Feature Requests & Bug Reports
For feature requests and bug reports, [submit an issue][issues].

## Style Guide
We follow [PEP8][pep8] as the general style guide with the following changes:

- Line length can be up to 120 characters long
- Double quotes for all strings except when avoiding backslashes

We use `flake8` for linting and `pytest` with `tox` for testing.

## Pull Requests
The preferred way to contribute is to fork the [main repository][repository] on GitHub.

1. Discuss your proposed change in a GitHub issue first before spending time and implementing a feature or fix.

2. Ensure all changes are relevant to the pull request. Keep pull requests as small and to-the-point as possible.

3. Add & modify tests as necessary. Also, ensure the code meets our style standards.

4. Once changes are completed, open a pull request for review against the master branch.


[repository]: https://github.com/devshawn/kafka-shell
[issues]: https://github.com/devshawn/kafka-shell/issues
[pep8]: https://www.python.org/dev/peps/pep-0008/
