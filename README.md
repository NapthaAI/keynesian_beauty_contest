# Template

This is a base template for creating task and flow modules. You can check out other examples of task and flow modules (and request to join the organization!) at https://huggingface.co/NapthaAI. 

## Pre-Requisites 

### Install Poetry 

From the official poetry [docs](https://python-poetry.org/docs/#installing-with-the-official-installer):

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/home/$(whoami)/.local/bin:$PATH"
```

### Clone and Install the Module

Clone the repo using:

```bash
git clone https://huggingface.co/NapthaAI/template
cd template
```

You can install the module using:

```bash
poetry install
```

## Prototyping the Module

Before deploying to a Naptha node, you should iterate on improvements with the module locally. You can run the module using:

```bash
poetry run python template/run.py
```

When ready, push to your own HuggingFace or the Naptha org. Don't forget to change the name.