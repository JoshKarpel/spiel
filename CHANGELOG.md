# Changelog

## 0.4.2

### Added

- [#163](https://github.com/JoshKarpel/spiel/pull/163) Added a public `present` function that presents the deck at the given file.

## 0.4.1

### Fixed

- [#157](https://github.com/JoshKarpel/spiel/pull/157) Pinned to Textual v0.4.0 to work around https://github.com/Textualize/textual/issues/1274

## 0.4.0

### Changed

- [#154](https://github.com/JoshKarpel/spiel/pull/154) Switch to [Textual](https://textual.textualize.io/) as the overall control and rendering engine.

### Removed

- [#154](https://github.com/JoshKarpel/spiel/pull/154) Removed library-provided `Example` slides, `Options`, and various other small features
  as part of the Textual migration. Some of these features will likely be reintroduced later.

## 0.3.0

### Removed

- [#129](https://github.com/JoshKarpel/spiel/pull/129) Dropped support for Python `<=3.9`.
