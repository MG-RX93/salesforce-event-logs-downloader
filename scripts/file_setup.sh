#!/bin/bash

: <<'END_COMMENT'
See docs/directory_structure for all the files used and their descriptions.
END_COMMENT


# Create .vscode dir files
touch .vscode/launch.json # debug configuration file

# Create .github/workflow files (Testing, Building, Linting)
touch .github/workflows/ci_test.yml .github/workflows/ci_build.yml .github/workflows/ci_lint.yml

# Create shared dir files
touch src/__init__.py src/auth.py src/query.py

# Create tests dir files
touch tests/__init__.py tests/test_auth.py tests/test_query.py

# Create package related files
touch requirements.txt setup.py .env 

# Create directory structure to serve as an example for creating project directories
touch docs/directory_structure.md