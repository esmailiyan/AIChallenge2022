# Using readlines()
file = open('log.txt', 'r')
lines = file.readlines()
lines.sort()

# writing to file
file = open('log.txt', 'w')
file.writelines(lines)
file.close()