# Backend Setup

## Virtual Environment
The project uses a Python virtual environment located at:
```
~/.venvs/med-auditor-venv
```

Python interpreter path:
```
~/.venvs/med-auditor-venv/bin/python
```

## Activating the Environment
```bash
source ~/.venvs/med-auditor-venv/bin/activate
```

## IDE Configuration
Create a local `.vscode/settings.json` file (this file is gitignored) with the following content:

```json
{
    "python.defaultInterpreterPath": "~/.venvs/med-auditor-venv/bin/python",
    "python.terminal.activateEnvironment": true
}
```

If you're using a different IDE, configure it to use the Python interpreter at:
```
~/.venvs/med-auditor-venv/bin/python
``` 