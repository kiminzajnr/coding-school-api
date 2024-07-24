# Coding School RESTful API

## Description
This project is an API for a coding school designed to manage courses, projects, tasks, tags and  users. It allows for CRUD operations on all entities, supports authentication, and includes detailed documentation for ease of use.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [License](#license)
- [References](#references)

## Installation
### Prerequisites
- Python 3.8+
- pip
- Virtual environment

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/kiminzajnr/coding-school-api.git
    cd coding-school-api
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    . venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. Run the application:
    ```bash
    flask run
    ```

## Usage
### Examples
- To create a new user:
    ```bash
    curl -X POST http://127.0.0.1:5000/register -d '{"username": "John", "password": "1234", "email": "john@example.com"}' -H "Content-Type: application/json"
    ```

- To get a list of courses:
    ```bash
    curl http://127.0.0.1:5000/course
    ```

## Features
- Feature 1
- Feature 2
- Feature 3

## Contributing
Guidelines for contributing to the project.

## License
This project is licensed under the MIT License. See the [LICENSE](/LICENSE) file for details.

## References
Links to additional resources, documentation, or related projects.
