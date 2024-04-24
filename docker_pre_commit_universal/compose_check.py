#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


def get_compose_binary() -> list[str]:
    compose_binary = ['docker', 'compose']
    try:
        subprocess.run(['docker', 'help', 'compose'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.run(['docker-compose'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            compose_binary = ['docker-compose']
        except subprocess.CalledProcessError:
            print('ERROR: Neither "docker-compose" nor "docker compose" were found')
            sys.exit(1)

    return compose_binary


def check_file(file: str) -> subprocess.CompletedProcess[bytes] | None:
    try:
        commands = get_compose_binary()
        commands.append('--file')
        commands.append(file)
        commands.append('config')
        commands.append('--quiet')
        result = subprocess.run(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    except Exception as e:
        print(f'Exception happened during the execution of {commands!s}: {e!s}')
        return None
    else:
        return result


def check_files(all_files: list[str]) -> bool:
    has_error = False
    for file in all_files:
        if Path(file).is_file():
            proc = check_file(file)
            if proc and proc.returncode != 0:
                print(f'> Error in {file}:')
                print(f'\t{proc.stdout.decode().strip()} {proc.stderr.decode().strip()}')
                has_error = True
            elif not proc:
                print()
    return has_error


def main() -> None:
    if check_files(sys.argv[1:]):
        print('Docker compose validation resulted in failure!')
        sys.exit(1)
    else:
        print('All docker compose files successfully validated.')
        sys.exit(0)


if __name__ == '__main__':
    main()
