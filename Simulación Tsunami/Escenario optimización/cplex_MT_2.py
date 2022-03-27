# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 16:52:06 2021

@author: usuario
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 18:50:47 2021

@author: usuario
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 13:25:12 2020

@author: usuario
"""


#from timeit import timeit
from collections import deque
import docplex.mp #Cplex
from docplex.mp.model import Model
#from arbol_normal2 import Arbol
#from arbol_normal2 import Nodo
from matplotlib import pyplot as plt 
import numpy as np




class py_docplex():
    def __init__(self,BDij,rest,NMi,CBj,MD,WE,WK,WA,ELDERS,KIDS,ADULTS,FO,nnn,depto,save=False):
 
        self.BDij = BDij
        self.rest = rest
        self.NMi = NMi
        self.CBj = CBj
        self.MD =MD
        self.WE = WE
        self.WK = WK
        self.WA = WA
        self.ELDERS = ELDERS
        self.KIDS = KIDS
        self.ADULTS = ADULTS
        self.funcion_objetivo= [WE*elders + WK*kids + WA*adults for elders,kids,adults in zip(ELDERS,KIDS,ADULTS)]
        self.nnn = nnn
        self.depto = depto
        self.solution_x = None
        self.solution_y = None
        self.save = save
           
    def resolver_pl(self):

        FO=self.funcion_objetivo
        BDij = self.BDij
        NMi = self.NMi 
        CBj = self.CBj  
        MD = self.MD 
        WE = self.WE  
        WK =self.WK
        WA= self.WA
        FO = self.funcion_objetivo
        Rest = self.rest
        nnn = self.nnn
        DEPTO = self.depto
        modelo=Model('modelo') #nombre del modelo
        n = len(FO)*nnn # edificios por familia
        m = len(FO)*1 # puntos de encuentro por familia
        x = modelo.binary_var_list(n,name='x') # nnn edificios más cercanos por familia
        y = modelo.binary_var_list(m,name='y') # 1 punto de encuentro más cercano por familia
        xij = {}
        cont = 0
        for i in range(len(FO)):
            for j in range(nnn):
                xij['x_{}_{}'.format(i,j)] = x[cont]
                cont += 1
        
        fo = 0
        for i in range(len(FO)):
            for j in range(nnn):
                fo += FO[i] * xij['x_{}_{}'.format(i,j)] # + xij['x_{}_{}'.format(i,j)] * j * (-1)*(0.00000000000000000000000000000000000000000000000000000001)
        modelo.maximize(fo)
                
        
        #modelo.maximize(modelo.sum(FO[fam]*x[i] + FO[fam]*x[i+1] + FO[fam]*x[i+2] + FO[fam]*x[i+3] for fam,i in enumerate(range(0,n,4)) ) )
        print(len(BDij), len(BDij[0]))
        print(len(FO))
        
        #RESTRICCION DE ASIGNACION EDIFICIOS, MAXIMO 1 POR FAMILIA
        for i in range(len(FO)):
            rest = y[i]
            for j in range(nnn):
             
                #print(i,j)
                rest += xij['x_{}_{}'.format(i,j)]
                #print(float(BDij[i][j]),xij['x_{}_{}'.format(i,j)])
                #bd += float(BDij[i][j]) * xij['x_{}_{}'.format(i,j)]
            #modelo.add_constraint(bd <= 1000000000000 )
            modelo.add_constraint(rest <= 1)
           
        #RESTRICCION EXTRA PARA PROBAR ALGO    
     
        #################      
        #for i,j in zip(range(0,n,4),range(0,m)):
        #   modelo.add_constraint(x[i] + x[i+1] + x[i+2] + x[i+3] + y[j] == 1)
        #   modelo.add_constraint(float(BDi1[j])*x[i] + float(BDi2[j])*x[i+1] + float(BDi3[j])*x[i+2] + float(BDi4[j])*x[i+3] <= MD)
        
        #RESTRICCION DE CAPACIDAD PARA CADA EDIFICIO
        
        indices_edificios_mas_cercanos_para_cada_familia = CBj[0]
        dict_capacidades_edificios= CBj[1]
        dict_ocupacion_edificios = {i:0 for i in dict_capacidades_edificios}
        for j in range(nnn):
            for i,nmi in enumerate(NMi):
                ind = indices_edificios_mas_cercanos_para_cada_familia[i][j]
                dict_ocupacion_edificios[ind] += xij['x_{}_{}'.format(i,j)]*nmi
                
                #restt += xij['x_{}_{}'.format(i,j)]*nmi
            #print(restt)
            # modelo.add_constraint(restt <= CBj[i][j])
            #modelo.add_constraint(restt <= CBj[i][j])#CBj
            
        for ind in dict_ocupacion_edificios:
            modelo.add_constraint(dict_ocupacion_edificios[ind] <= dict_capacidades_edificios[ind])
        
        #RESTRICCION DE EDIFICIOS MÁS LEJANOS A MP NO DEBEN ASIGNARSE
        ##
        
        for i in range(len(FO)):
            for j in range(nnn):
                if Rest[i][j] == 0:
                    modelo.add_constraint(xij['x_{}_{}'.format(i,j)] == 0)
                else:
                    pass
              
        
        # RESTRICCION PARA ASIGNAR A PERSONAS QUE YA ESTÁN EN EDIFICIOS
        cont = 0
        for i,j in zip(Rest,DEPTO):
            if j == 1 and i[0] !=0:
                
                ind = indices_edificios_mas_cercanos_para_cada_familia[cont][0]
                #print('edificio: {},familia: {}'.format(ind,cont))
                modelo.add_constraint(xij['x_{}_{}'.format(cont,0)] == 1)
               
            else:
                pass
            cont += 1
        
        #modelo.add(modelo.sum(x[i]*nmi for i,nmi in zip(range(0,n,4),NMi)) <= CBj)
        #modelo.add(modelo.sum(x[i+1]*nmi for i,nmi in zip(range(0,n,4),NMi)) <= CBj)
        #modelo.add(modelo.sum(x[i+2]*nmi for i,nmi in zip(range(0,n,4),NMi)) <= CBj)
        #modelo.add(modelo.sum(x[i+3]*nmi for i,nmi in zip(range(0,n,4),NMi)) <= CBj)
        
   
            
            
        #modelo.add(modelo.sum(x[i]*1 for i in range(0,self.m))==1)
        #print(modelo.export_to_string())
        modelo.print_information()
        solucion = modelo.solve(log_output=True)
        estado = modelo.get_solve_status()
        if solucion:
            #i=solucion.display()
            fo=solucion.get_objective_value()
            solutions=[x[i].solution_value for i in range(0,n)] #xij
            solutions2 = [y[i].solution_value for i in range(0,m)] #yij
            dictt = xij
            #solutions=[y[i].solution_value for i in range(0,m)]
            self.solution_x = solutions
            self.solution_y = solutions2
            self.Save()
            #for ind in dict_ocupacion_edificios:
            #    print( dict_capacidades_edificios[ind],ind)
            
            print("Números 1: {}".format(solutions.count(1)))
           # print("--------------Iteración x---------------")
            #print("Estado: ",estado)
            print("FO=",fo,end= "")
            print(len(solutions))
            #count = 0
            #for i in range(0,n,nnn):
            #    g = [solutions[i+j] for j in range(nnn)]
            #    if g.count(1) == 1:
            #        index = g.index(1)
            #        print('x_{}_{}=1'.format(count,index),end= " ")
            #    else:
            #        pass
                    #print('y_{}=1'.format(count),end= " ")
            #    count += 1
                #x='x'+str(i)
                #print(", ",x,"=" ,solutions[i],end= "")
                #print(" binaria: ",solutions[2])
            interruptor=True
            print(len(solutions2))
            #print(solutions2[0])
            return [interruptor,fo,solutions,None,estado]
        else: 
            #print("Estado: ",estado)
            interruptor=False
            
            return [interruptor,estado]

    def Save(self):
      parameters = [self.solution_x,self.solution_y]
      name = ['B_noche','MP_noche','dict_noche']
      for param,nam in zip(parameters,name):
        with open("SOLUCIONES_CPLEX\{}.pickle".format(nam), "wb") as f:
            pickle.dump(param, f)

if __name__ == "__main__":
    
    
    import pickle
    name = ['NMi','CBj','MD','WE','WK','WA','ELDERS','KIDS','ADULTS','BDij','rest','num_edif','depto']
    param = []
    for nam in name:
        with open("C:/Users/usuario/Desktop/CODIGO_OFICIAL/Input_modelo_cplex/{}_noche.pickle".format(nam), "rb") as f:
            obj = pickle.load(f)
            param.append(obj)
    
    
    BDij,rest = param[9],param[10]
    NMi,CBj,MD,WE,WK,WA,ELDERS,KIDS,ADULTS = param[0],param[1],param[2],param[3],param[4],param[5],param[6],param[7],param[8]
    nnn = param[11]
    depto = param[12]
    print(nnn)
    o,m = 0,len(rest)#13000
    FO = [WE*elders + WK*kids + WA*adults for elders,kids,adults in zip(ELDERS,KIDS,ADULTS)]
    #print(len(BDij),BDij[2426][35],len(BDij[0]))
    mld = py_docplex(BDij[o:m],rest[o:m],NMi[o:m],CBj,MD,WE,WK,WA,ELDERS[o:m],KIDS[o:m],ADULTS[o:m],FO[o:m],nnn,depto,True)
    ddd = ['B' if i.count(1)>=1 else 'MP' for i in rest]
    print('Hola')
    print(ddd.count('B'),ddd.count('MP'))
    print(len(CBj))
    mld.resolver_pl()
    #print(CBj[0],WE,WK,WA)
    print(len(BDij))
    print(WE,WK,WA)
    print(depto.count(1))
    
