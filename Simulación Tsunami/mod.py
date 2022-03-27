# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 18:59:23 2022

@author: usuario
"""


from abc import ABC, abstractmethod
import copy
import random 
from random import sample



class AbstractEvent(ABC):

    @abstractmethod

    def execute(simulator): #AbstractSimulator

        pass



class OrderedSet(ABC):

    @abstractmethod

    def insert(x): #Comparable 

        pass

    @abstractmethod

    def removeFirst(): # return Comparable

        pass

    @abstractmethod

    def size(): # return int

        pass

    @abstractmethod

    def remove(x): # x is a Comparable, return a Comparable

        pass



class AbstractSimulator(object):

    def __init__(self):

        self.events = None

    def insert(self,e): #Insert an abstract event

        self.events.insert(e)
        #print("Nuevo evento insertado: {}".format(type(e)))

    def cancel(self,e): #AbstractEvent

        raise NotImplementedError("Method not implemented")

        

class Event(AbstractEvent,ABC):

    def __init__(self):

        self.time = None
        self.current_evacuated = None

    def __lt__(self,y):

        if isinstance(y,Event):

            return self.time < y.time

        else:

            raise ValueError('This is not an event')

    def __eq__(self, other) : 

        return self.__dict__ == other.__dict__

            

class Simulator(AbstractSimulator):

    def __init__(self):

        super().__init__()

        self.time = None
        self.cont = 0
        self.dir = None

    def now(self):

        return self.time

    def doAllEvents(self):
        import os

        #personas_servers = sum([self.servers[key].flow for key in self.servers])
        '''
        self.numero.append(0)

        self.kids.append(0)
        self.youngs.append(0)
        self.adults.append(0)
        self.elders.append(0)
        self.hombres.append(0)
        self.mujeres.append(0)

        self.instante.append(0)
        '''
        import copy
        tppo = 10
        
        import time
        inicio = time.time()
        act = 60
        while self.events.size()>0:
            #print("")
            #print("-----------------------EXECUTE---------------------------------------------------------------------------------------")
            e = self.events.removeFirst()
 
            self.time = e.time
            actual = time.time()
            
            if actual-inicio >= act:
                print('TIEMPO SIMULACIÓN: {},tiempo ejecución {}, evento: {}'.format(self.time,actual - inicio,type(e)))
                self.PlotResults()
                act += 60
                tppo += 10
                
            e.execute(self)
        
            if self.save== True:
              #self.plotEventStatus(e)
              self.plotEventStatus2(e)
              if self.verbose == True:
                self.StatusView('Running')
            

            # Estadisticas tipo de personas en el sistema, por instante de tiempo ( server flow per time)
            
            
            '''
            personas_servers = sum([self.servers[key].flow for key in self.servers]) 
            kids = sum([self.servers[key].capacity[e].kids_members for key in self.servers for e in self.servers[key].capacity ])
            youngs = sum([self.servers[key].capacity[e].youngs_members for key in self.servers for e in self.servers[key].capacity ])
            adults = sum([self.servers[key].capacity[e].adults_members for key in self.servers for e in self.servers[key].capacity ])
            elders = sum([self.servers[key].capacity[e].elders_members for key in self.servers for e in self.servers[key].capacity ])
            '''
            '''
            personas_servers = 100
            kids = 100
            youngs = 100
            adults = 100
            elders = 100
            '''
            '''
            self.numero.append(self.flujo_total)
            self.kids.append(self.flujo_kids)
            self.youngs.append(self.flujo_youngs)
            self.adults.append(self.flujo_adults)
            self.elders.append(self.flujo_elders)
            self.hombres.append(self.flujo_hombres)
            self.mujeres.append(self.flujo_mujeres)
            
            
   

            self.instante.append(self.time)
            '''
            # Estadisticas de 
            #self.Br.append(copy.deepcopy(self.B)) #diccionario con claves cada instante de tiempo
            #self.MPr.append(copy.deepcopy(self.MP))
            #self.serversr.append(copy.deepcopy(self.servers))  
            self.cont += 1
      


    def plotEventStatus(self,e):
        import matplotlib.pyplot as plt
        Servers = {self.servers[i].name : self.servers[i].flow for i in self.servers}
        Buildings = {self.B[i].name: self.B[i].flow for i in self.B}
        Meeting_Points = {self.MP[i].name:self.MP[i].flow for i in self.MP}
        data = dict(Meeting_Points,**dict(Buildings,**Servers))
        group_data = list(data.values())
        group_names = list(data.keys())
        group_mean = np.mean(group_data)
        #plt.title("Tsunami Evacuation Simulation, time: {}".format(self.now()))
        
        plt.style.use('fivethirtyeight')
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(group_names, group_data)
        labels = ax.get_xticklabels()
        
        if e.event_type == 'Street_Arrival':
          ax.set( xlabel='N° Familias',
          title="Tsunami Evacuation Simulation, time: {:.2f} \
           \n{} to server {}, destiny : {}".format(self.now(),e.entity.name, e.server, e.entity.destiny_choice ))
        elif e.event_type == "Shelter_Arrival":#e.type_event == 'Building_Arrival' or e.type_event == 'Meeting_Point_Arrival':
          ax.set( xlabel='N° Familias',
          title="Tsunami Evacuation Simulation, time: {:.2f} \
           \n{} to {} :{}".format(self.now(),e.entity.name, e.entity.destiny_choice , e.shelter))

        plt.xlim(0,20)
        #from os import system
        #system("clear")

        plt.close(fig)
        
        path = '/content/drive/MyDrive/MT/Código_simulación/Imagenes_gif_status/'
        
        fig.savefig(self.path + 'dir{}_escenario_{}/'.format(self.dir,self.scenario) + 'Status_{}.jpg'.format(self.cont), transparent=False, dpi=80,  bbox_inches="tight")
        
    def plotEventStatus2(self,e):
      #!pip install geopandas 
      import geopandas as gpd
      path = "/content/drive/MyDrive/MT/Código_simulación/Simulador_basico/shapefiles_codigo_oficial/"
      nodos = gpd.read_file(path + 'Antofa_nodes_of.shp')
      calles = gpd.read_file(path + 'Antofa_edges_of.shp')
            #!pip install contextily 
      from random import sample
      #nodos_11 = [4433,4799,1902] # ids Hogares , sacados de a mano de qgis
  
      #nodos_1 = nodos[nodos.new_id.isin(nodos_11)]
      
      print("Evento {} ejecutado, tiempo simulación: {}".format(self.cont,self.time))
      ids_servers = [self.edges_id_servers[self.servers[i].id] for i in self.servers]
      flow_servers = [self.servers[i].flow for i in self.servers]
      ids_b = [self.nodes_id_b[self.B[i].id] for i in self.B]
      flow_b = [self.B[i].flow for i in self.B]
      ids_mp = [self.nodes_id_mp[self.MP[i].id] for i in self.MP]
      flow_mp = [self.MP[i].flow for i in self.MP]

      #nodos_1 = nodos[nodos.new_id.isin(nodos_11)] #Hogares, se deja intacto el punto para graficar
      nodos_2 = nodos[nodos.new_id.isin(ids_b)] #Buildings, se añade la columna flow para visualizar estado
      nodos_2['flow'] = flow_b
      nodos_3 = nodos[nodos.new_id.isin(ids_mp)] # Meeting Points, se añade columna flow para visualizar estado
      nodos_3['flow'] = flow_mp
      print(ids_servers)
      print(flow_servers)
      calles_copy = calles[calles.new_id.isin(ids_servers)]
      for i,valor in enumerate(ids_servers): 
        calles_copy.loc[valor,'street_flow'] = flow_servers[i]
      #rom pyproj import CRS
      import matplotlib.pyplot as plt
      #import contextily as ctx
      #print("nodos crs:", CRS(nodos.crs).name)
      #print("calles crs:", CRS(nodos.crs).name)
      # Control figure size in here
      fig, ax = plt.subplots(figsize=(100,50))

      # Plot the data
      #nodos.plot(ax=ax,  color = 'red', alpha=0.4, legend = True)
      nodos_2.plot(ax=ax,  marker = 'o', markersize = 50,color = 'red')
      nodos_3.plot(ax=ax,  marker = 'o', markersize = 50,color = 'blue')
      calles_copy.plot(ax=ax, column='street_flow',cmap='OrRd', linewidth=10, alpha=0.99, legend = True)
      #nodos_1.plot(ax=ax, color='grey',marker = 'o',markersize = 20)
      
      plt.close(fig)
        
      path = '/content/drive/MyDrive/MT/Código_simulación/Imagenes_gif_status/'
      
      
      fig.savefig(path + 'dir{}_escenario_{}/'.format(self.dir,self.scenario) + 'Status_{}.jpg'.format(self.cont), transparent=False, dpi=80,  bbox_inches="tight")
      
    def CreateGif(self):

        import os
        import imageio

        # Ubicación de la base de datos
        
        import imageio
        images = []
        filenames = ['Status_{}.jpg'.format(i) for i in range(self.cont)]
        for filename in filenames:
            images.append(imageio.imread(self.path + 'dir{}_escenario_{}/'.format(self.dir,self.scenario) + filename))
        imageio.mimsave(self.path + 'dir{}_escenario_{}/'.format(self.dir,self.scenario) + 'Simulation_{}.gif'.format(self.scenario), images)

class ListQueue(OrderedSet):

    elements = list()

    def insert(self,x):

        i=0

        while i < len(self.elements) and self.elements[i] < x:

            i += 1

        self.elements.insert(i,x)

    def removeFirst(self):

        if len(self.elements) == 0:

            return None

        x = self.elements.pop(0)

        return x

    def remove(self,x):

        for i in range(len(self.elements)):

            if self.elements[i] == x:

                return self.elements.pop(i)

        return None

    def size(self):

        return len(self.elements)

class SimulationEntity(ABC):

    NumberOfEntities = 0

    def __init__(self, name=None):

        SimulationEntity.NumberOfEntities += 1

        self.name = name
        if name is None:
            self.name = 'Entity {}'.format(SimulationEntity.NumberOfEntities)
    
    def __str__(self):
        return self.name

import numpy as np       

class Random(object):

    def __init__(self):

        pass

    @staticmethod

    def exponential(mean):

        return -mean*np.log(np.random.rand())

    @staticmethod

    def bernulli(p):

        return np.random.rand() < p



        
                
 
 

class Street_Arrival(Event):

    # time, name
   def __init__(self,
                entity: object,
                server: str,
                time : float,
                name: str = None):
     
     super().__init__()
     self.entity = entity
     self.name = entity.name
     self.time = time
     self.server = server
     self.previous_server = None 
     self.event_type = "Street_Arrival"
 
   def execute(self,simulator):
        
        # servidor actual , actualizado previamente 
        #print('Person {} has arrived at time {:.2f} in {}'.format(self.entity.name, self.time,simulator.servers[self.server].name)) ################################
    
        # DEF UPDATE SERVER
        self.getIn(simulator, self.server)
      
        #print('Flow street: {}'.format(simulator.servers[self.server].flow))
        #print('Flow street (len capacity): {}'.format(simulator.servers[self.server].flow))
        
        # DEFINIR TIEMPO EVACUACIÓN 
        
        evacuation_street_time = self.calculateStreetTime(simulator)

        #print("Family_velocity: {}".format(self.entity.family_street_velocity))
        #print("Time in {} : {}".format(simulator.servers[self.server].name,evacuation_street_time))
        #print("Simulation time: {}".format(simulator.now()))
        #return
        #print("----------------------------------------------------------------------------------------------------------------------------------------")
        
        # DEFINIR MOMENTO INICIO PRÓXIMO EVENTO
        time = simulator.now() + evacuation_street_time # tiempo en que finaliza evento actual y comienza evento posterior.
        # Proximo evento se retira entidad del server actual, ya que ingresa a nuevo server o shelter
        ############################################################################################################################3
        #            STREET ARRIVAL
        #print(len(self.entity.route[self.entity.destiny_choice]) > 1 ,self.entity.route[self.entity.destiny_choice] )
        if len(self.entity.route[self.entity.destiny_choice]) > 1 : # Street Arrival, quedan servers por recorrer, se podria preguntar de otra forma...

          # DEF INSERTAR PROXIMO EVENTO street arrival
          self.insert(simulator,time, 'Street_Arrival')
          
          if self.previous_server != None: # Actualiza server anterior (familia sale de la calle anterior)

             # UPDATE SERVER
             self.getOut(simulator, self.previous_server)

          elif self.previous_server == None:

             pass
          else:
            pass 
 

        ##############################################################################################################################################################
        #             NEXT SHELTER ARRIVAL 
        else:
          #print('HOLAAAAAAAAAAA')
          #print(self.previous_server)
          if self.previous_server != None: # Actualiza server anterior (familia sale de la calle anterior)

            self.getOut(simulator, self.previous_server)
          else:
            pass
          self.insert(simulator,time, 'Shelter_Arrival')
          



    

        

   def isAvailable(self):

      return self.__current_evacuated == None

   def insert(self,simulator,time,type_event): # server.insert (del generador) o self.server (del mismo server)

      if type_event == 'Street_Arrival':
        next_street = self.entity.route[self.entity.destiny_choice].pop(0) ##
        actual_street = copy.copy(self.server)
        street_arrival_event = Street_Arrival(self.entity,next_street,time)
        street_arrival_event.previous_server = actual_street
        simulator.insert(street_arrival_event)
        #print("Street Arrival event insert, ruta hacia {}".format(self.entity.destiny_choice))

      elif type_event == 'Shelter_Arrival':

        #print("Abandona última calle")
        #print(self.entity.route[self.entity.destiny_choice], self.entity.name)
        next_shelter = self.entity.route[self.entity.destiny_choice].pop(0) ## MODIFICAR PARA BUILDINGS Y MEETING POINTS
        #print('ruta {}, shelter n°: {}'.format(self.entity.destiny_choice,next_shelter))
        actual_street = copy.copy(self.server)
        shelter_arrival_event = Shelter_Arrival(self.entity,next_shelter,actual_street,time)
        simulator.insert(shelter_arrival_event)
        #print("Shelter Arrival event insert")


   def getIn(self, simulator,server): # INGRESA A FAMILIA EN EL SERVIDOR
      simulator.servers[server].capacity[self.entity] = self.entity # Actualiza a familia en el servidor
      #simulator.servers[server].flow = len(simulator.servers[server].capacity)
      simulator.servers[server].flow += self.entity.total_members
      #Actualizar flujto total por calle
      simulator.servers2[server].flow += self.entity.total_members
      
      
      #Agregar flujo de personas desglosados para calcular numero personas promedio en el sistema
      '''
      simulator.flujo_total += self.entity.total_members
      simulator.flujo_kids += self.entity.kids_members
      simulator.flujo_youngs += self.entity.youngs_members
      simulator.flujo_adults += self.entity.adults_members
      simulator.flujo_elders += self.entity.elders_members
      simulator.flujo_hombres += self.entity.m
      simulator.flujo_mujeres += self.entity.w
      '''
      
     
      
   def getOut(self, simulator, server): # SALE FAMILIA DEL SERVIDOR
      simulator.servers[self.previous_server].capacity.pop(self.entity) # Elimina entidad del server anterior 
      #simulator.servers[self.previous_server].flow = len(simulator.servers[self.previous_server].capacity) # Agregar como directo de servers
      simulator.servers[server].flow -= self.entity.total_members
      '''
      # Quitar personas de la calle
      simulator.flujo_total -= self.entity.total_members
      simulator.flujo_kids -= self.entity.kids_members
      simulator.flujo_youngs -= self.entity.youngs_members
      simulator.flujo_adults -= self.entity.adults_members
      simulator.flujo_elders -= self.entity.elders_members
      simulator.flujo_hombres -= self.entity.m
      simulator.flujo_mujeres -= self.entity.w
      '''
      
   def calculateStreetTime(self, simulator):
      if pppp == 'MOD':
        limitt = 0.6
      else:
        limitt = LIMIT
      if simulator.servers[self.server].flow > simulator.servers[self.server].street_capacity:
        v = limitt
        
      else:
        v = self.entity.family_street_velocity # No modificar, solo utilizar para calcular tiempo evacuacion
      
      l = simulator.servers[self.server].length
      evacuation_street_time = l/v 
      return evacuation_street_time

class Shelter_Arrival(Event): 
      # time, name
   def __init__(self,
                entity: object,
                shelter: str, #next shelter
                previous_server: str, # actual street (previous arrival shelter)
                time : float,
                name: str = None):
     
     super().__init__()
     self.entity = entity
     self.name = entity.name
     self.time = time
     self.shelter = shelter
     self.previous_server = previous_server
     self.event_type = "Shelter_Arrival"
     self.server = None
 
   def execute(self,simulator):


        # ACTUALIZACION SERVERS PREVIOS A LLEGADA DE REFUGIO, SE VACIAN
        if self.previous_server == None:
          pass
        else:
          self.getOut(simulator,self.previous_server)
        
        if  self.entity.destiny_choice == 'MP' or self.entity.destiny_choice == 'B-MP' : # Caso H --> MP
          #print('Person {} has arrived to {} at time {:.2f}'.format(self.entity.name,simulator.MP[self.shelter].name, self.time))
          #Actualizar capacidad shelter
          # GetIn Shelter MP
          self.getIn(simulator,self.shelter,simulator.MP)
          #print(self.entity.o_d)
          '''
          for i in range(self.entity.total_members):
              simulator.evacuation_times.append([self.time,'MP',self.entity.o_d])
              if i < self.entity.kids_members:
                simulator.evacuation_times_kids.append([self.time,'MP',self.entity.o_d])
              if i < self.entity.youngs_members:
                simulator.evacuation_times_youngs.append([self.time,'MP',self.entity.o_d])
              if i < self.entity.adults_members:
                simulator.evacuation_times_adults.append([self.time,'MP',self.entity.o_d])
              if i < self.entity.elders_members:
                simulator.evacuation_times_elders.append([self.time,'MP',self.entity.o_d])
          '''

          #print('People in shelter: {}'.format(simulator.MP[self.shelter].flow))
          #print('People in shelter(len capacity): {}'.format(simulator.MP[self.shelter].flow))
         
          #print("Simulation time: {}".format(simulator.now()))
          #print("----------------------------------------------------------------------------------------------------------------------------------------")

        elif self.entity.destiny_choice == 'B':  # Caso H --> B
          if simulator.B[self.shelter].max_capacity >= simulator.B[self.shelter].flow + self.entity.total_members: # Si B tiene capacidad disponible, se debe considerar que tenga capacidad disponible para TODA la familia, caso contrario se van
            #print('Person {} has arrived to {} at time {:.2f}'.format(self.entity.name,simulator.B[self.shelter].name, self.time))
            #Actualizar capacidad shelter
            # GetIn Shelter B
            self.getIn(simulator,self.shelter,simulator.B)
            
            '''
            for i in range(self.entity.total_members):
              simulator.evacuation_times.append([self.time,'B',self.entity.o_d])
              if i < self.entity.kids_members:
                simulator.evacuation_times_kids.append([self.time,'B',self.entity.o_d])
              if i < self.entity.youngs_members:
                simulator.evacuation_times_youngs.append([self.time,'B',self.entity.o_d])
              if i < self.entity.adults_members:
                simulator.evacuation_times_adults.append([self.time,'B',self.entity.o_d])
              if i < self.entity.elders_members:
                simulator.evacuation_times_elders.append([self.time,'B',self.entity.o_d])
            #print('People in shelter: {}'.format(simulator.B[self.shelter].flow))
            #print('People in shelter(len capacity): {}'.format(simulator.B[self.shelter].flow))
            #print("Simulation time: {}".format(simulator.now()))
            #print("----------------------------------------------------------------------------------------------------------------------------------------")
            '''
          else: # Si edificio está con capacidad máxima, familia toma ruta B --> MP
            #print("Edificio lleno, Street Arrival event insert ")
            # INSERT STREET ARRIVAL EVENT FROM BUILDING
            self.insert(simulator, 'Street_Arrival')
            #print("----------------------------------------------------------------------------------------------------------------------------------------")
          
   def getIn(self, simulator,server,shelter): # INGRESA A FAMILIA EN EL SERVIDOR
      import copy
      self.entity.final_time = copy.copy(self.time)
      shelter[self.shelter].capacity[self.entity] = self.entity
      #shelter[self.shelter].flow = len(shelter[self.shelter].capacity)
      shelter[self.shelter].flow += self.entity.total_members
      
      #Actualiza flujo por calle (total)
      simulator.servers2[server].flow += self.entity.total_members
      
      # NUEVO!! INGRESAR ENTIDADES DE PERSONAS EN UNA LISTA, PARA GUARDAR DATOS EN CSV DESPUÉS!
      self.entity.id_destiny = self.shelter
      shelter[self.shelter].entidades.append(self.entity)
  
   def getOut(self, simulator, server): # SALE FAMILIA DEL SERVIDOR
      simulator.servers[self.previous_server].capacity.pop(self.entity) # Elimina entidad del server anterior 
      simulator.servers[self.previous_server].flow = len(simulator.servers[self.previous_server].capacity) # Agregar como directo de servers
      
      '''
      # Quitar personas de la calle
      simulator.flujo_total -= self.entity.total_members
      simulator.flujo_kids -= self.entity.kids_members
      simulator.flujo_youngs -= self.entity.youngs_members
      simulator.flujo_adults -= self.entity.adults_members
      simulator.flujo_elders -= self.entity.elders_members
      simulator.flujo_hombres -= self.entity.m
      simulator.flujo_mujeres -= self.entity.w
      '''
      
   def insert(self,simulator,type_event):
      next_street = self.entity.route['B-MP'].pop(0) 
      # Actualiza la nueva ruta de escape, que en este caso es desde el edificio hacia el punto de encuentro más cercano
      self.entity.destiny_choice = 'B-MP'
      #actual_street = copy.copy(self.server) 
      time_evacuation_street = 0 # no hay tiempo de evacuación , pasa directo de edificio lleno a calle adyacente
      time = simulator.now() + time_evacuation_street # De pasar del nodo edificio a la calle adyacente se considera que no pasa tiempo,
      street_arrival_event = Street_Arrival(self.entity,next_street,time)
      street_arrival_event.previous_server = None # Ya se eliminó la familia del server anterior, por lo que no se asigna ningún server previo para que no elimine la misma familia en dicho server
      simulator.insert(street_arrival_event)



class Server_:
  id = 0
  def __init__(self,length,width):
    #super().__init__()
    self.capacity = {}
    self.flow = 0
    self.name = 'Street_{}'.format(Server_.id)
    #self.max_capacity = C
    self.arrival_time = None
    self.length = length
    self.width = width
    #self.street_capacity = SC
    self.street_capacity = (length * width)*1.55
    self.id = Server_.id
    Server_.id += 1
  
  #def update(self):


class Shelter_:
  id = 0
  def __init__(self):
    #super().__init__()
    self.capacity = {}
    self.flow = None
    self.max_capacity = None
    self.name = None
    self.type_ = None
    self.entidades = []
    Shelter_.id += 1

class Building_(Shelter_):
  id = 0
  def __init__(self,capacity):
    super().__init__()
    self.capacity = {}
    self.flow = 0
    self.max_capacity = capacity
    self.name = 'B_{}'.format(Building_.id)
    self.type_ = None
    self.id = Building_.id
    Building_.id += 1

class Meeting_Point_(Shelter_):
  id = 0
  def __init__(self):
    super().__init__()
    self.capacity = {}
    self.flow = 0
    self.max_capacity = 10000000
    self.name = 'MP_{}'.format(Meeting_Point_.id)
    self.type_ = None
    self.id = Meeting_Point_.id
    Meeting_Point_.id += 1

       
class Entity(SimulationEntity):
  Total_evacuated = 0
  Building_evacuated = 0
  Meeting_points_evacuated = 0
  velocity_factors = None
  delay_probabilities = None
  time_in_minutes = None # parametros simulador
  #escenario = 2 # Parámetro simulador 1,2 o3 # parámetro simulador
  id = 0

  def __init__(self,a,b,c,d,node_id,m,w,o_d,o,depto,route,destiny_choice,*args):
    super().__init__(*args)
    pppp = 'MOD'
    Entity.id += 1
    self.id = Entity.id
    self.kids_members = a
    self.youngs_members = b
    self.adults_members = c
    self.elders_members = d
    self.node_id = node_id
    self.m = m # hombres
    self.w = w # mujeres
    if pppp == 'MOD':
      self.o_d = o_d
      self.o = o
      self.DEPTO = depto
    else:
      self.o_d = None
      self.o = None
      self.DEPTO = None
    self.route = route
    self.distances = None
    if self.o_d == 'estudio' or self.o_d == 'otros' or self.o == '12'   : # cualquiera de estas significa que se movieron, el 12 en particular que vienen desde fuera
        self.destiny_choice = 'MP'
    else:
        self.destiny_choice = destiny_choice
    self.name = args[0]
    self.previous_server = None
    self.actual_server = None
   
    self.family_type = ['a' if (members[0] == 0 and members[1] == 0) else 'b' if (members[0] > 0 and members[1]==0) 
                               else 'c' if (members[0] == 0 and members[1] > 0) else 'd' if (members[0] > 0 and members[1]>0) else 'indefinido' 
                               for members in [(self.kids_members,self.elders_members)]][0]
    #self.route_choice = [destiny if (Entity.escenario == 3 or Entity.escenario == 2) else [destiny[1]] if Entity.escenario == 1 else 'indefinido' for destiny in [['B','MP']]][0]
    self.delay_probabilities_ = Entity.delay_probabilities[self.family_type]
    self.delay_start = random.choice(np.concatenate([[e] * int(p*100) for e,p in zip(Entity.time_in_minutes,self.delay_probabilities_)] ).tolist()) * 60
    self.total_members = self.kids_members + self.youngs_members + self.adults_members + self.elders_members
    #self.ruta_mas_corta_B = sample(['{}'.format(x) for x in range(S)],R) + ['{}'.format(random.choice([i for i in range(B)]))]
    #self.ruta_mas_corta_MP = sample(['{}'.format(x) for x in range(S)],R) + ['{}'.format(random.choice([i for i in range(MP)]))]
    #self.ruta_mas_corta_B_MP = sample(['{}'.format(x) for x in range(S)],R) + ['{}'.format(random.choice([i for i in range(MP)]))]
    ############################
    #  Utilizar con muestra pequeña real de rutas a edificios y mp
    self.ruta_mas_corta_B = []
    self.ruta_mas_corta_MP = []
    self.ruta_mas_corta_B_MP = []
    #self.ruta_mas_corta_MP = sample( ['{}'.format(x) for x in range(S)],R) + ['{}'.format(random.choice([i for i in range(MP)] ) ) ]
    #self.ruta_mas_corta_B_MP = sample(['{}'.format(x) for x in range(S)],R) + ['{}'.format(random.choice([i for i in range(MP)]))]
    #############################
    # SELF.ROUTE ES LA QUE SE USA, ESTA HAY QUE INGRESAR DESDE EL INPUT, JUNTO CON DESTINY CHOICE
    #self.route = {'B':self.ruta_mas_corta_B[:],'MP':self.ruta_mas_corta_MP[:],'B-MP':self.ruta_mas_corta_B_MP[:]}
    self.route = {'B':route[0],'MP':route[1],'B-MP':route[2]}
    self.route_original = self.route.copy() 
    #self.ruta_mas_corta_original = self.ruta_mas_corta[:]
    self.origin_node = None
    self.destiny_node = None
    self.family_street_velocity = ((self.kids_members*Entity.velocity_factors[0] + self.youngs_members*Entity.velocity_factors[1] + self.adults_members*Entity.velocity_factors[2] + self.elders_members*Entity.velocity_factors[3])/(self.total_members))
    if pppp == 'MOD' and self.o_d == 'estudio':
      self.family_street_velocity = 0.4
    if pppp == 'MOD' and (self.o_d == 'trabajo' or self.o_d == 'otros'):
      self.delay_start = 0.001
    if self.DEPTO == 1 and self.o_d == False: # ASIGNAR A EDIFICIO EN INSTANTE 0
      self.delay_start = 0
    #self.destiny_choice = random.choice(['B' for i in range(P)]+['MP' for i in range(100 - P)])
    self.destiny_choice = destiny_choice
    self.final_time = None
    self.id_destiny = None
  


  def initializeParameters(self,delay_probabilities,velocity_factors,time_in_minutes):
    Entity.delay_probabilities = delay_probabilities
    Entity.velocity_factors = velocity_factors
    Entity.time_in_minutes = time_in_minutes
  
  def updateNewIds(self,sim,i):
    if self.destiny_choice == 'B':
      self.ruta_mas_corta_B = list(map(lambda x: sim.edges_id_servers.index(x),sim.rutas[i][0][:-2])) + list(map(lambda x: sim.nodes_id_b.index(x),sim.rutas[i][0][-2:-1])) # Transforma a nuevos indices
      #self.ruta_mas_corta_MP = list(map(lambda x: sim.edges_id_servers.index(x),sim.rutas[i][1][:-2])) + list(map(lambda x: sim.nodes_id_mp.index(x),sim.rutas[i][1][-2:-1]))# Transforma a nuevos indices
      self.ruta_mas_corta_B_MP = list(map(lambda x: sim.edges_id_servers.index(x),sim.rutas[i][2][:-2])) + list(map(lambda x: sim.nodes_id_mp.index(x),sim.rutas[i][2][-2:-1]))# Transforma a nuevos indices
      self.route = {'B':self.ruta_mas_corta_B[:],'MP':self.ruta_mas_corta_MP[:],'B-MP':self.ruta_mas_corta_B_MP[:]}
      #print('Familia {}, rutas new ids :{}'.format(self.id-1,self.route))
      self.route_original = copy.deepcopy(self.route)
    elif self.destiny_choice == 'MP':
      #self.ruta_mas_corta_B = list(map(lambda x: sim.edges_id_servers.index(x),sim.rutas[i][0][:-2])) + list(map(lambda x: sim.nodes_id_b.index(x),sim.rutas[i][0][-2:-1])) # Transforma a nuevos indices
      self.ruta_mas_corta_MP = list(map(lambda x: sim.edges_id_servers.index(x),sim.rutas[i][1][:-2])) + list(map(lambda x: sim.nodes_id_mp.index(x),sim.rutas[i][1][-2:-1]))# Transforma a nuevos indices
      self.ruta_mas_corta_B_MP = list(map(lambda x: sim.edges_id_servers.index(x),sim.rutas[i][2][:-2])) + list(map(lambda x: sim.nodes_id_mp.index(x),sim.rutas[i][2][-2:-1]))# Transforma a nuevos indices
      self.route = {'B':self.ruta_mas_corta_B[:],'MP':self.ruta_mas_corta_MP[:],'B-MP':self.ruta_mas_corta_B_MP[:]}
      #print('Familia {}, rutas new ids :{}'.format(self.id-1,self.route))
      self.route_original = copy.deepcopy(self.route)

    
class SimParameters():
  def __init__(self,scenario,rutas,distance_rutas,delay_probabilities,velocity_factors,time_in_minutes,poblacionSintetica = None ,Antofagasta = None, replica = None):
    self.scenario = scenario
    self.replica = replica
    # shelter and server generator parameters
    self.rutas = rutas
    self.destiny = None
    self.max_capacity_b = 10 
    self.distance_rutas = distance_rutas #[[30,20,50], [23,45,65],...] -->[[B_1,MP_1,B-MP_1][B_2,MP_2,B-MP_2],...]--> [[FAMILY 1], [FAMILY 2], ...]


    # initial events generator parameters
    self.delay_probabilities = delay_probabilities #Entity.delay_probabilities = 
    self.time_in_minutes = time_in_minutes #Entity.time_in_minutes = 
    self.entities_list = None # events generator input
    self.velocity_factors = velocity_factors

    # Optimization model parameters
    #self.H_B_4 = H_B_4
    #self.H_MP_1 = H_MP_3
    # BDij, Matriz distancias hogar i a edificio j: se obtiene de H_B_4

    #self.BDi11 = {origen:H_B_4[origen][0][0] for origen in H_B_4 }
    #self.BDi22 = {origen:H_B_4[origen][1][0] for origen in H_B_4 }
    #self.BDi33 = {origen:H_B_4[origen][2][0] for origen in H_B_4 }
    #self.BDi44 = {origen:H_B_4[origen][3][0] for origen in H_B_4 }
    self.BDi1 = None
    self.BDi2 = None
    self.BDi3 = None 
    self.BDi4 = None

    # BDij, matriz general
    #self.BDiijj = {origen:[i[0] for i in H_B_4[origen]] for origen in H_B_4 }
    self.BDij = None
    # NMi
    self.NMi = None
    # CBj, de momento 400 para todos
    self.CBj = 600
    # MD, maxima distancia
    self.MD = 200
    # Weigths elders,adults,kids
    self.WE = 10
    self.WK = 5
    self.WA = 2
    # elders,adults,kids
    self.ELDERS = None
    self.KIDS = None
    self.ADULTS = None

    #restricciones distancias b>mp
    self.rest = [0]#restt


    #solutions cplex : asignaciones xij .
    self.h_b = None # rutas 4 edificios para cada  familia
    self.b_mp = None # rutas 4 edificios más cercanos a puntos de encuentro para cada familia
    self.solutions = None
  



    
    self.poblacionSintetica = poblacionSintetica #GeoDF se utiliza para crear la lista de entidades en esta clase 
    self.Antofagasta = Antofagasta # GeoDF se utiliza para agregar atributos a servers y shelters

  def createNMi(self):
    self.createScenario()
    self.NMi = [e.total_members  for e in self.entities_list ]
    self.ELDERS = [e.elders_members  for e in self.entities_list ]
    self.KIDS = [e.kids_members  for e in self.entities_list ]
    self.ADULTS = [e.adults_members  for e in self.entities_list ]
    #self.BDi1 = [self.BDi11[e.node_id]  for e in self.entities_list ]
    #self.BDi2 = [self.BDi22[e.node_id]  for e in self.entities_list ]
    #self.BDi3 = [self.BDi33[e.node_id]  for e in self.entities_list ]
    #self.BDi4 = [self.BDi44[e.node_id]  for e in self.entities_list ]
    self.BDij = [self.BDiijj[e.node_id]  for e in self.entities_list ]

  def createScenario(self):

    if self.scenario == 1:
      self.destiny = ['MP' for i in range(len(self.rutas))] # mejorable, no es necesario tener toda la lista con los mismos strings
      self.createEntityList(self.scenario) # all population?

      
    elif self.scenario == 2:

      self.max_capacity_b = C
      probabilistic_choice_b = [self.distance_rutas[i][1]/(self.distance_rutas[i][0] + self.distance_rutas[i][1]) for i in range(len(self.rutas)) ]
      probabilistic_choice_mp = [self.distance_rutas[i][0]/(self.distance_rutas[i][0] + self.distance_rutas[i][1]) for i in range(len(self.rutas)) ]
      
      # Valores inf en distancias. Eliminar son solo 4. esto va a eliminar a todas las familias asociadas a esos 4 nodos
      #for i in range(len(self.rutas)):
      #  print(self.distance_rutas[i][1],self.distance_rutas[i][0] )
      #  if np.isinf(self.distance_rutas[i][1]) == True or np.isinf(self.distance_rutas[i][0]) == True :
      #    print('Nan Value')

      #self.calculateDestinyChoices(probabilistic_choice_b,probabilistic_choice_mp,0.85)
      self.calculateDestinyChoices(probabilistic_choice_b,probabilistic_choice_mp,0.50,False) # Selecciona los destinos más cercanos para cada familia, B o MP
      self.calculateDestinyChoices(probabilistic_choice_b,probabilistic_choice_mp,0.85,True) # Estocasticidad a personas cercanas a edificio

      # Modificar decisiones de B y cambiar por estocasticidad dependiendo de distancias y relación de distancia MP
      #self.destiny = [self.calculateChoice(b,mp,p) for  b,mp in probabilities]

      self.createEntityList(self.scenario) # solo poblacion cercana a edificios o todos? tiene sentido todos porque la decision probabilistica se basa en la distancia, por lo que si están lejos de buildings van a mp caso contrario van a buildings

    elif self.scenario == 3:
      #self.destiny = ['B' for i in range(len(self.rutas))] # mejorable, no es necesario tener toda la lista con los mismos strings
      #self.max_capacity = 10000000
      #self.createEntityList(self.scenario) # solo población cercana a edificios!

      self.max_capacity_b = C
      probabilistic_choice_b = [self.distance_rutas[i][1]/(self.distance_rutas[i][0] + self.distance_rutas[i][1]) for i in range(len(self.rutas)) ]
      probabilistic_choice_mp = [self.distance_rutas[i][0]/(self.distance_rutas[i][0] + self.distance_rutas[i][1]) for i in range(len(self.rutas)) ]
      
      # Valores inf en distancias. Eliminar son solo 4. esto va a eliminar a todas las familias asociadas a esos 4 nodos
      #for i in range(len(self.rutas)):
      #  print(self.distance_rutas[i][1],self.distance_rutas[i][0] )
      #  if np.isinf(self.distance_rutas[i][1]) == True or np.isinf(self.distance_rutas[i][0]) == True :
      #    print('Nan Value')

      self.calculateDestinyChoices(probabilistic_choice_b,probabilistic_choice_mp,0.50,False) # Selecciona los destinos más cercanos para cada familia, B o MP
      print('')
      print(self.destiny.count('B'),self.destiny.count('MP'))
      print('')
      # Optimization Model: Asignación de familias con niños y adultos mayores a edificios como prioridad
      self.createEntityList(self.scenario) 

    elif self.scenario == 4:
      self.destiny = destiny_ # optimization model cplex
      print('')
      print(self.destiny.count('B'),self.destiny.count('MP'))
      print('')
      self.createEntityList(self.scenario) 


  

  def selectBuildingsRoutes(self):
      #print(len(self.distance_rutas))
      self.entities_list = [entitie for i,entitie in enumerate(self.entities_list) if self.destiny[i] == 'B']
      self.rutas = [ruta for i,ruta in enumerate(self.rutas) if self.destiny[i] == 'B']
      self.distance_rutas = [distances for i,distances in enumerate(self.distance_rutas) if self.destiny[i]== 'B' ]
      print(self.destiny)
      self.destiny = [destiny for destiny in self.destiny if destiny =='B']
      print(self.destiny)
      

  def calculateDestinyChoices(self,probabilistic_choice_b,probabilistic_choice_mp,p,subset):
     
      probabilities = list(zip(probabilistic_choice_b,probabilistic_choice_mp))
      #for b,m in probabilities:
       #print(type(b),b,type(m),m)
      if subset == False: 
        self.destiny = [self.calculateChoice(b,mp,p) for  b,mp in probabilities]
      elif subset == True:
        self.destiny = [self.calculateChoice(b,mp,p) if self.destiny[i] == 'B' else 'MP' for  i,(b,mp) in enumerate(probabilities)] # subset de familias cercanas a edificios, estocasticidad en esa desicion

  
  def calculateChoice(self,b_,mp_,p):
    if b_ > p:
      destiny = 'B'
    elif mp_ > p:
      destiny = 'MP'
    else:
      #print(b_*100)
      P = int(b_*100) # Porbabilidad de elegir B, caso contrario elige MP
      destiny = random.choice(['B' for i in range(P)]+['MP' for i in range(100 - P)])
    return destiny

  
  def createEntityList(self,scenario):

    #Entity.delay_probabilities = self.delay_probabilities
    #Entity.velocity_factors = self.velocity_factors
    #Entity.time_in_minutes = self.time_in_minutes
    #print(self.delay_probabilities,self.velocity_factors,self.time_in_minutes)

    Entity.initializeParameters(self,delay_probabilities = self.delay_probabilities, velocity_factors = self.velocity_factors, time_in_minutes= self.time_in_minutes)
    Poblacion = self.poblacionSintetica
    N = Poblacion.shape[0]
    
    # De momento esto, esto corresponde a atributos de la población sintética
    a,b,c,d,node_ids,m,w  = Poblacion['EDAD_0A5'].tolist(),Poblacion['EDAD_6A14'].tolist(),Poblacion['EDAD_15A64'].tolist(),Poblacion['EDAD_65YMA'].tolist(),Poblacion['new_id'].tolist(),Poblacion['HOMBRES'].tolist() ,Poblacion['MUJERES'].tolist()
    
    o_d,o ,depto = Poblacion['o_d'].tolist(),Poblacion['o'].tolist(),Poblacion['DEPTO'].tolist()
    #a,b,c,d = a[:N],b[:N],c[:N],d[:N]
    #a = [random.randint(0,1) for i in range(N)] #kids
    #b = [random.randint(1,6) for i in range(N)] #youngs
    #c = [random.randint(1,6) for i in range(N)] #adults
    #d = [random.randint(0,1) for i in range(N)] #elders
    names = ['family_{}'.format(i) for i in range(N)]
    print(len(self.rutas),len(self.destiny),len(names),N)
    atributos = list(zip(a,b,c,d,node_ids,m,w,o_d,o,depto,self.rutas,self.destiny,names))
    

   
    self.entities_list =  [Entity(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12]) for i in atributos] # Syntetic population
    #if scenario == 3: #--> filtrar población a solo hogares cercanos a edificios
    #  self.selectBuildingsRoutes()
    #print([entitie.destiny_choice for entitie in entities_list])
    print('')
    print('Número familias seleccionadas: {}'.format(len(self.entities_list)))
    print('')

class TsuSimulator(Simulator):

    def __init__(self,Sim,verbose = False,save = False, path = '/content/drive/MyDrive/MT/Código_simulación/Imagenes_gif_status/'):

        super().__init__()
        self.Sim = Sim 
        self.initializeParameters()
        self.population = self.Sim.entities_list #list_entities
        self.edges_id_servers_new = None # Lista new_ids 
        self.nodes_id_b_new = None # Lista new_ids  (0,1,2,3,....)
        self.nodes_id_mp_new = None # Lista new_ids 
        self.edges_id_servers = None # Lista ids originales
        self.nodes_id_b = None # Lista ids  originales
        self.nodes_id_mp = None # Lista ids originales
        
        self.replica = self.Sim.replica
        
        '''
        self.numero = []
        self.kids = []
        self.youngs = []
        self.adults = []
        self.elders = []
        self.hombres = []
        self.mujeres = []

        self.instante = []
        '''


        self.destiny = self.Sim.destiny
        self.rutas = self.Sim.rutas
        self.delay_probabilities = self.Sim.delay_probabilities
        self.time_in_minutes = self.Sim.time_in_minutes
        self.velocity_factors = self.Sim.velocity_factors
        self.max_capacity_b = self.Sim.max_capacity_b
        self.distance_rutas = self.Sim.distance_rutas
        self.scenario = self.Sim.scenario
        self.Antofagasta = self.Sim.Antofagasta
        
        self.verbose = verbose
        self.save = save
        self.path = path
        # Results
        self.Br = [] #diccionario con claves cada instante de tiempo
        self.MPr = []
        self.serversr = []

        self.serversrr = None
        self.Brr = None
        self.MPrr = None
        
        
        
        # Número de personas actual en las calles ( en sistema )
        self.flujo_total = 0
        self.flujo_kids  = 0
        self.flujo_youngs = 0
        self.flujo_adults = 0
        self.flujo_elders = 0
        self.flujo_hombres = 0
        self.flujo_mujeres = 0


    def SaveStatistics(self):

      # guardar eventos
      # ids reseteados y originales de servidores, puntos de encuentro y edificios
      # Estados finales edificios y puntos de encuentro (calles obviamente están vacías)
      # entidades en edificios: self.B , entidades en puntos de encuentro: self.MP
      # Estados para cada instante de tiempo ( guardar en cada evento estados):
      # lista instantes de tiempo: self.instante , entidades en servidores: self.servers, entidades en edificios: self.B, entidades en puntos de encuentro: self.MP
      #  self.edges_id_servers_new = None # Lista new_ids 
      #  self.nodes_id_b_new = None # Lista new_ids  (0,1,2,3,....)
      #  self.nodes_id_mp_new = None # Lista new_ids 
      #  self.edges_id_servers = None # Lista ids originales
      #  self.nodes_id_b = None # Lista ids  originales
      #  self.nodes_id_mp = None # Lista ids originales

      ids = [self.edges_id_servers,self.nodes_id_b,self.nodes_id_mp]
      names_ids = ['edges_ids_servers','nodes_id_b','nodes_id_mp']

      ids_news = [self.edges_id_servers_new,self.nodes_id_b_new,self.nodes_id_mp_new]
      names_ids_news = ['edges_ids_servers_new','nodes_id_b_new','nodes_id,mp_new']

      #self.serversrr = { i: e for i,e in zip(self.instante,self.serversr)}
      #self.Brr = { i: e for i,e in zip(self.instante,self.Br)}
      #self.MPrr = { i: e for i,e in zip(self.instante,self.MPr)}
      #results = [self.serversrr,self.Brr,self.MPrr]
      #names_ = ['servers','B','MP']

      '''
      total_ = ids + ids_news + results
      names = [i + '_{}_{}'.format(scenario,replica)]
      for param,nam in zip(total_,names):
        with open("{}.pickle".format(nam), "wb") as f:
            pickle.dump(param, f)
      '''
    def PlotResults(self):
        
        import matplotlib.pyplot as plt
        #intervalos = range(int(min(self.evacuation_times)), int(max(self.evacuation_times)) + 200)
        # TIEMPOS DE EVACUACION, SEPARADOS POR TIO REFUGIO Y TIPO PERSONA
        todos = [i[0] for i in self.evacuation_times ]
     
        
        bbb = [i[0] for i in self.evacuation_times if i[1]=='B']
        mpp = [i[0] for i in self.evacuation_times if i[1]=='MP']
        
        bbb_kids = [i[0] for i in self.evacuation_times_kids if i[1]=='B']
        mpp_kids = [i[0] for i in self.evacuation_times_kids if i[1]=='MP']
        
        bbb_youngs = [i[0] for i in self.evacuation_times_youngs if i[1]=='B']
        mpp_youngs = [i[0] for i in self.evacuation_times_youngs if i[1]=='MP']
        
        bbb_adults = [i[0] for i in self.evacuation_times_adults if i[1]=='B']
        mpp_adults = [i[0] for i in self.evacuation_times_adults if i[1]=='MP']
        
        bbb_elders = [i[0] for i in self.evacuation_times_elders if i[1]=='B']
        mpp_elders = [i[0] for i in self.evacuation_times_elders if i[1]=='MP']
        
        bbb = [i[0] for i in self.evacuation_times if i[1]=='B']
        mpp = [i[0] for i in self.evacuation_times if i[1]=='MP']
        
        bbb_trabajo = [i[0] for i in self.evacuation_times if (i[1]=='B') & (i[2]=='trabajo')]
        mpp_trabajo = [i[0] for i in self.evacuation_times if(i[1]=='MP') & (i[2]=='trabajo')]
        
        bbb_estudio = [i[0] for i in self.evacuation_times if (i[1]=='B') & (i[2]=='estudio')]
        mpp_estudio = [i[0] for i in self.evacuation_times if(i[1]=='MP') & (i[2]=='estudio')]
        
        
        bbb_otros = [i[0] for i in self.evacuation_times if (i[1]=='B') & (i[2]=='otros')]
        mpp_otros = [i[0] for i in self.evacuation_times if(i[1]=='MP') & (i[2]=='otros')]
        
        bbb_familias = [i[0] for i in self.evacuation_times if (i[1]=='B') & (i[2]== False)]
        mpp_familias = [i[0] for i in self.evacuation_times if(i[1]=='MP') & (i[2]== False)]

        plt.title('Histograma tiempos de evacuación total, {}'.format(self.scenario))
        plt.hist(x=todos, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación edificios, {}'.format(self.scenario))
        plt.hist(x=bbb, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación shelters, {}'.format(self.scenario))
        plt.hist(x=mpp, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación edificios trabajo, {}'.format(self.scenario))
        plt.hist(x=bbb_trabajo, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación shelters trabajo, {}'.format(self.scenario))
        plt.hist(x=mpp_trabajo, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación edificios estudio, {}'.format(self.scenario))
        plt.hist(x=bbb_estudio, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación shelters estudio, {}'.format(self.scenario))
        plt.hist(x=mpp_estudio, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        
        plt.title('Histograma tiempos de evacuación edificios otros, {}'.format(self.scenario))
        plt.hist(x=bbb_otros, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación shelters otros, {}'.format(self.scenario))
        plt.hist(x=mpp_otros, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación edificios familias, {}'.format(self.scenario))
        plt.hist(x=bbb_familias, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación shelters familias, {}'.format(self.scenario))
        plt.hist(x=mpp_familias, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
    def initializeParameters(self):
        self.Sim.createScenario()

    def start(self):
        import copy
        self.ResetIndex()
        self.events = ListQueue()
        #self.server = Server_() # De momento un único servidor en toda la simulación
        #self.shelter = Shelter_() # De momento un único refugio en toda la simulación
        self.servers = {}
        self.servers2 = {} # para calcular flujo acumulado en cada calle
        self.shelters = {}
        self.B = {}
        self.MP = {}
        self.evacuation_times = [] # Todo tipo de personas, opcion de separar a edificios y shelters
        #self.evacuation_times_2 = [] # Separa a edificios y shelters
        self.evacuation_times_kids = []
        self.evacuation_times_youngs = []
        self.evacuation_times_adults = []
        self.evacuation_times_elders = []

        # Inicializador de eventos, servidores y refugios ( 14087 familias )
        #############################################################
        # Aquí se ingresa el input del modelo
        # input para server y shelter generator : rutas y destiny
        #self.ServerGenerator_(['{}'.format(i) for i in range(S)])
        #self.ShelterGenerator_(['{}'.format(i) for i in range(B)],['{}'.format(i) for i in range(MP)])
        self.ServerGenerator_()
        self.ShelterGenerator_()
        self.servers2 = copy.deepcopy(self.servers)

        self.InitialEventGenerator_()

        #############################################################
        #self.StatusView('Initial')
        self.doAllEvents()
        self.SaveStatistics()
        #self.StatusView('Final')
        
        import matplotlib.pyplot as plt
        #intervalos = range(int(min(self.evacuation_times)), int(max(self.evacuation_times)) + 200)
        # TIEMPOS DE EVACUACION, SEPARADOS POR TIO REFUGIO Y TIPO PERSONA
        '''
        todos = [i[0] for i in self.evacuation_times ]
     
        
        bbb = [i[0] for i in self.evacuation_times if i[1]=='B']
        mpp = [i[0] for i in self.evacuation_times if i[1]=='MP']
        
        bbb_kids = [i[0] for i in self.evacuation_times_kids if i[1]=='B']
        mpp_kids = [i[0] for i in self.evacuation_times_kids if i[1]=='MP']
        
        bbb_youngs = [i[0] for i in self.evacuation_times_youngs if i[1]=='B']
        mpp_youngs = [i[0] for i in self.evacuation_times_youngs if i[1]=='MP']
        
        bbb_adults = [i[0] for i in self.evacuation_times_adults if i[1]=='B']
        mpp_adults = [i[0] for i in self.evacuation_times_adults if i[1]=='MP']
        
        bbb_elders = [i[0] for i in self.evacuation_times_elders if i[1]=='B']
        mpp_elders = [i[0] for i in self.evacuation_times_elders if i[1]=='MP']
        
        bbb = [i[0] for i in self.evacuation_times if i[1]=='B']
        mpp = [i[0] for i in self.evacuation_times if i[1]=='MP']
        
        bbb_trabajo = [i[0] for i in self.evacuation_times if (i[1]=='B') & (i[2]=='trabajo')]
        mpp_trabajo = [i[0] for i in self.evacuation_times if(i[1]=='MP') & (i[2]=='trabajo')]
        
        bbb_estudio = [i[0] for i in self.evacuation_times if (i[1]=='B') & (i[2]=='estudio')]
        mpp_estudio = [i[0] for i in self.evacuation_times if(i[1]=='MP') & (i[2]=='estudio')]
        
        
        bbb_otros = [i[0] for i in self.evacuation_times if (i[1]=='B') & (i[2]=='otros')]
        mpp_otros = [i[0] for i in self.evacuation_times if(i[1]=='MP') & (i[2]=='otros')]
        
        bbb_familias = [i[0] for i in self.evacuation_times if (i[1]=='B') & (i[2]== False)]
        mpp_familias = [i[0] for i in self.evacuation_times if(i[1]=='MP') & (i[2]== False)]
        print('#####################################################################################')
        print('FINAL')
        print('#####################################################################################')
        plt.title('Histograma tiempos de evacuación total, {}'.format(self.scenario))
        plt.hist(x=todos, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación edificios, {}'.format(self.scenario))
        plt.hist(x=bbb, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación shelters, {}'.format(self.scenario))
        plt.hist(x=mpp, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación edificios trabajo, {}'.format(self.scenario))
        plt.hist(x=bbb_trabajo, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación shelters trabajo, {}'.format(self.scenario))
        plt.hist(x=mpp_trabajo, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación edificios estudio, {}'.format(self.scenario))
        plt.hist(x=bbb_estudio, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación shelters estudio, {}'.format(self.scenario))
        plt.hist(x=mpp_estudio, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        
        plt.title('Histograma tiempos de evacuación edificios otros, {}'.format(self.scenario))
        plt.hist(x=bbb_otros, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación shelters otros, {}'.format(self.scenario))
        plt.hist(x=mpp_otros, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación edificios familias, {}'.format(self.scenario))
        plt.hist(x=bbb_familias, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        
        plt.title('Histograma tiempos de evacuación shelters familias, {}'.format(self.scenario))
        plt.hist(x=mpp_familias, bins=20)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('N° evacuados')
        plt.show()
        #grafico acumulado
        
        import math
        '''
        '''
        def calcular_tiempo_promedio_y_acumulado(string,lista_tiempos):
          tiempos = list(set(lista_tiempos))# cada tiempo se repite el numero de personas que evacuaron en dicho tiempo
          mean = round(sum(lista_tiempos)/len(lista_tiempos),2)
          var = sum([(t - mean)**2 for t in lista_tiempos])/len(lista_tiempos)
          std = round(var**0.5,2)
          print('Tiempo promedio {} : {}, Desviacion estándar: {}'.format(string,mean,std))
          tiempos.sort()
          evacuados = [lista_tiempos.count(tiempo) for tiempo in tiempos]
      
          cum = []
          summ = 0
          for tiempo,evac in zip(tiempos,evacuados):
            summ += evac
            cum.append(summ)
          x = tiempos
          y = cum
          plt.plot(x,y)#, bins=intervalos)
          plt.show()

          

        for string,lista_tiempos in [('Total',self.evacuation_times),('Kids',self.evacuation_times_kids),('Youngs',self.evacuation_times_youngs),('Adults',self.evacuation_times_adults),('Elders',self.evacuation_times_elders)]:
          calcular_tiempo_promedio_y_acumulado(string = string,lista_tiempos = lista_tiempos)

        Y = self.numero
        Y1 = self.kids
        Y2 = self.youngs
        Y3 = self.adults
        Y4 = self.elders
        X = self.instante

        self.Y = Y
        self.Y1 = Y1
        self.Y2 = Y2
        self.Y3 = Y3
        self.Y4 = Y4
        self.X = X
      
        import matplotlib.pyplot as plt
        def calcular_personas_sistema(X,Y,string):

          num_prom = []

          def get_indexes(ls,index):
            return [i for i in range(len(ls)) if ls[i] == index]

          for y in list(set(Y)):
            tpo = 0
            indices = get_indexes(Y,y)
            for i in indices:

              if X[i] != X[-1]:

                tpo += X[i+1] - X[i]
                #if tpo == 0:
                #  print(X[i+1],X[i])
            vv = (y,tpo/X[-1])
            num_prom.append(vv)

          #print(num_prom)
          num_prom = sum([a*b for a,b in num_prom])
          #print("Ultimo numero {} {}".format(string,Y[-1]))
          print("Número promedio {} en el sistema: {}".format(string,num_prom))
        calcular_personas_sistema(X,Y,'personas')
        calcular_personas_sistema(X,Y1,'niños')
        calcular_personas_sistema(X,Y2,'jovenes')
        calcular_personas_sistema(X,Y3,'adultos')
        calcular_personas_sistema(X,Y4,'adultos mayores')
        
      
        plt.plot(X,Y)#, bins=intervalos)
        plt.show()
        '''



            
        
            
          
        k,y,a,e,mm,ww = 0,0,0,0,0,0
        for key in self.B:
          kids = sum([self.B[key].capacity[e].kids_members for e in self.B[key].capacity])
          youngs = sum([self.B[key].capacity[e].youngs_members for e in self.B[key].capacity])
          adults = sum([self.B[key].capacity[e].adults_members for e in self.B[key].capacity])
          elders = sum([self.B[key].capacity[e].elders_members for e in self.B[key].capacity])
          m = sum([self.B[key].capacity[e].m for e in self.B[key].capacity])
          w = sum([self.B[key].capacity[e].w for e in self.B[key].capacity])
          k += kids
          y += youngs 
          a += adults
          e += elders
          mm += m
          ww += w
        self.Bk = k
        self.By = y
        self.Ba = a
        self.Be = e
        self.Bm = mm
        self.Bw = ww 
        print("B, kids: {}, youngs: {}, adults: {}, elders: {}, hombres: {}, mujeres: {}".format(k,y,a,e,mm,ww))
        
        k,y,a,e,mm,ww = 0,0,0,0,0,0
        for key in self.MP:
          kids = sum([self.MP[key].capacity[e].kids_members for e in self.MP[key].capacity])
          youngs = sum([self.MP[key].capacity[e].youngs_members for e in self.MP[key].capacity])
          adults = sum([self.MP[key].capacity[e].adults_members for e in self.MP[key].capacity])
          elders = sum([self.MP[key].capacity[e].elders_members for e in self.MP[key].capacity])
          m = sum([self.MP[key].capacity[e].m for e in self.MP[key].capacity])
          w = sum([self.MP[key].capacity[e].w for e in self.MP[key].capacity])
          k += kids
          y += youngs 
          a += adults
          e += elders
          mm += m
          ww += w
        self.MPk = k
        self.MPy = y
        self.MPa = a
        self.MPe = e
        self.MPm = mm
        self.MPw = ww 

           
        print("MP, kids: {}, youngs: {}, adults: {}, elders: {}, hombres: {}, mujeres: {}".format(k,y,a,e,mm,ww))




    def ResetIndex(self):
      Server_.id = 0
      Building_.id = 0
      Meeting_Point_.id = 0
      Entity.id = 0
      
    def InitialEventGenerator_(self):
       #Rutas muestra 5 familias, 3 to B, 2 to MP(mismo MP : 1902 ID NODO).


      i = 0
      len_rutas = []
      times = []
      distt = []

      for entity in self.population:

        distances = self.distance_rutas[i]
        
        if entity.destiny_choice == 'B':
          distance = distances[0]
        elif entity.destiny_choice == 'MP':
          distance = distances[1]
        elif entity.destiny_choice == 'B-MP':
          distance = distances[2]
        delay = entity.delay_start
        v = entity.family_street_velocity
        d = distance
        time = (d/v) + delay
        times.append(time)
        distt.append(d)

        #print('Familia {}, velocidad: {}'.format(i,entity.family_street_velocity))
        #print('Refugio : {}, distancias: {}'.format(entity.destiny_choice,self.distance_rutas[i] ))
        
        Rutas_ = self.rutas
        #Family = entitie
        entity.previous_server = None
        #Family.destiny_choice = Rutas[i][-1]
        #print('Hola')
        #print(self.edges_id_servers)
        #print(self.edges_id_b.index(4760),self.edges_id_mp)

        #HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        #print('Familia {}, rutas ids originales: {} '.format(i,entity.route))

        #print(entity.destiny_choice == 'B' and len(entity.route['B']) != 0,list(map(lambda x: self.edges_id_servers.index(x),Rutas_[i][0][:-2])) + list(map(lambda x: self.nodes_id_b.index(x),Rutas_[i][0][-2:-1]))) # Transforma a nuevos indices)
        #print(entity.destiny_choice == 'MP' and len(entity.route['MP']) != 0,list(map(lambda x: self.edges_id_servers.index(x),Rutas_[i][1][:-2])) + list(map(lambda x: self.nodes_id_mp.index(x),Rutas_[i][1][-2:-1])))
        entity.updateNewIds(self,i)
        # Puede ser street o shelter arrival en un inicio
        if len(entity.route[entity.destiny_choice]) == 1 :
          id_shelter = entity.route[entity.destiny_choice][0]
          # si el evento inicial es shelter arrival, entonces el delay start es 0 pq ya se ecnuentra en el refugio
          event = Shelter_Arrival(entity,id_shelter,None,entity.delay_start)

        elif len(entity.route[entity.destiny_choice]) > 1:
          id_first_street = entity.route[entity.destiny_choice].pop(0)
          entity.actual_server = id_first_street
          event = Street_Arrival(entity,id_first_street,entity.delay_start)
          if entity.delay_start<0:
              print('STREET ARRIVAL == 0', entity.delay_start,entity.o_d,entity.DEPTO)
          #print("Shelter_Arrival")

        else:
          print("ERROR, LISTA VACÍA")
          raise ValueError  
        i += 1

       
        self.events.insert(event)
      #print('maximo de calles {}'.format(max(len_rutas)))
      

      indice = np.argmax(times)
      if self.population[indice].destiny_choice == 'MP' :
        ruta_original = [self.edges_id_servers[i] for i in self.population[indice].route[self.population[indice].destiny_choice][:-1]] + [self.nodes_id_mp[self.population[indice].route[self.population[indice].destiny_choice] [-1] ] ]
      elif self.population[indice].destiny_choice == 'B':
        ruta_original = [self.edges_id_servers[i] for i in self.population[indice].route[self.population[indice].destiny_choice][:-1]] + [self.nodes_id_b[self.population[indice].route[self.population[indice].destiny_choice] [-1] ] ]
        
      #print('Tiempo max {}'.format(max(times)))
      #print('Familia {}, velocidad: {}, rutas ids : {} '.format(indice,self.population[indice].family_street_velocity, ruta_original ))#self.population[indice].route[self.population[indice].destiny_choice]))
      #print('Refugio : {}, distancias: {}'.format(self.population[indice].destiny_choice,self.distance_rutas[indice] ))
      #print('Distance: {}, delay: {}'.format(max(distt),self.population[indice].delay_start))
      #print(" Destino {}: {}".format(self.population[indice].destiny_choice,self.population[indice].route[self.population[indice].destiny_choice] [-1] ) )
      
      #import matplotlib.pyplot as plt
      #plt.hist(times)
      #print("First Arrivals Streets ")
      #for i in self.events.elements:
        
        #print("{}, tiempo salida: {}[min], velocidad: {:.2f}[mt/s], first arrival in street {} --> ruta mas corta hacia {}: {}, {}: {}".format(i.entity.name,(i.entity.delay_start/60),i.entity.family_street_velocity,i.server,i.entity.destiny_choice, i.entity.route_original[i.entity.destiny_choice][:-1],i.entity.destiny_choice,i.entity.route_original[i.entity.destiny_choice][-1]))
      #print("-----------------------------------------------------------------------------")
    
    def ServerGenerator_(self): #keys servers dict ( self.servers)
      Rutas_ = self.rutas
      Servers = []

      #Rutas = [[ruta1,ruta2,ruta3],[ruta1,ruta2,ruta3]...]
      for i,entity in enumerate(Rutas_[:]): # Se quita 'B' o 'MP' ,  y id respectivo, por eso -2
        if self.destiny[i] == 'B':
          Servers += entity[0][:-2] #h-b
          Servers += entity[2][:-2] # b-mp
        elif self.destiny[i] == 'MP':
          Servers += entity[1][:-2] #h-mp
          Servers += entity[2][:-2] # b-mp
        #for rutas in entity:
        #  Servers += rutas[:-2]
      
      self.edges_id_servers = list(set(Servers))
      Servers = list(set(Servers))
      #print('Servers original ids :{}'.format(Servers))
      new_ids_servers = [i for i in range(len(Servers))]
      #print('Servers new ids :{}'.format(new_ids_servers))
      self.edges_id_servers_new = new_ids_servers
      # Ej : [1230,345,32345,234,3234,1234]
      #    : [0    , 1, 2    , 3, 4   ,  5]
      #path = "/content/drive/MyDrive/MT/Código_simulación/Simulador_basico/shapefiles_codigo_oficial/"
      #calles = gpd.read_file(path + 'Antofa_edges_of.shp')
      #calles = calles[calles.new_id.isin(Servers)]
      calles = self.Antofagasta
      i = 0
      for server in Servers[:]:
        # 0,1,2,3,...,len(Servers[:])
        #Agregar length
        #print(Servers[i])
        width = calles[calles['new_id']==Servers[i]]['width'].tolist()[0]
        length = calles[calles['new_id']==Servers[i]]['length'].tolist()[0]
        self.servers[Servers[:].index(server)] = Server_(length,width)
        i += 1
    
      #for server in servers:
      #  self.servers[server] = Server_()


    
    def ShelterGenerator_(self): #id's shelters
      Rutas_ = self.rutas
      buildings = []
      meeting_Points = []
      #Rutas = [[ruta1,ruta2,ruta3],[ruta1,ruta2,ruta3]...]
  

      for i,entity in enumerate(Rutas_[:]):
      
        if self.destiny[i] == 'B':
          if len(entity[0]) != 0:
            buildings.append(entity[0][-2:-1] [0])
            meeting_Points.append(entity[2][-2:-1] [0])
        elif self.destiny[i] == 'MP':
          if len(entity[1]) != 0:
            #buildings.append(entity[0][-2:-1] [0])
            meeting_Points.append(entity[1][-2:-1] [0])
            meeting_Points.append(entity[2][-2:-1] [0])

          
        #for destino in entity:
        #  if len(destino) != 0:
        #    if destino[-1] == 'B':
        #      buildings.append(destino[-2:-1][0])
              #print(buildings)

        #    elif destino[-1] == 'MP':
        #      meeting_Points.append(destino[-2:-1][0])
        #    elif destino[-1] =='B-MP':
        #      meeting_Points.append(destino[-2:-1][0])
        #  else:
        #    pass  

      #print(buildings, meeting_Points)
      self.nodes_id_b = list(set(buildings))
      self.nodes_id_mp = list(set(meeting_Points))
      buildings = list(set(buildings))
      meeting_Points = list(set(meeting_Points))
      #print('Buildings original ids: {}'.format(buildings))
      #print('Meeting Points orignal ids: {}'.format(meeting_Points))

      new_ids_b = [i for i in range(len(buildings))]
      new_ids_mp = [i for i in range(len(meeting_Points))]
      self.nodes_id_b_new = new_ids_b
      self.nodes_id_mp_new = new_ids_mp
      #print('Buildings new ids: {}'.format(new_ids_b))
      #print('Meeting Points new ids: {}'.format(new_ids_mp))
      
      # 0 ,1, 2,3 ,--
      #print(buildings)
      for shelter in buildings:
        self.B[buildings.index(shelter)] = Building_(B_[B_['new_id']==shelter]['available_capacity'].iloc[0])

      #0,1,2,...
      for shelter in meeting_Points:
        self.MP[meeting_Points.index(shelter)] = Meeting_Point_()
    
    def StatusView(self,time):
        if time == 'Initial':
          print("-----------INITIAL GENERAL STATUS SERVERS AND SHELTERS-----------------------------------------------------------------------")
        elif time == 'Running':
          print("--------------- GENERAL STATUS SERVERS AND SHELTERS------------------------------------------------------------------------")
        else:
          print("-----------FINAL GENERAL STATUS SERVERS AND SHELTERS-----------------------------------------------------------------------")
        
   
        serverss = [(self.servers[key].name,self.servers[key].flow,self.servers[key].length) for key in self.servers]
        #shelterr = [(self.shelters[key].name,self.shelters[key].flow) for key in self.shelters]
        buildings = [(self.B[key].name,self.B[key].flow,self.B[key].max_capacity) for key in self.B]
        meeting_points = [(self.MP[key].name,self.MP[key].flow) for key in self.MP]
        total_servers = sum([self.servers[key].flow for key in self.servers])
        total_buildings = sum([self.B[key].flow for key in self.B])
        total_meeting_points = sum([self.MP[key].flow for key in self.MP])
        #print(" SERVERS : ", serverss)
        print(" Total families in servers: {}".format(total_servers))
        print("")
        print(" BUILDINGS : ", buildings)
        print(" Total families in buildings: {}".format(total_buildings))
        print("")
        print(" MEETING POINTS : ", meeting_points)
        print(" Total families in meeting points: {}".format(total_meeting_points))
        print(" Total Evacuation Time: {}".format(self.now()))
        import matplotlib.pyplot as plt
 
        ## Declaramos valores para el eje x
        eje_x = [key for key in self.servers2]
        
        ## Declaramos valores para el eje y
        eje_y = [self.servers2[key].flow for key in self.servers2]
        
        ## Creamos Gráfica
        #plt.bar(eje_x, eje_y)
        plt.hist(eje_y)
        ## Legenda en el eje y
        plt.ylabel('Cantidad de calles')
        
        ## Legenda en el eje x
        plt.xlabel('Personas')
        
        ## Título de Gráfica
        plt.title('Flujo total por calle')
        
        ## Mostramos Gráfica
        plt.show()

        print("---------------------------------------------------------------------------------------------------------------------") 

      
    
#######################################################################

#Experiment builder
# Testing sets
#SimParameterss = SimParameters(scenario = scenario,rutas = rutas ,distance_rutas = distance_rutas,delay_probabilities = delay_probabilities, velocity_factors = velocity_factors ,time_in_minutes = time_in_minutes, poblacionSintetica = H_copy, Antofagasta = calles)
#scenario = scenario,rutas = rutas ,distance_rutas = distance_rutas,delay_probabilities = delay_probabilities, velocity_factors = velocity_factors ,time_in_minutes = time_in_minutes, poblacionSintetica = H_copy, Antofagasta = calles


import geopandas as gpd
import pandas as pd
import pickle
import numpy as np

path_ = 'C:/Users/usuario/Desktop/PC/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/'

calles = gpd.read_file(path_ + 'edges_con_edificios_total.shp')
#Añadir calles con sentido contrario a la red
calles_reverse = calles.copy()

from shapely.geometry import Point, LineString
columns = ['u','v','new_u','new_v','new_id','geometry','id','backRefere','forwardRef']
reverse_columns = ['v','u','new_v','new_u',None,None,None,'forwardRef','backRefere']
for column,reverse in zip(columns,reverse_columns):
  if column == 'new_id':
    calles_reverse[column] = [i for i in range(calles.shape[0], 2*calles.shape[0])]
  elif column == 'geometry':
    calles_reverse[column] = [LineString([Point(list(line.coords)[::-1][0]),Point(list(line.coords)[::-1][1])])  for line in calles_reverse[column].tolist()] 
  elif column == 'id':
    calles_reverse[column] = ['reverse_{}'.format(i) for i in range(calles.shape[0], 2*calles.shape[0])]
  else:
    calles_reverse[column] = calles[reverse].tolist()
    
calles = pd.concat([calles,calles_reverse],axis= 0)
calles['width'] = [4 if calle == 'residential' else 8 if calle == 'primary' else 2 for calle in calles['highway'].tolist()] 

path = 'C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/otros'

inputt = []
ps = 'C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/input'
name = ['input_distancias_dia','input_rutas_dia','input_ids_hogares_dia']
for nam in name:
        with open(ps + "/{}.pickle".format(nam), "rb") as f:
            obj = pickle.load(f)
            inputt.append(obj)
distances_final , rutas_final = inputt[0],inputt[1]

H_copy = gpd.read_file('C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/input/H_copy.shp')
H_copy['o_d'] =[False if i == '0' else i for i in H_copy['o_d'].tolist()]
H_copy.rename(columns={'num_person':'num_personas'},inplace = True)

B_ = gpd.read_file('C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/input/B_.shp')
B_.rename(columns={'available_':'available_capacity'},inplace = True)

print('Input cargado ...')
pppp = 'MOD'
#permutacion = np.random.permutation(len(rutas_final))
permutacion = [i for i in range(len(rutas_final))]
o = 0
m = len(rutas_final) #7000#len(rutas_final)
poblacion = H_copy.iloc[permutacion]#H_copy[o:m]
poblacion = poblacion[o:m]
delay_probabilities = {'a': [0.2,0.3,0.3,0.15,0.05,0,0,0],'b':[0,0.1,0.15,0.3,0.3,0.15,0,0],'c':[0,0,0,0.1,0.3,0.3,0.15,0.15],'d':[0,0,0,0,0.2,0.3,0.3,0.2]} # LITERATURA PROBABILIDADES (?)
velocity_factors = [1.3,1.5,1.5,0.98] # FACTORES PARA CALCULAR VELOCIDAD
time_in_minutes = [2,3,4,5,6,7,8,9] # TIEMPOS DE SALIDA
L, C = 80, 400 # LENGTH SERVER Y CAPACIDAD B
LIMIT = 0.751
SC = 200 #STREET CAPACITY
n_replicas = 10

#restt = rest[o:m]

scenarios  = [2]
rutass = [[rutas_final[i] for i in permutacion][o:m] for sc in scenarios ]
distancess = [[distances_final[i] for i in permutacion][o:m] for sc in scenarios ]
destinyy = [None for sc in scenarios]
#rutass = [rutas_final[o:m] for sc in scenarios ]
#distancess = [distances_final[o:m] for sc in scenarios ]
#destinyy = [[None for i in range(0,m)]  for sc in scenarios]
EXPERIMENTS = [{'scenario': s,'rutas':r,'distances':d,'destiny':dest,'replicas':n_replicas } for s,r,d,dest in zip(scenarios,rutass,distancess,destinyy)]
output = {}
kk = 0
for i in range(1,n_replicas):
    for valor,exp in enumerate(EXPERIMENTS): #experiment es un diccionario, EXPERIMENTS diccionario de diccionarios
    
      name = 'scenario_{}'.format(exp['scenario'])
      
      #output.append([name, experiment])
      scenario,rutas,distance_rutas,destiny_ = exp['scenario'],exp['rutas'],exp['distances'],exp['destiny']

      random.seed(i)

      print("Tsunami Evacuation, escenario: {}, réplica: {}".format(scenario,i))
  
      if scenario == 2:
      
      
        SimParameterss = SimParameters(scenario = scenario,rutas = rutas ,distance_rutas = distance_rutas,delay_probabilities = delay_probabilities, velocity_factors = velocity_factors ,time_in_minutes = time_in_minutes, poblacionSintetica = poblacion, Antofagasta = calles,replica = i)
        #print(SimParameterss.rutas[:2])
        #break
        
        ##SimParameterss.createNMi()

        TsuSim = TsuSimulator(Sim = SimParameterss,verbose = False,save = False,path = path ) # Agregar verbose = true,false
      
        
     
        
        TsuSim.dir = 58
        import os

        #os.mkdir(path + 'dir{}_escenario_{}'.format(TsuSim.dir,TsuSim.scenario))
        
        TsuSim.start()
        #TsuSim.SaveStatistics()
        
        
        #Guardar en listas estadisticas para personas promedio en sistema
        '''
        parameters = [TsuSim.instante,TsuSim.numero,TsuSim.kids,TsuSim.youngs,TsuSim.adults,TsuSim.elders,TsuSim.mujeres,TsuSim.hombres]
        name = ['instantes','total','kids','youngs','adults','elders','mujeres','hombres']
        pathhh = 'C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/personasprom_flujocalles'
        for param,nam in zip(parameters,name): 
           with open(pathhh + "/{}_{}.pickle".format(nam,i), "wb") as f: 
        
                 pickle.dump(param, f)
        '''         
        # Guardar estadisticas para flujo acumulados de cada calle
        '''
        C = {key:TsuSim.servers2[key].flow for key in TsuSim.servers2}
        #B = {key:TsuSim.B[key].flow for key in TsuSim.B}
        #MP = {key:TsuSim.MP[key].flow for key in TsuSim.MP}
        parameters = [C]
        name = ['calles']
        pathhh = 'C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/personasprom_flujocalles'
        for param,nam in zip(parameters,name): 
           with open(pathhh + "/{}_{}.pickle".format(nam,i), "wb") as f: 
        
                 pickle.dump(param, f)
        
                 
        columna_flujo_calle = [TsuSim.servers2[key].flow for key in TsuSim.servers2]
        columna_id_calle = [key for key in TsuSim.servers2]
        '''
        C = [(key,TsuSim.servers2[key].flow) for key in TsuSim.servers2]
        fcalles = pd.DataFrame(C, columns = ['id_calle','flujo'])
        fcalles.to_csv('calles_of_{}.csv'.format(i))
        
        # Guardar resultados en un csv, para dps graficar en POWER BI 
        
        atributos = ['id','kids','youngs','adults','elders','node_id','hombres','mujeres','o_d','o','DEPTO','destiny_choice','name','family_type','delay_start','final_time','nodo_destino']
        filas = []
        
        for b in TsuSim.B:
            for e in TsuSim.B[b].entidades:
                a1 = e.id
                a2 = e.kids_members
                a17 = e.youngs_members
                a3 = e.adults_members
                a4 = e.elders_members
                a5 = e.node_id
                a6 = e.m
                a7 = e.w
                a8 = e.o_d
                a9 = e.o
                a10 = e.DEPTO
                a12 = e.destiny_choice
                a13 = e.name
                a14 = e.family_type
                a15 = e.delay_start
                a16 = e.final_time
                a18 = int(e.id_destiny)
                filas.append((a1,a2,a17,a3,a4,a5,a6,a7,a8,a9,a10,a12,a13,a14,a15,a16,a18))
        
        for mp in TsuSim.MP:
            for e in TsuSim.MP[mp].entidades:
                a1 = e.id
                a2 = e.kids_members
                a17 = e.youngs_members
                a3 = e.adults_members
                a4 = e.elders_members
                a5 = e.node_id
                a6 = e.m
                a7 = e.w
                a8 = e.o_d
                a9 = e.o
                a10 = e.DEPTO
                a12 = e.destiny_choice
                a13 = e.name
                a14 = e.family_type
                a15 = e.delay_start
                a16 = e.final_time
                a18 = int(e.id_destiny)
                filas.append((a1,a2,a17,a3,a4,a5,a6,a7,a8,a9,a10,a12,a13,a14,a15,a16,a18))
        
        
        results = pd.DataFrame(filas, columns = atributos)
        results.to_csv('oficial_{}.csv'.format(i))
        
        # DESGLOSAR FAMILIAS EN ENTIDADES INDIVIDUALES
        filas2 = []
        new_columns = ['id', 'node_id', 'o_d', 'o', 'DEPTO', 'destiny_choice', 'name', 'family_type',
       'delay_start', 'final_time', 'nodo_destino']
        add = ['edad','sexo']
        
        for f in range(len(results)):
            mmm = copy.copy(results.loc[f]['mujeres'])
            hhh = copy.copy(results.loc[f]['hombres'])
            
            for j in ['kids','youngs','adults','elders']:
                for jjjj in range(results.loc[f][j]):
                    if results.loc[f][j] > 0: # número de nuevas filas con etiqueta j
                          if mmm > 0:
                              new_fila = results.loc[f][new_columns].tolist() + [j] + ['mujer']
                              mmm -= 1
                          elif hhh > 0:
                              new_fila = results.loc[f][new_columns].tolist() + [j] + ['hombre']
                              hhh -= 1
                          filas2.append(new_fila)
                      
        results_2 = pd.DataFrame(filas2, columns = new_columns + add)
        results_2.to_csv('oficial_2_{}.csv'.format(i))   
        #######################################################
        
        print('##############################################')
        print('GUARDANDO RESULTADOS ESCENARIO {}, REPLICA {}...'.format(scenario,i))
        print('##############################################')

        
        '''
        output['Experiment_{}_replica_{}'.format(valor,i)] = TsuSim
        parameters = [output['Experiment_{}_replica_{}'.format(valor,i)] ]
        name = ['scenario_{}'.format(scenario)]
        pathhh = 'C:/Users/usuario/Desktop/PC/CODIGO_OFICIAL/Archivos_oficiales_mt/Resultados_simulacion'
        for param,nam in zip(parameters,name): 
          with open(pathhh + "/{}_{}_dia.pickle".format(nam,i), "wb") as f:
              pickle.dump(param, f)           
        
          #TsuSim.CreateGif()
        '''
         
        ######################################################
        #print(len(SimParameterss.NMi))
        '''
        import pickle
        s = SimParameterss
        parameters = [s.NMi,s.CBj,s.MD ,s.WE , s.WK , s.WA , s.ELDERS , s.KIDS , s.ADULTS,s.BDij,s.rest,nnn]
        print(len(s.ADULTS))
        name = ['NMi','CBj','MD','WE','WK','WA','ELDERS','KIDS','ADULTS','BDij','rest','num_edif']
        pathhh = '/content/drive/MyDrive/MT/Código_simulación/Input_modelo_cplex/'
        for param,nam in zip(parameters,name):
          with open(pathhh + "{}_dia.pickle".format(nam), "wb") as f:
              pickle.dump(param, f)
        kk += 1

        #break
        '''
      else:
        pass


  #with open('experimentsConfigA.pickle', 'wb') as f:
  #    pickle.dump(output, f)

