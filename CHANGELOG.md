# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2021-08-06
### Fixed
- `MANIFEST.in` was missing `requirements.txt`, causing an issue when installing with `pip`.

## [0.1.2] - 2021-03-11
### Fixed
- the expression `x in [a to b]` is now correctly translated to `x >= a and x <= b`; quantifier domain semantics remain the same (only integers with `range()`).

## [0.1.1] - 2021-03-09
### Changed
- Updated the `README.md` file.

## [0.1.0] - 2021-03-09
Initial release.
