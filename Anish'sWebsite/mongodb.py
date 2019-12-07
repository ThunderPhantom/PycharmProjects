import pymongo

client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
outer_space = client["outerspace"]
planets = outer_space.planets

planets.insert_one({'name': 'Earth', 'color': 'blue'})
planets.insert_many([{'name': 'Mars', 'color': 'red'}, {'name': 'Saturn', 'color': 'yellow'}, {'name': 'Pluto', 'color': 'brown'}])

#planets.update_many({'name: Earth'},{'$inc':{'count:2'}} )


for document in planets.find({}):
    print(document)
