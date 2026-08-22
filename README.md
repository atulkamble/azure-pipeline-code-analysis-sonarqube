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


### Troubleshoot 
```
1. Go to https://marketplace.visualstudio.com/items?itemName=SonarSource.sonarqube
2. Click **Get it free** and select your Azure DevOps organization.
3. An org admin must approve/install it (Organization Settings → Extensions if you already have access but it's pending approval).
```

### SonarQube Connection 

Yes. If you're using **SonarQube Server (self-hosted)**, you need a machine/server where SonarQube is actually running. It does **not** need to be a physical machine.

For your Azure DevOps practice, the architecture can be:

```text
GitHub / Azure Repo
       ↓
Azure DevOps Pipeline
       ↓
sonarqube-connection
       ↓
SonarQube Server
       ↓
Code Analysis Dashboard
```

The SonarQube Server can run on:

```text
Azure VM        ✅
AWS EC2         ✅
Local VM        ✅
Physical Server ✅
Docker host     ✅
Your laptop     ✅ (practice)
```

The important requirement is that the **Azure DevOps pipeline agent must be able to reach the SonarQube URL**.

For example, if SonarQube runs on an Azure VM:

```text
Azure VM
Public IP: 20.x.x.x

SonarQube:
http://20.x.x.x:9000
```

Then your Azure DevOps service connection would use:

```text
Server URL:
http://20.x.x.x:9000

Token:
<sonarqube-token>

Connection Name:
sonarqube-connection
```

### Important for your lab

If you install SonarQube only on your Mac and use:

```text
http://localhost:9000
```

a **Microsoft-hosted Azure DevOps agent cannot reach your Mac's localhost**.

So for an easy training lab, I'd recommend:

**Azure VM → Docker → SonarQube → expose port 9000 → create SonarQube token → Azure DevOps service connection → run pipeline.**

Alternatively, if you use **SonarQube Cloud**, you don't need to maintain a SonarQube VM/server yourself.


```
This error is no longer about the SonarQube task version. The task is loading correctly now; Azure DevOps simply cannot find the service connection named:

```text
sonarqube-connection
```

You need to create that service connection in the Azure DevOps project, or change the YAML to use the exact name of an existing one.

Go to:

```text
Azure DevOps Project
   ↓
Project Settings
   ↓
Service connections
   ↓
New service connection
   ↓
SonarQube
```

Then enter your SonarQube server URL, for example:

```text
http://<sonarqube-server-ip>:9000
```

or:

```text
https://sonarqube.example.com
```

Generate a token in SonarQube:

```text
SonarQube
   ↓
My Account
   ↓
Security
   ↓
Generate Token
```

Copy the token and paste it into the Azure DevOps service connection configuration.

For the **Service connection name**, use exactly:

```text
sonarqube-connection
```

Then click:

```text
Verify and Save
```

If Azure DevOps shows an authorization option, enable:

```text
Grant access permission to all pipelines
```

For your lab, this is the simplest option.

Your YAML can then remain:

```yaml
- task: SonarQubePrepare@8
  inputs:
    SonarQube: 'sonarqube-connection'
    scannerMode: 'cli'
    configMode: 'manual'
    cliProjectKey: 'python-code-analysis'
    cliProjectName: 'Python Code Analysis'
    cliSources: '.'
```

The important part is this:

```yaml
SonarQube: 'sonarqube-connection'
```

That value is **not the SonarQube project name**. It is the Azure DevOps **Service Connection name**.

So your architecture is:

```text
Azure DevOps Pipeline
        |
        | uses
        v
sonarqube-connection
        |
        | token authentication
        v
SonarQube Server
        |
        v
python-code-analysis
```

If you already created a connection named something like:

```text
MySonarQube
```

then don't create another one. Just change your pipeline:

```yaml
SonarQube: 'MySonarQube'
```

The names must match exactly.

After fixing it, your pipeline sequence should be:

```text
SonarQubePrepare@8
        ↓
pytest
        ↓
SonarQubeAnalyze@8
        ↓
SonarQubePublish@8
```

So the current error is essentially:

```text
Task found       ✅
Task version     ✅
YAML syntax      ✅
Service connection ❌
```

Fix/create the service connection and rerun pipeline `20260822.2`.

```
