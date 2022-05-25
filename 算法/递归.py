def countdown(i):
    print(i)
    if i >= 0:
        countdown(i-1)

countdown(5)