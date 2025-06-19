import os
from pathlib import Path

# Feature-based project structure
project_structure = {
    "alembic": ["env.py", "script.py.mako", "versions/"],
    "src": {
        "features": {
            "item": {
                "api": ["__init__.py", "routes.py"],
                "models": ["__init__.py", "item.py"],
                "schemas": ["__init__.py", "item.py"],
                "services": ["__init__.py", "item_service.py"],
                "tests": ["__init__.py", "test_item_service.py", "test_routes.py"],
                "__files__": [],
            },
            # Add more features like "user", "order" here
        },
        "core": ["__init__.py", "config.py", "database.py", "logging.py"],
        "__files__": ["main.py", "dependencies.py", "middleware.py", "__init__.py"],
    },
    "tests": {
        "__files__": ["__init__.py", "conftest.py"],
    },
    "__files__": [
        ".env",
        ".gitignore",
        "Dockerfile",
        "docker-compose.yml",
        "pyproject.toml",
        "README.md",
    ],
}


def create_structure(base_path: Path, structure):
    for name, content in structure.items():
        if name == "__files__":
            for file_name in content:
                file_path = base_path / file_name
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.touch()
        elif isinstance(content, list):
            dir_path = base_path / name
            dir_path.mkdir(parents=True, exist_ok=True)
            for item in content:
                if item.endswith("/"):
                    (dir_path / item).mkdir(parents=True, exist_ok=True)
                else:
                    (dir_path / item).touch()
        elif isinstance(content, dict):
            dir_path = base_path / name
            dir_path.mkdir(parents=True, exist_ok=True)
            create_structure(dir_path, content)


if __name__ == "__main__":
    base_dir = Path(".")
    create_structure(base_dir, project_structure)
    print("Feature-based project structure created successfully.")
