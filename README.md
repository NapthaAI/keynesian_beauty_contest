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

Don't forget to change the name of the module.

## Prototyping the Module

Before deploying to a Naptha node, you should iterate on improvements with the module locally. You can run the module using:

```bash
poetry run python <module_name>/run.py
```

When ready, let's push to your own HuggingFace or the Naptha org. Add a version number using:

```bash
git tag v0.1
```

You'll need to [generate an SSH key](https://huggingface.co/docs/hub/security-git-ssh) on HF and add it to your account. Then you'll be able to update your Git repository using:

```bash
git remote set-url origin git@hf.co:NapthaAI/<module_name>
```

More details in the HF [docs](https://huggingface.co/blog/password-git-deprecation#switching-to-ssh-keys)

```bash
git push --tags
```