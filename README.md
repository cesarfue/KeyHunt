
# README

Simple instructions for installing dependencies, generating a GitHub personal access token, and running the key-testing script.

## Installation

```bash uv venv .venv
uv pip install -r requirements.txt ```

## GitHub key (Personal Access Token)

1. Go to GitHub and sign in.
2. Open: Settings → Developer settings → Personal access tokens → Tokens
   (classic) → Generate new token. 
3. Select scope : public_repo 
4. Save the token in a `.env` file in the project root as:

``` GITHUB_KEY=yourkey ```

## Usage

```bash python your_script.py --tries <NUMBER> --service
<openai|anthropic> ```

