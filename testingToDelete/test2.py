import json

file = open('./attack_pattern_validation.jsonl', "rb")
print(file)

data = file.read()

for line in json.loads(data):
    with open('attack_pattern_validation_formatted.jsonl', 'a') as f:
        f.write(json.dumps(line))
        f.write('\n')