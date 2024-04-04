import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('TextFile', metavar='textfile', type=str, help='file to process')
args = parser.parse_args()
with open(args.TextFile, 'r') as file:
    data = file.read()


# money_pattern =  r'(\$[0-9]+([\.\s][0-9]+)?)|(\$[0-9]\s+(million|billion|thousand|trillion))|(([0-9]\s+(hundred|million|billion|thousand|trillion)\s?(\s?dollars?))|((one|two|three|four|five|six|seven|eight|nine|ten)\s*(hundred|million|billion|thousand|trillion)\s?(\s?dollars?)))'
# money_pattern = r'|\$\d+|\w+\s+dollars?'
# money_pattern = r'\$[0-9]+[\.\s][0-9]+|\$[0-9]+\,[0-9]+|[0-9]+\,[0-9]+ dollars| \w+ dollars'
money_pattern = r'\$[0-9]+(?:\,[0-9]{3})*(?:\.[0-9]{1,2})?|\w+ hundred thousand dollars|\w+ thousand dollars|\w+\,\w* dollars|\w+\s+dollars?'

matches = re.findall(money_pattern, data)
count = len(matches)
with open('dollar_output.txt', 'w') as file:
    for match in matches:
        print(match)
        file.write(f'{match}\n')
print("matches: " + str(count))

