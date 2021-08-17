# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## v0.1.4 - 2021-08-17
### Fixed
- String encoding error in Python 3 (was returning `bytes`).

## v0.1.3 - 2021-08-06
### Fixed
- `MANIFEST.in` was missing `requirements.txt`, causing an issue when installing with `pip`.

## v0.1.2 - 2021-03-11
### Fixed
- the expression `x in [a to b]` is now correctly translated to `x >= a and x <= b`; quantifier domain semantics remain the same (only integers with `range()`).

## v0.1.1 - 2021-03-09
### Changed
- Updated the `README.md` file.

## v0.1.0 - 2021-03-09
Initial release.
