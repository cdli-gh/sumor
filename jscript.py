import json

dev = []
test = []
train = []

f = open('corp.json', 'r+')
data = json.load(f)

print("\n\nTRAIN\n\n")
for i in data[0]['entries']:
    train.append(i['CDLI no.'])
print(train)

print("\n\nTEST\n\n")
for i in data[1]['entries']:
    test.append(i['CDLI no.'])
print(test)

print("\n\nDEV\n\n")
for i in data[2]['entries']:
    dev.append(i['CDLI no.'])
print(dev)

f.close()
