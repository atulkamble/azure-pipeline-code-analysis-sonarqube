Here’s a simple **SonarQube Code Analysis Project** you can use for Azure DevOps practice.

### Project: Python Code Analysis with SonarQube

**Goal:** Analyze Python source code for bugs, vulnerabilities, code smells, duplication, and maintainability issues using SonarQube.

**Suggested repo name:** `sonarqube-code-analysis-python`

### Project structure

```text
sonarqube-code-analysis-python/
├── app.py
├── calculator.py
├── test_calculator.py
├── requirements.txt
├── sonar-project.properties
└── README.md
```

### `app.py`

```python
from calculator import add, divide

print("Addition:", add(10, 20))
print("Division:", divide(10, 2))
```

### `calculator.py`

Add a few intentional quality issues so SonarQube has something to detect:

```python
def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        print("Cannot divide by zero")
        return None

    return a / b


def unused_function():
    password = "admin123"
    print(password)
```

### `test_calculator.py`

```python
from calculator import add, divide


def test_add():
    assert add(10, 20) == 30


def test_divide():
    assert divide(10, 2) == 5
```

### `requirements.txt`

```text
pytest
pytest-cov
```

### `sonar-project.properties`

```properties
sonar.projectKey=python-code-analysis
sonar.projectName=Python Code Analysis
sonar.projectVersion=1.0

sonar.sources=.
sonar.tests=.
sonar.test.inclusions=test_*.py

sonar.python.coverage.reportPaths=coverage.xml

sonar.sourceEncoding=UTF-8
```

### Run tests with coverage

```bash
pip install -r requirements.txt

pytest --cov=. --cov-report=xml
```

This creates:

```text
coverage.xml
```

Then SonarQube can import the coverage report.

### SonarQube workflow

```text
Developer
   |
   v
Git Repository
   |
   v
Build Pipeline
   |
   +----> Install Dependencies
   |
   +----> Run Unit Tests
   |
   +----> Generate Coverage
   |
   +----> SonarQube Analysis
   |
   v
Quality Gate
   |
   +---- PASS ---> Continue Build/Deployment
   |
   +---- FAIL ---> Stop Pipeline
```

### Azure DevOps pipeline example

```yaml
trigger:
- main

pool:
  vmImage: ubuntu-latest

steps:

- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.12'

- script: |
    pip install -r requirements.txt
  displayName: 'Install Dependencies'

- script: |
    pytest --cov=. --cov-report=xml
  displayName: 'Run Tests and Coverage'

- task: SonarQubePrepare@7
  inputs:
    SonarQube: 'sonarqube-connection'
    scannerMode: 'CLI'
    configMode: 'file'

- task: SonarQubeAnalyze@7
  displayName: 'Run SonarQube Analysis'

- task: SonarQubePublish@7
  inputs:
    pollingTimeoutSec: '300'
  displayName: 'Publish Quality Gate'
```

The important concepts to practice are **SonarQube Server → Project → Token/Service Connection → Scanner → Code Analysis → Quality Profile → Quality Gate → Pipeline result**.

A good next project would be to deliberately introduce **5–10 SonarQube issues** into this Python application and then fix them one by one, so students can clearly see the SonarQube dashboard changing.
