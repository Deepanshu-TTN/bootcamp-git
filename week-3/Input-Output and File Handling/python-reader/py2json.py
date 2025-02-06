import json

def result_builder(file_path):
    result = {
    "package": [],
    "function": [],
    "class": [],
    "variable": []
    }

    with open(file_path, 'r') as script:

        for line in script:
            if line.startswith("import "):
                packages = line[7:].split(',')
                for package in packages:
                    package = package.strip()
                    if '.' in package:
                        package = package.split('.')[0]
                    if package:
                        result["package"].append(package)

            elif line.startswith("class "):
                class_name = line[6:].split('(')[0].split(":")[0].strip()
                if class_name:
                    result["class"].append(class_name)

            elif line.startswith("def "):
                func = line[4:].split("(")[0].strip()
                if func:
                    result["function"].append(func)
            
            elif "=" in line and not line.startswith(("if", "for", "while", "elif", "def", "class")):
                lefty = line.split("=")[0]
                if "," in lefty:
                    variables = [v.strip() for v in lefty.split(',')]
                else: variables = [lefty.strip()]

                for v in variables:
                    if v: result["variable"].append(v)
    
    return result


anal_result = result_builder("Python_script.py")

with open("tokens.json", "w") as data:
    json.dump(anal_result, data, indent=4)

print(json.dumps(anal_result, indent=4))