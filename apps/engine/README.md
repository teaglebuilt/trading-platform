# Engine

Strategy runtime api

## Responsibilities

- Run custom strategies (stocks) or wrap external frameworks (Freqtrade/Jesse for crypto).

- Convert signals + market data → OrderIntent.

- Risk checks via risk/ before passing to Executor.
