
# README

## Installation

```
uv venv .venv
uv pip install -r requirements.txt
source .venv/bin/python3
```

## GitHub key

1. Go to GitHub
2. Open: Settings → Developer settings → Personal access tokens → Tokens
   (classic) → Generate new token
3. Select scope : public_repo 
4. Save the token in a `.env` file in the project root as:

```
GITHUB_KEY=yourkey
```

## Usage

```
python3 keyhunt.py --tries <NUMBER> --service <openai|anthropic>
```

