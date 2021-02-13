import pickle
import json
import yaml

# Round-trip reading and writing the following formats:
# - yaml
# - json
# - pickle

dict = { 'name':'Barča', 'age':13, 'list':[1, 2, 3, 4, 5], 'set':['1', '2', '3']}
dict2 = {}

print(f"dict = {dict}")

# Yaml (pip3 install pyyaml)
yaml_file = 'data.yaml'
with open(yaml_file, 'w', encoding='utf8') as f:
  f.write(yaml.dump(dict, allow_unicode=True))

with open(yaml_file, 'r') as f:
  dict2 = yaml.load(f, Loader=yaml.FullLoader)
print(f"yaml = {dict}")

# Json
json_file = 'data.json'
with open(json_file, 'w', encoding='utf8') as f:
  json.dump(dict, f, ensure_ascii=False, indent=2)

with open(json_file, 'r') as f:
  dict2 = json.load(f)
print(f"json = {dict}")

# Pickle - Python serialization
with open('data.pkl', 'wb') as f:
  pickle.dump(dict, f)

with open('data.pkl', 'rb') as f:
  dict2 = pickle.load(f)

print(f"pickle = {dict}")
