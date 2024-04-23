#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


def get_compose_binary() -> str:
    compose_binary = 'docker compose'
    try:
        subprocess.run(['docker', 'help', 'compose'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.run(['docker-compose'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            compose_binary = 'docker-compose'
        except subprocess.CalledProcessError:
            print('ERROR: Neither "docker-compose" nor "docker compose" were found')
            sys.exit(1)

    return compose_binary


def check_file(file: str) -> int:
    try:
        result = subprocess.run([get_compose_binary(), '--file', file, 'config', '--quiet'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except Exception:
        return 1
    else:
        return result.returncode


def check_files(all_files: list[str]) -> bool:
    has_error = False
    for file in all_files:
        if Path(file).is_file() and check_file(file) != 0:
            print(f'ERROR: {file}')
            has_error = True
    return has_error


def main() -> None:
    if check_files(sys.argv[1:]):
        print('Some compose files failed')
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
