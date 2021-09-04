from cs50 import get_int

#ger height
while True:
    #x = int(input("Height: "))
    x = get_int("Height: ")
    if x > 0 and x<9:
        break

for i in range(x):
        print(" " * (x-i-1), end="")
        print("#" * (i+1), end="")
        print("  ", end="")
        print("#" * (i+1), end="")
        print()
