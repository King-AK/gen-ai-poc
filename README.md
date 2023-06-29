# gen-ai-poc
PoC repo for working with LLMs to generate code

## Usage
Ensure you have Python3.8+ installed.

Create a .env file and populate your OpenAI API key under the variable `OPENAI_API_KEY`.

Make and activate a python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Interact with the python program. The `-h` flag may be used to get more information.

```bash
python python_generator.py -h
```

Generates the following usage information:
```
usage: python_generator.py [-h] [-b REQUIREMENT_FILE] [-l LICENSE_FILE] [-m OPENAI_MODEL_NAME] [-r]

Generate a Python Repository

options:
  -h, --help            show this help message and exit
  -b REQUIREMENT_FILE, --requirement_file REQUIREMENT_FILE
                        Prompt File Containing Requirements Description
  -l LICENSE_FILE, --license_file LICENSE_FILE
                        Prompt File Containing License Information
  -m OPENAI_MODEL_NAME, --openai_model_name OPENAI_MODEL_NAME
                        OpenAI Model to use
  -r, --run             Specify if an actual run should be performed (Send requests to OpenAI). If not specified, will only generate prompt.
```