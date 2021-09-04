from cs50 import get_float
while True:

    x = get_float("Change owed: ")
    if x > 0:
        break

count = 0

while x>0.0010:
    if x >= 0.25:
        x = x-0.25
        count = count + 1
    elif x >= 0.10 and x < 0.25:
        x = x-0.10
        count = count + 1
    elif x >= 0.05 and x < 0.10:
        x = x-0.05
        count = count + 1
    elif x > 0 and x < 0.05:
        x = x-0.25
        count = count + 1

print(count)

