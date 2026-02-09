# QA Automation Assessment Framework

This pytest framework is designed to assess QA automation engineering candidates' skills in Python, pytest, API testing, and test design patterns.

## Overview

This framework tests the [RESTful Booker API](https://restful-booker.herokuapp.com/apidoc/index.html) and includes:

- [pytest documentation](https://docs.pytest.org/)
- [RESTful Booker API documentation](https://restful-booker.herokuapp.com/apidoc/index.html)

## Setup

1. Install uv. [Installation guide](https://docs.astral.sh/uv/getting-started/installation/)
2. Create virtual environment using uv
    ```bash
    uv venv
    ```
    This will create the folder and automatically download python if necessary
3. Install dependencies
    ```bash
    uv sync
    ```
3. If virtual environment is not activated automatically, run this command to enter the virtual environment
    Linux or MacOS
    ```bash
    source .venv/bin/activate
    ```

    Windows
    ```shell
    .venv\Scripts\activate
    ```

## Run tests

To run all tests in this project.
```
uv run pytest
```

Please refer to Makefile for more commands.
