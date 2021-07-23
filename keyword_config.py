try:
    with open('keywords.txt', 'r') as file:
        keywords = [ line.rstrip() for line in file.readlines()]
except FileNotFoundError:
    raise Exception('keywords.txt not found.')