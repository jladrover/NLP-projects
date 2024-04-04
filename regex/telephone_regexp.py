import re
import argparse
import re
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('TextFile', metavar='textfile', type=str)
args = parser.parse_args()
with open(args.TextFile, 'r') as file:
    data = file.read()

tele_pattern = r'\([0-9]{3}\)[-\.\s][0-9]{3}[-\.\s][0-9]{4}'

matches = re.findall(tele_pattern, data)
matches = [re.sub(r'\n', ' ', match) for match in matches]  # Remove newline characters

matches_line = ' '.join(matches)

with open('telephone_output.txt', 'w') as file:
    file.write(matches_line)

# print("matches: " + str(len(matches)))

with open('telephone_output.txt', 'w') as file:
    for match in matches:
        print(match)
        file.write(f'{match}\n')
print("matches: " + str(len(matches)))