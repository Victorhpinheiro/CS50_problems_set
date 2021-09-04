s = input("Text: ")

spaces = 0
letters = 0
word = 1
sent = 0

for i in s:
    if i == " ":
        word = word + 1
        spaces = spaces + 1
    if i =="." or i == "!" or i =="?":
        sent = sent + 1

letters = len(s) - spaces - sent

L = (letters * 100)/word
S = (100 * sent)/word
ind = 0.0588*L - 0.296*S - 15.8

index = int(ind)

if ind < 2:
    print("Before Grade 1")
if ind > 16:
    print("Grade 16+")

if ind>2 and ind<16:
    print(f"Grade {index}")

