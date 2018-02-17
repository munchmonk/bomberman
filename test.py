try:
    a = 3 / 0
    print("success!")
except:
    print("failure...")


try:
    a = 3 / 0
except:
    pass
finally:
    print("yaya")