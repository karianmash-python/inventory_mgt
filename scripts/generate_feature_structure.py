import os
import sys


def create_feature_structure(base_dir: str, feature_name: str):
    subfolders = [
        "api",
        "schemas",
        "models",
        "repository",
        "service"
    ]

    feature_path = os.path.join(base_dir, "src", "features", feature_name)
    os.makedirs(feature_path, exist_ok=True)

    # Create __init__.py in the root feature folder
    init_file = os.path.join(feature_path, "__init__.py")
    open(init_file, 'a').close()

    for folder in subfolders:
        folder_path = os.path.join(feature_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        open(os.path.join(folder_path, "__init__.py"), 'a').close()

    print(f"✅ Structure created for feature: '{feature_name}'")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_feature_structure.py <feature_name>")
        sys.exit(1)

    feature_name = sys.argv[1]
    create_feature_structure(base_dir=".", feature_name=feature_name)

# Run the script
# python scripts/generate_feature_structure.py <feature_name>
