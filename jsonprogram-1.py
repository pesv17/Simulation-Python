import json
import Simsims



road1= Simsims.Road()
road2= Simsims.Road()
storage1 = Simsims.Storage()
storage2 = Simsims.Storage()
barn2 = Simsims.Barn()
barn1 = Simsims.Barn()

for i in range(10):
    road1._que.append(Simsims.Worker())
    barn1._que.append(Simsims.Food())
    barn2._que.append(Simsims.Food())
    storage1._que.append(Simsims.Product())
    storage2._que.append(Simsims.Product())

plclst = [road1,road2,barn1,barn2,storage1,storage2]

plant = Simsims.Plant(road1,road2,storage1)
cafeteria1 = Simsims.Cafeteria(road2,road1,barn1)
cafeteria2 = Simsims.Cafeteria(road1,road2,barn2)
field = Simsims.Field(road1,road2,barn1)
house1 = Simsims.House(road2,road1,storage1)
house2 = Simsims.House(road2,road1,storage2)


translst = [plant,cafeteria1,cafeteria2,field,house1,house2]

w1 = Simsims.worldmaker(translst,plclst)

data = w1.to_dict()
jsondata = json.dumps(data)


with open('simsims.json','w') as outfile:
    json.dump(data,outfile)



# road1= Simsims.Road()
# # road2= Simsims.Road()
# barn = Simsims.Barn()
# storage = Simsims.Storage()

# for i in range(3):
#     road1._que.append(Simsims.Worker())
#     # road2._que.append(Simsims.Worker())
#     barn._que.append(Simsims.Food())
#     storage._que.append(Simsims.Product())
# print(road1)
# # print(road2)
# plclst = [road1,barn,storage]
    
# cafeteria = Simsims.Cafeteria(road1,road1,barn)
# field = Simsims.Field(road1,road1,barn)
# house = Simsims.House(road1,road1,storage)
# plant = Simsims.Plant(road1,road1,storage)

# translst = [cafeteria,field,house,plant]


# w1 = Simsims.worldmaker(translst,plclst)

# # w1.simulate()

# data = w1.to_dict()
# jsondata = json.dumps(data)


# with open('simsims.json','w') as outfile:
#     json.dump(data,outfile)



#     # data = w1.to_dict()
#     # jsondata = json.dumps(data)
#     # print(jsondata)

# #   self._day_counter = 0

# # self._r1 = Road()
# # self._r2 = Road()
# # self._f1 = Field()
# # self._f1.set_roads(self._r1,self._r2)
# # self._b1 = Barn()
# # self._f1.set_barn(self._b1)
# # self._r1.add_to_places(Worker())
# # self._c1 = Cafeteria()
# # self._h1 = House()


# # self._s1 = Storage()
# # self._p1 = Plant()

# # self._p1.set_roads(self._r2,self._r1)
# # self._p1.set_storage(self._s1)

# # self._c1.set_roads(self._r1,self._r2)
# # self._c1.set_barn(self._b1)

# # self._h1.set_roads(self._r2,self._r1)
# # self._h1.set_storage(self._s1)

#     # self._day_counter = Days

#     #     self._r1 = Road().refactor(road1)
#     #     self._r2 = Road().refactor(road2)
#     #     self._f1 = Field()
#     #     self._f1.set_roads(self._r1,self._r2)
#     #     self._b1 = barn
#     #     self._f1.set_barn(self._b1)
#     #     self._r1.add_to_places(Worker())
#     #     self._c1 = Cafeteria()
#     #     self._h1 = House()
      

#     #     self._s1 = storage
#     #     self._p1 = Plant()
        
#     #     self._p1.set_roads(self._r2,self._r1)
#     #     self._p1.set_storage(self._s1)

#     #     self._c1.set_roads(self._r1,self._r2)
#     #     self._c1.set_barn(self._b1)

#     #     self._h1.set_roads(self._r2,self._r1)
#     #     self._h1.set_storage(self._s1)
