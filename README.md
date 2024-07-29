[![.github/workflows/main.yaml](https://github.com/xeroc/python-solana-actions/actions/workflows/main.yaml/badge.svg?branch=main)](https://github.com/xeroc/python-solana-actions/actions/workflows/main.yaml)
![pypi](https://img.shields.io/pypi/v/solana-actions.svg)
![versions](https://img.shields.io/pypi/pyversions/solana-actions.svg)
[![documentation](https://readthedocs.org/projects/python-solana-actions/badge/?version=latest)](https://python-solana-actions.readthedocs.org)
[![Pre-Commit Enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

# python-solana-actions

Solana Actions library in python.

## Documentation

Full Documentation is available on [python-solana-actions.rtfd.io](https://python-solana-actions.rtfd.io).

## Installation

    pip3 install solana-actions

## Resources

- [How to Build Solana Actions](https://youtu.be/kCht01Ycif0)
- [more resources for Solana Actions and blinks](https://solana.com/solutions/actions)

## Examples

Please find implementation examples in this repo:

- [Using Flask](https://github.com/xeroc/python-solana-actions/tree/main/examples/flask)
- [Using FastAPI](https://github.com/xeroc/python-solana-actions/tree/main/examples/fastapi)

## Grant

Many thanks to [Superteam](https://de.superteam.fun/) for funding the development of this library through an [instagrant](https://earn.superteam.fun/grants/).

## What are Solana Actions?

[Solana Actions](https://solana.com/docs/advanced/actions#actions) are
specification-compliant APIs that return transactions on the Solana blockchain
to be previewed, signed, and sent across a number of various contexts, including
QR codes, buttons + widgets, and websites across the internet. Actions make it
simple for developers to integrate the things you can do throughout the Solana
ecosystem right into your environment, allowing you to perform blockchain
transactions without needing to navigate away to a different app or webpage.

## What are blockchain links (blinks)?

[Blockchain links](https://solana.com/docs/advanced/actions#blinks) – or blinks
– turn any Solana Action into a shareable, metadata-rich link. Blinks allow
Action-aware clients (browser extension wallets, bots) to display additional
capabilities for the user. On a website, a blink might immediately trigger a
transaction preview in a wallet without going to a decentralized app; in
Discord, a bot might expand the blink into an interactive set of buttons. This
pushes the ability to interact on-chain to any web surface capable of displaying
a URL.

## License

[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)
