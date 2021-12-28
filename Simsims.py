import random
import collections
from collections import deque
import json
import time

class Resource:

    """ Överklass för resurserna, innehåller virtuella metoder"""

    def __init__(self):
        pass
    
    def to_dict(self):
        pass
        
    @staticmethod
    def refactor(data):
        pass

class Place:

    """ Överklass för platserna, innehåller specifikt en klassmetod som ändrar placeid"""

    placeid = 0
    place_dic = {}
    def __init__(self,id):
        self._que = deque()

        if id != None:
            self.id= id
        else:
            self.id = Place.placeid
            Place.class_method()

    @classmethod
    def class_method(cls):
        cls.placeid += 1

    def __str__(self):
        return type(self).__name__+":"+str(len(self._que))
        
    def add_to_places(self,resource):
        self._que.append(resource)

    def remove_from_places_que(self):
        if len(self._que) != 0:
            return self._que.popleft()
        else:
            return 0
        
    def remove_from_places_stack(self):
        return self._que.pop()

    def get_que(self):
        return self._que

    def get_lengthsub(self):
        return ((len(self._que))*0.02)

    def to_dict(self):
        pass
        
    @staticmethod
    def refactor(data):
        pass

class Transition:

    """ Överklass för övergångarna"""

    def __init__(self,roadin,roadout):

        self._road_in = roadin
        self._road_out = roadout
    
    def simulate(self):
        pass

    def to_dict(self):
        pass
        
    @staticmethod
    def refactor(data):
        pass

class Worker(Resource):

    """ Arbetare, hanterar livskraften"""

    workerid = 0

    def __init__(self,lifeforce=None):
      
        super().__init__()
        if lifeforce != None:
            self._lifeforce = lifeforce
        else:
            self._lifeforce = 1.0
      
    def __str__(self):  
        return str(self._lifeforce)

    @property
    def get_lifeforce(self):
        return self._lifeforce

    def add_lifeforce(self,addition):
        old = self._lifeforce
        if old < 1:
            self._lifeforce = old + addition

    def sub_lifeforce(self,substraction):
        old = self._lifeforce
        if old >0:
            self._lifeforce = old - substraction

    def to_dict(self):
        return dict(lifeforce = self._lifeforce) 

    @staticmethod
    def refactor(data):
        return Worker(data["lifeforce"])
      
class Product(Resource):

    """Produkter. hanterar ett värde för kvaliteten på produkten"""

    def __init__(self):
        super().__init__()
        self._unique = random.randint(0,10)

    def to_dict(self):
        return dict(product = self._unique) 
    
    @staticmethod
    def refactor(data):
        return Product()

class Food(Resource):
    """ Mat, hanterar kvaliteten på matobjektet"""

    def __init__(self,qlt=None):
        super().__init__()
        if qlt != None:
            self._quality= qlt
        else:
            self._quality = round((random.random()),2)
    def __str__(self):
        return str(self._quality)
    
    def get_quality(self):
        return self._quality

    def to_dict(self):
        return dict(Food_quality = self._quality) 

    @staticmethod
    def refactor(data):
        return Food(data["Food_quality"])

class Road(Place): 

    """ Hanterar det som kan befinna sig på vägen """
  
    
    def __init__(self,id=None):
        super().__init__(id)

  
    def __str__(self):
        return type(self).__name__+":".join([str(pos) for pos in self._que])
    
    def to_dict(self):
        roadlst=[]
        for worker in self._que:
            roadlst.append(worker.to_dict())
        return dict(road=self.id,contents=roadlst,plctype="Road")

    @staticmethod
    def refactor(data):

        idplace = data["road"]

        if idplace in Place.place_dic.keys():
            return Place.place_dic[idplace]

        else:

            roadobj = Road(id=data["road"])
         
            for worker in data["contents"]:
                roadobj.add_to_places(Worker.refactor(worker))
            Place.place_dic[data["road"]]=roadobj
            return roadobj

class Storage(Place):
    """Fungerar som en stack av produkterna, sist in och först ut"""


    def __init__(self,id=None):
        super().__init__(id)




    def to_dict(self):
        storagelst=[]
        for product in self._que:
            storagelst.append(product.to_dict())
        return dict(storage=self.id,contents=storagelst,plctype="Storage")


    @staticmethod
    def refactor(data):
        
        idplace = data["storage"]

        if idplace in Place.place_dic.keys():
            return Place.place_dic[idplace]

        else:
            storageobj = Storage(id=data["storage"])
            for sto in data["contents"]:
                storageobj.add_to_places(Product.refactor(sto))
            Place.place_dic[data["storage"]]=storageobj
            return storageobj

class Barn(Place):
    """Fungerar så att först in först ut"""

    def __init__(self,id=None):
        super().__init__(id)

    def to_dict(self):
        barnlst=[]
        for food in self._que:
            barnlst.append(food.to_dict())
        return dict(barn=self.id,contents=barnlst,plctype="Barn")

    @staticmethod
    def refactor(data):

        idplace = data["barn"]

        if idplace in Place.place_dic.keys():
            return Place.place_dic[idplace]

        else:

            barnobj = Barn(id=data["barn"])
            for food in data["contents"]:
                barnobj.add_to_places(Food.refactor(food))
            Place.place_dic[data["barn"]]=barnobj
            return barnobj
    
class Field(Transition):
    """tar in en arbetare och returnerar en bit mat och en arbetare (ifall den överlever)"""

    transitionid = 0

    def __init__(self,roadin,roadout,barn,id=None):

        super().__init__(roadin,roadout)

        self._barn = barn

        if id != None:
            self.id= id
        else:
            self.id = Field.transitionid
            Field.class_method()
  
    @classmethod
    def class_method(cls):
        cls.transitionid += 1

    def simulate(self):
        
        if len(self._road_in.get_que()) != 0:

            accident = random.randint(0,100)
            created = Food()
            worker = self._road_in.remove_from_places_que()
          

            if accident < 95:

                self._road_out.add_to_places(worker)
                to_sub = self._road_out.get_lengthsub()
                worker.sub_lifeforce(to_sub)
                self._barn.add_to_places(created)

            else:
                self._barn.add_to_places(created)

    def set_barn(self,barn):
        self._barn = barn

    def to_dict(self):
        return dict(
            transition = "Field",
            transitionid = self.id,
            barn = self._barn.to_dict(), 
            roadin = self._road_in.to_dict(), 
            roadout=self._road_out.to_dict())
            
    @staticmethod
    def refactor(data):
        return Field(Road.refactor(data["roadin"]),Road.refactor(data["roadout"]),Barn.refactor(data["barn"]),data["transitionid"])
        
class Cafeteria(Transition):

    """ Låter arbetare äta och regenerera hälsa"""

    transitionid = 0

    def __init__(self,roadin,roadout,barn,id=None):
        super().__init__(roadin,roadout)
        self._barn = barn
        
        if id != None:
            self.id= id
        else:
            self.id = Cafeteria.transitionid
            Cafeteria.class_method()
        
  
    @classmethod
    def class_method(cls):
        cls.transitionid += 1

    def simulate(self):
      
        if len(self._road_in.get_que()) != 0 and len(self._barn.get_que()) != 0 :
            
            food = self._barn.remove_from_places_que()
            food_quality = food.get_quality()
            worker = self._road_in.remove_from_places_que()
            life_force = worker.get_lifeforce

            if food_quality >= 0.1:

                to_add = (1/life_force)
                worker.add_lifeforce(to_add)
                self._road_out.add_to_places(worker)
                to_sub = self._road_out.get_lengthsub()
                worker.sub_lifeforce(to_sub)
                return  
        
            else:

                to_sub = ((1/life_force)/2)
                worker.sub_lifeforce(to_sub)
                self._road_out.add_to_places(worker)
                to_sub = self._road_out.get_lengthsub()
                worker.sub_lifeforce(to_sub)
                return  
        else:
            return 
  
                    
    def set_barn(self,barn):
        self._barn = barn

    def to_dict(self):
        return dict(
            transition = "Cafeteria",
            transitionid = self.id,
            barn = self._barn.to_dict(),
            roadin = self._road_in.to_dict(),
            roadout=self._road_out.to_dict()) 

    @staticmethod
    def refactor(data):
        return Cafeteria(Road.refactor(data["roadin"]),Road.refactor(data["roadout"]),Barn.refactor(data["barn"]),data["transitionid"])

class Plant(Transition):

    """Tar in arbetare och tillverkar produkter"""

    transitionid = 0

    def __init__(self,roadin,roadout,storage,id=None):
        super().__init__(roadin,roadout)
        self._storage = storage
        
        if id != None:
            self.id= id
        else:
            self.id = Plant.transitionid
            Plant.class_method()
  
    @classmethod
    def class_method(cls):
        cls.transitionid += 1

    def simulate(self):
     
       
        if len(self._road_in.get_que()) != 0:
            
            accident = random.randint(0,100)
            stress = random.uniform(0,0.5)
            created = Product()
            worker = self._road_in.remove_from_places_que()
            time_consumption = None

            if accident < 30:
                
                # arbetaren kommer få lägre livskraft pga att de blir stressade
                worker.sub_lifeforce(stress)
                life_force = worker.get_lifeforce

                # De får även lägre livskraft för att det tar lång tid att producera, ju sämre de mår desto längre tid tar det.
                time_consumption = (worker.get_lifeforce)

                worker.sub_lifeforce(((1-(time_consumption)))*0.02)

                if life_force > 0 :

                    self._storage.add_to_places(created)
                    self._road_out.add_to_places(worker)
                    to_sub = self._road_out.get_lengthsub()
                    worker.sub_lifeforce(to_sub)
                    return
                else: 
                    self._storage.add_to_places(created)
                    return
            else:
                self._storage.add_to_places(created)
                return

        else:
            return 

    def set_storage(self,storage):
        self._storage = storage

    def to_dict(self):
        
        return dict(
            transition = "Plant",
            transitionid = self.id,
            storage = self._storage.to_dict(),
            roadin = self._road_in.to_dict(),
            roadout=self._road_out.to_dict()) 

    @staticmethod
    def refactor(data):
        return Plant(Road.refactor(data["roadin"]),Road.refactor(data["roadout"]),Storage.refactor(data["storage"]),data["transitionid"])
        
class House(Transition):

    """Tar in en eller två arbetare och returnerar beroende på olika fall"""
    transitionid = 0

    def __init__(self,roadin,roadout,storage,id=None):

        super().__init__(roadin,roadout)

        self._storage = storage

        if id != None:
            self.id= id
        else:
            self.id = House.transitionid
            House.class_method()

    @classmethod
    def class_method(cls):
        cls.transitionid += 1
        
    def simulate(self):

        
        if len((self._road_in.get_que())) != 0:
        
            fertility_rate = random.randint(0,20)
            worker = self._road_in.remove_from_places_que()
            life_force = worker.get_lifeforce

            if len(self._road_in.get_que()) < 2:
            
                if life_force > 1 :
                    self._road_out.add_to_places(worker)
                    to_sub = self._road_out.get_lengthsub()
                    worker.sub_lifeforce(to_sub)
                    return 
                else: 

                    to_add = ((1/life_force)/2)
                    worker.add_lifeforce(to_add)
                    self._road_out.add_to_places(worker)
                    to_sub = self._road_out.get_lengthsub()
                    worker.sub_lifeforce(to_sub)
                    return
            else:

                worker_2 = self._road_in.remove_from_places_que()
                worker_3 = Worker()

                if fertility_rate > 10:
                    self._road_out.add_to_places(worker)
                    self._road_out.add_to_places(worker_2)
                    self._road_out.add_to_places(worker_3)
                    to_sub = self._road_out.get_lengthsub()
                    worker.sub_lifeforce(to_sub)
                    worker_2.sub_lifeforce(to_sub)
                    worker_3.sub_lifeforce(to_sub)
                    return
                else:
                    self._road_out.add_to_places(worker)
                    self._road_out.add_to_places(worker_2)
                    to_sub = self._road_out.get_lengthsub()
                    worker.sub_lifeforce(to_sub)
                    worker_2.sub_lifeforce(to_sub)
                    return

    def set_storage(self,storage):
        self._storage = storage

    def to_dict(self):
    
        return dict(
            transition = "House",
            transitionid = self.id,
            storage = self._storage.to_dict(),
            roadin = self._road_in.to_dict(),
            roadout=self._road_out.to_dict()) 

    @staticmethod
    def refactor(data):
       
        return House(Road.refactor(data["roadin"]),Road.refactor(data["roadout"]),Storage.refactor(data["storage"]),data["transitionid"])

class worldmaker():

    """ Syr ihop världen och tar in det som ska göras om från JSON fil"""
    def __init__(self,transitions = [], places = []):
       
        self._transition_list = transitions
        self._place_list = places
     
     

    def simulate(self):

        number_of_workers = 1
        days = 0
       
        while number_of_workers != 0:
            time.sleep(0.2)
            
            number_of_workers = 0

            for trans in self._transition_list:
                
                trans.simulate()
                
                number_of_workers = sum([len(place._que) for place in self._place_list if isinstance(place,Road)]) 
            
            days += 1
            print("Counting number of days: " + str(days))

        print("The simulation lasted "+ str(days) + " days!")
          
                
                
    def str_to_obj(self,string):

        obj = None

        if string == "Field":
            obj = Field

        elif string == "House":
            obj = House
        
        elif string == "Cafeteria":
            obj = Cafeteria

        elif string == "Plant":
            obj = Plant
        
        elif string == "Road":
            obj = Road

        elif string == "Storage":
            obj = Storage

        elif string == "Barn":
            obj = Barn

        return obj


    def to_dict(self):
        transitionlist = []
        placelist= []

        for trans in self._transition_list:
            transitionlist.append(trans.to_dict())

        for place in self._place_list:
            placelist.append(place.to_dict())

        return dict(transitions = transitionlist, places = placelist)


    @staticmethod
    def refactor(data):
        world = worldmaker()
        
        for index,trans in enumerate(data["transitions"]):
            world._transition_list.append(world.str_to_obj(trans["transition"]).refactor(data["transitions"][index]))

        for index,place in enumerate(data["places"]):
            world._place_list.append(world.str_to_obj(place["plctype"]).refactor(data["places"][index]))

        return world

if __name__ == "__main__":
    

    with open('simsims.json') as json_file:
            
        data_read = json.load(json_file)
        w1 = worldmaker.refactor(data_read)
       
        w1.simulate()
