# docker-pre-commit

A set of [pre-commit](http://pre-commit.com) hooks for Docker services

# Installation

Add the following to your `.pre-commit-config.yaml` file

```yaml
  - repo: https://github.com/NtWriteCode/docker-pre-commit-universal
    rev: v0.0.1
    hooks:
      - id: docker-compose-check
```

and then run `pre-commit autoupdate`.


## Hooks

### docker-compose-check
Verifies that docker compose files are valid by using `docker compose config` to parse them.

This repository is the for of [IamTheFij/docker-pre-commit](https://github.com/IamTheFij/docker-pre-commit), because that originally used a shell script, which was failing on Windows. I just quickly rewrote it on python, so it works cross-platform.
