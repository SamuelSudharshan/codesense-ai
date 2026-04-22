import os

def load_code(folder):
    data = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith((".py", ".js", ".cpp")):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    data.append(f.read())
    return "\n".join(data)