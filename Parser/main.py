from Parser import parser

champ = "Ла Лига"
home = "Барселона"
guest = "Валенсия"

res = parser(champ, home, guest)

# print(f"Барселона сыграла {res[4]} матчей, из них: {res[0]} домашних и {res[1]} гостевых\n"
#       f"Валенсия сыграла {res[5]} матчей, из них: {res[2]} домашних и {res[3]} гостевых")

print(res)