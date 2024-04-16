import os
import dotenv
import glob

dotenv.load_dotenv()

variables = list()
file_path = os.path.join(os.getcwd(), ".env")
with open(file_path, "r") as file:
    for line in file:
        splitIndex = line.find("=")
        key = line[:splitIndex]
        value = line[splitIndex+1:]
        value = value.strip("\n\"")
        #key, value = line.strip().split("=")
        variables.append((key, value))

folder_path = os.path.join(os.getcwd(), "debug")
if os.path.exists(folder_path):
    print("Debug folder exists")
else:
    os.makedirs(folder_path)
    print("Debug folder created")
          
json_files = glob.glob("api-payload/*.json")
for file in json_files:
    with open(file, "r") as json_file:
        data = json_file.read()
        for key, value in variables:
            data = data.replace(key, value)
        output_file_path = os.path.join(folder_path, os.path.basename(file))
        with open(output_file_path, "w") as output_file:
            output_file.write(data)
            
print("Files prepped for loading")
            
          





