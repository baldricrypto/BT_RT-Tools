# basic ROT13 Code breaker

code = input("Input your code:\n")

ROT13_pre = "nopqrstuvwxyzabcdefghijklm"
ROT13 = [*ROT13_pre]
ROT13_upper = [*ROT13_pre.upper()]

alphabet_pre = "abcdefghijklmnopqrstuvwxyz"
alphabet =[*alphabet_pre]
alphabet_upper = [*alphabet_pre.upper()]

code = [*code]
broken_code = []

for letter in code:
    if letter in alphabet:
        for index, char in enumerate(alphabet):
            if letter == char:
                x = index
        for index, char in enumerate(ROT13):
            if x == index:
                broken_code.append(char)     
    elif letter in alphabet_upper:
        for index, char in enumerate(alphabet_upper):
            if letter == char:
                x = index
        for index, char in enumerate(ROT13_upper):
            if x == index:
                broken_code.append(char)
    else:
        broken_code.append(letter)

print("".join(broken_code))
print()

