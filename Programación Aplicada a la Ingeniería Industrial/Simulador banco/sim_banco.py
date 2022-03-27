class Cliente :
    def __init__ (self,ID,tipo,preferencia,llegada,demora) :
        self.ID = ID
        self.tipo=tipo
        self.preferencia=preferencia
        self.llegada=llegada
        self.demora=demora
        self.real_espera=0
        self.horario_atencion=0
        self.caja=None
        self.llegada_caja=0
        self.contador=0
        self.contador_cola=0
        self.contador_atendido=0
        self.numero_caja=0
        self.siguiente = None
        self.anterior = None
class Atendido:
    def __init__ (self,ID,tipo,preferencia,llegada,demora,caja) :
        self.ID = ID
        self.tipo=tipo
        self.preferencia=preferencia
        self.llegada=llegada
        self.demora=demora
        self.caja=caja
        self.siguiente=None
        self.anterior=None

class Caja:
    def __init__(self,total_cajas,cajas_t,cajas_e,cajas_g):
        self.total_cajas=total_cajas
        self.cajas_t=cajas_t
        self.cajas_e=cajas_e
        self.cajas_g=cajas_g

class Lista :
    def __init__ (self) :
        self.inicio = None
        self.fin = None
        self.size = 0
    
    def vacia(self):
        return self.inicio == None    
    def agregar_ultimo_clientes(self,ID,tipo,preferencia,llegada,demora):

        if self.vacia() == True:
            self.inicio=self.fin = Cliente(ID,tipo,preferencia,llegada,demora)
       
        else: 
            Nodo_anterior=self.fin
            self.fin = Cliente(ID,tipo,preferencia,llegada,demora)
            Nodo_anterior.siguiente=self.fin
            Nodo_actual=self.fin
            Nodo_actual.anterior=Nodo_anterior
        self.size+=1
        return self.fin   
    def agregar_inicio_cajas(self,total_cajas,cajas_t,cajas_e,cajas_g):
        if self.vacia() == True:
            self.inicio=self.fin = Caja(total_cajas,cajas_t,cajas_e,cajas_g)
        
        else: 
            Nuevo_Nodo_anterior=Caja(total_cajas,cajas_t,cajas_e,cajas_g)
            Nuevo_Nodo_siguiente=self.inicio
            Nuevo_Nodo_anterior.siguiente=Nuevo_Nodo_siguiente
            Nuevo_Nodo_siguiente.anterior=Nuevo_Nodo_anterior
            self.inicio=Nuevo_Nodo_anterior
        return self.inicio
    def agregar_inicio_clientes(self,ID,tipo,preferencia,llegada,demora):
        if self.vacia() == True:
            self.inicio=self.fin = Cliente(ID,tipo,preferencia,llegada,demora)

        else: 
            Nuevo_Nodo_anterior=Cliente(ID,tipo,preferencia,llegada,demora)
            Nuevo_Nodo_siguiente=self.inicio
            Nuevo_Nodo_anterior.siguiente=Nuevo_Nodo_siguiente
            Nuevo_Nodo_siguiente.anterior=Nuevo_Nodo_anterior
            self.inicio=Nuevo_Nodo_anterior#actualizacion nuevo pos inicial, = al nodo ingresado actualmente

        self.size+=1
    def agregar_inicio_atendidos(self,ID,tipo,preferencia,llegada,demora,caja):
        if self.vacia() == True:
            self.inicio=self.fin = Atendido(ID,tipo,preferencia,llegada,demora,caja)

        else: 
            Nuevo_Nodo_anterior=Atendido(ID,tipo,preferencia,llegada,demora,caja)
            Nuevo_Nodo_siguiente=self.inicio
            Nuevo_Nodo_anterior.siguiente=Nuevo_Nodo_siguiente
            Nuevo_Nodo_siguiente.anterior=Nuevo_Nodo_anterior
            self.inicio=Nuevo_Nodo_anterior#actualizacion nuevo pos inicial, = al nodo ingresado actualmente

        self.size+=1
    def recorrer_inicio_clientes(self):
        Nodo_actual=self.inicio
        i=0
        while Nodo_actual != None:
            i+=1
            #print(Nodo_actual.ID,Nodo_actual.tipo,Nodo_actual.preferencia,Nodo_actual.llegada,Nodo_actual.demora,"tamaño: ",i)
            Nodo_actual=Nodo_actual.siguiente
        return i
    def recorrer_inicio_cajas(self):
        Nodo_actual=self.inicio
        print(Nodo_actual.total_cajas,Nodo_actual.cajas_t,Nodo_actual.cajas_e,Nodo_actual.cajas_g)
    def eliminar_ultimo(self):
        if self.vacia():
            print("ESTÁ VACÍA")
        elif self.inicio.siguiente == None:
            self.inicio=self.fin = None
            self.size=0
        else:
            print("AHORA VA A QUEDAR UN CLIENTE EN COLA:", self.fin.ID)
            self.fin=self.fin.anterior
            self.fin.siguiente = None
            self.size-=1
        
      
        return self.fin 
    def eliminar_cliente_segun_dato(self,ID):
            actual=self.inicio

            if actual is None:
                pass
            elif self.fin==self.inicio:
                self.fin=None
                self.inicio=None
            
            elif actual.ID == ID:
                self.inicio = actual.siguiente
                self.inicio.anterior = None
                
            elif self.fin.ID == ID:
                self.fin=self.fin.anterior
                self.fin.siguiente=None
                
            else: 
                while actual:
                    if actual.ID == ID:
                        actual.anterior.siguiente = actual.siguiente
                        actual.siguiente.anterior = actual.anterior
                        
                    actual = actual.siguiente
            self.size-=1
            return actual
    def eliminar_inicio(self):
        
        
        if self.vacia():
            print("ESTÁ VACÍA")
        elif self.inicio.siguiente == None:
            self.inicio=self.fin=None
            self.size = 0
        else:
            self.inicio = self.inicio.siguiente
            self.inicio.anterior = None
            self.size-=1            
    def recorrer_fin(self):
        Nodo_actual=self.fin
        while Nodo_actual != None:
            print(Nodo_actual.ID,Nodo_actual.tipo,Nodo_actual.preferencia,Nodo_actual.llegada,Nodo_actual.demora)
            Nodo_actual=Nodo_actual.anterior
    def ordenar_preferencia(self):
        listaclientes=self.inicio
        i=0
        #print("ORDENAMIENTO POR PREFERENCIA UTILIZANDO BUBBLESORT")
        while(listaclientes.siguiente!=None):
            temp2=listaclientes.siguiente
            while(temp2!=None):
                if(listaclientes.preferencia<temp2.preferencia):
                    aux1=listaclientes.ID
                    aux2=listaclientes.tipo
                    aux3=listaclientes.preferencia
                    aux4=listaclientes.llegada
                    aux5=listaclientes.demora
                    listaclientes.ID=temp2.ID
                    listaclientes.tipo=temp2.tipo
                    listaclientes.preferencia=temp2.preferencia
                    listaclientes.llegada=temp2.llegada
                    listaclientes.demora=temp2.demora
                    temp2.ID=aux1
                    temp2.tipo=aux2
                    temp2.preferencia=aux3
                    temp2.llegada=aux4
                    temp2.demora=aux5

                temp2=temp2.siguiente
            i+=1        
         #   print("ITERACIÓN DE ORDENAMIENTO DE BURBUJA N° ",i,":")
            listaclientes=listaclientes.siguiente
            Nodo_actual=self.inicio
            while Nodo_actual != None:
         #       print(Nodo_actual.ID,Nodo_actual.tipo,Nodo_actual.preferencia,Nodo_actual.llegada,Nodo_actual.demora)
                Nodo_actual=Nodo_actual.siguiente

        #print("FINAL ORDENAMIENTO DE LA BURBUJA")    
    def ordenar_por_llegada(self): 
        if self.inicio==None:
            return
        listaclientes=self.inicio
        i=0
        #print("ORDENAMIENTO POR LLEGADA UTILIZANDO BUBBLESORT")
        while(listaclientes.siguiente!=None):
            temp2=listaclientes.siguiente
            while(temp2!=None):
                if(listaclientes.llegada>temp2.llegada):
                    aux1=listaclientes.ID
                    aux2=listaclientes.tipo
                    aux3=listaclientes.preferencia
                    aux4=listaclientes.llegada
                    aux5=listaclientes.demora
                    listaclientes.ID=temp2.ID
                    listaclientes.tipo=temp2.tipo
                    listaclientes.preferencia=temp2.preferencia
                    listaclientes.llegada=temp2.llegada
                    listaclientes.demora=temp2.demora
                    temp2.ID=aux1
                    temp2.tipo=aux2
                    temp2.preferencia=aux3
                    temp2.llegada=aux4
                    temp2.demora=aux5

                temp2=temp2.siguiente
            i+=1        
         #   print("ITERACIÓN DE ORDENAMIENTO DE BURBUJA N° ",i,":")
            listaclientes=listaclientes.siguiente
            Nodo_actual=self.inicio
            while Nodo_actual != None:
          #      print(Nodo_actual.ID,Nodo_actual.tipo,Nodo_actual.preferencia,Nodo_actual.llegada,Nodo_actual.demora)
                Nodo_actual=Nodo_actual.siguiente

        #print("FINAL ORDENAMIENTO DE LA BURBUJA")            
        
                #nodo = nodo.siguiente
   
def recorrer_lista(lista_g_p):
    while lista_g_p.inicio!=None:
        print(lista_g_p.inicio.ID,lista_g_p.inicio.tipo,lista_g_p.inicio.preferencia,lista_g_p.inicio.llegada,lista_g_p.inicio.demora)
        lista_g_p.inicio=lista_g_p.inicio.siguiente
#FUNCIONES PARA EL INPUT DE LOS DATOS
def leer_archivo_caja():
    Archivo= open("banco.in.txt","r")
    Archivo_caja=Archivo.readline()
    Datos_caja=Archivo_caja.split()

    total=Total_cajas=Datos_caja[0]
    g=Cajas_t=int(Datos_caja[1])
    t=Cajas_e=int(Datos_caja[2])
    e=Cajas_g=int(Datos_caja[3])
    return g,t,e
def leer_archivo_clientes(lista_g_p,lista_g_n,lista_t_p,lista_t_n,lista_e_p,lista_e_n):
    Archivo= open("banco.in.txt","r")
    Archivo_caja=Archivo.readline()
    Datos_caja=Archivo_caja.split()

    total=Total_cajas=Datos_caja[0]
    t=Cajas_t=int(Datos_caja[1])
    e=Cajas_e=int(Datos_caja[2])
    g=Cajas_g=int(Datos_caja[3])

    lista_cajas.agregar_inicio_cajas(total,t,e,g)
    #lista_cajas.recorrer_inicio_cajas()

    #Archivo_clientes=Archivo.readlines()
    Datos_clientes=Archivo.readlines()
    i=1
    #print(len(Datos_clientes))

    for clientes in Datos_clientes:
        if clientes!=None:
            atributo=clientes.split()
        #print(atributo[1]=="t" and int(atributo[2])==1)
        #print(atributo)
            
            if atributo[1]=="t" and int(atributo[2])==1:
                ID,tipo,preferencia,llegada,demora =int(atributo[0]),atributo[1],int(atributo[2]),int(atributo[3]),int(atributo[4])
                lista_t_p.agregar_inicio_clientes(ID,tipo,preferencia,llegada,demora)

            elif atributo[1]=="t" and int(atributo[2])==0:
                ID,tipo,preferencia,llegada,demora =int(atributo[0]),atributo[1],int(atributo[2]),int(atributo[3]),int(atributo[4])
                lista_t_n.agregar_inicio_clientes(ID,tipo,preferencia,llegada,demora)

            elif atributo[1]=="g" and int(atributo[2])==1:
                ID,tipo,preferencia,llegada,demora =int(atributo[0]),atributo[1],int(atributo[2]),int(atributo[3]),int(atributo[4])
                lista_g_p.agregar_inicio_clientes(ID,tipo,preferencia,llegada,demora)
            
            elif atributo[1]=="g" and int(atributo[2])==0:
                ID,tipo,preferencia,llegada,demora =int(atributo[0]),atributo[1],int(atributo[2]),int(atributo[3]),int(atributo[4])
                lista_g_n.agregar_inicio_clientes(ID,tipo,preferencia,llegada,demora)

            elif atributo[1]=="e" and int(atributo[2])==1:
                ID,tipo,preferencia,llegada,demora =int(atributo[0]),atributo[1],int(atributo[2]),int(atributo[3]),int(atributo[4])
                lista_e_p.agregar_inicio_clientes(ID,tipo,preferencia,llegada,demora)
            
            elif atributo[1]=="e" and int(atributo[2])==0:
                ID,tipo,preferencia,llegada,demora =int(atributo[0]),atributo[1],int(atributo[2]),int(atributo[3]),int(atributo[4])
                lista_e_n.agregar_inicio_clientes(ID,tipo,preferencia,llegada,demora)
            i+=1
        else: break

    
    lista_g_p.ordenar_por_llegada()
    lista_g_n.ordenar_por_llegada()
    lista_t_p.ordenar_por_llegada()
    lista_t_n.ordenar_por_llegada()
    lista_e_p.ordenar_por_llegada()
    lista_e_n.ordenar_por_llegada()
#FUNCIONES PARA OPERACIONES EN EL BANCO(ESTO SE REPLICA 3 VECES, PARA LOS 3 TIPOS DE CLIENTES)
def recorrer_cola(tamaño_caja_g,caja_g,cola_preferentes_g):
     cola_p_g=cola_preferentes_g.inicio
     while cola_p_g!=None:#RECORRER COLA PREFERENTE
             #print("TAMAÑO CAJA: ",lista_cajas.size)
            # print("cliente preferente ",cola_preferente!=None,tamaño_caja>lista_cajas.size,lista_cajas.size,cola_preferente.ID)
            if tamaño_caja_g>caja_g.size:#PREGUNTA SI HAY CAJAS DISPONIBLES
                    #CASO EN QUE HAY CAJAS DISPONIBLES, CLIENTE ACTUAL ENTRA EN CAJA, Y SALE DE LA FILA  
                at1,at2,at3,at4,at5=cola_p_g.ID,cola_p_g.tipo,cola_p_g.preferencia,cola_p_g.llegada,cola_p_g.demora
                caja_g.agregar_ultimo_clientes(at1,at2,at3,at4,at5)#AGREGAR A CAJA     
                cola_preferentes_g.eliminar_inicio()#ELIMINAR DE COLA 
    
            else:#SI NO HAY CAJAS DISPONIBLES, HORARIO DE ATENCION AUMENTA
                interruptor=False
              
            cola_p_g=cola_p_g.siguiente
def recorrer_clientes(tamaño_caja_g,caja_g,cola_preferentes_g,lista_g_p,i):
    cliente_actual_p=lista_g_p.inicio
    while (cliente_actual_p!=None) :#ESTADO DE CADA CLIENTE PREFERENTE QUE LLEGÓ RECÍEN O AÚN NO LLEGA
            #CLIENTES QUE NO HAN LLEGADO O LLEGARON RECIÉN
            if cliente_actual_p.llegada-i==0 :#LLEGÓ CLIENTE PREFERENTE, preguntar si hay cajas disponibles(EXISTEN 2 POSIBILIDADES:MANDAR A CAJA O MANDAR A COLA PREFERENTE) 
                at1,at2,at3,at4,at5=cliente_actual_p.ID,cliente_actual_p.tipo,cliente_actual_p.preferencia,cliente_actual_p.llegada,cliente_actual_p.demora 
                #print(cliente_actual_p.ID,cliente_actual_p.tipo,cliente_actual_p.preferencia,cliente_actual_p.llegada,cliente_actual_p.demora)
                if tamaño_caja_g>caja_g.size:#PREGUNTA SI HAY CAJAS DISPONIBLES
                    
                    caja_g.agregar_ultimo_clientes(at1,at2,at3,at4,at5)#AGREGAR A CAJA
                else:
                   
                    cola_preferentes_g.agregar_ultimo_clientes(at1,at2,at3,at4,at5)
                lista_g_p.eliminar_inicio()
              
            cliente_actual_p=cliente_actual_p.siguiente 
def opera_caja(caja_g,atendidos_g):
    clientes_en_caja=caja_g.inicio 
    if clientes_en_caja!=None:
        caja=clientes_en_caja.contador_cola=0
    while clientes_en_caja!=None:
            caja+=1
            clientes_en_caja.contador_cola=caja
            clientes_en_caja.contador=clientes_en_caja.contador+1#EMPIEZA A AUMENTAR EL TIEMPO EN CAJA UNA VEZ QUE EL CLIENTE ENTRA A LA LISTA_CAJA,              contador=clientes_en_caja.contador
            #print("ID del cliente en caja: ",clientes_en_caja.ID,", Demora: ",clientes_en_caja.demora,",tiempo en caja: ",clientes_en_caja.contador,", tipo: ",clientes_en_caja.tipo,", preferencia: ",clientes_en_caja.preferencia)
            if (clientes_en_caja.contador)==clientes_en_caja.demora:#SI TIEMPO EN CAJA ES IGUAL A LA DEMORA, SALE DE LA CAJA
                #CREAR METODO DE ELIMINAR A X CLIENTE DE LA LISTA CAJA  
                at1,at2,at3,at4,at5=clientes_en_caja.ID,clientes_en_caja.tipo,clientes_en_caja.preferencia,clientes_en_caja.llegada,clientes_en_caja.demora
                atendidos_g.agregar_inicio_atendidos(at1,at2,at3,at4,at5,caja)
                caja_g.eliminar_cliente_segun_dato(clientes_en_caja.ID)
                #print("CLIENTE ATENDIDO: ",atendidos_g.inicio.ID)
                                            
            clientes_en_caja=clientes_en_caja.siguiente  
#FUNCION PARA ASIGNAR CLIENTES A CAJAS DE OTRO TIPO(RECORRE SOLO LAS COLAS)
def otras_cajas(tamaño_caja_t,caja_t,cola_normal_t,cola_preferentes_t,tamaño_caja_e,caja_e,cola_normal_e,cola_preferentes_e,cola_preferentes_g):
    if (tamaño_caja_t>caja_t.size and cola_normal_t.size==0 and cola_preferentes_t.size==0) or (tamaño_caja_e>caja_e.size and cola_preferentes_e.size==0 and cola_normal_e.size==0):
        cola_p_g=cola_preferentes_g.inicio
        while cola_p_g!=None:#RECORRER COLA PREFERENTE
             #print("TAMAÑO CAJA: ",lista_cajas.size)
            # print("cliente preferente ",cola_preferente!=None,tamaño_caja>lista_cajas.size,lista_cajas.size,cola_preferente.ID)
                
                if tamaño_caja_t>caja_t.size and cola_normal_t.size==0 and cola_preferentes_t.size==0:#PREGUNTA SI HAY CAJAS DISPONIBLES
                    #CASO EN QUE HAY CAJAS DISPONIBLES, CLIENTE ACTUAL ENTRA EN CAJA, Y SALE DE LA FILA  
                    at1,at2,at3,at4,at5=cola_p_g.ID,cola_p_g.tipo,cola_p_g.preferencia,cola_p_g.llegada,cola_p_g.demora
                    caja_t.agregar_ultimo_clientes(at1,at2,at3,at4,at5)#AGREGAR A CAJA t    
                    cola_preferentes_g.eliminar_inicio()#ELIMINAR DE COLA 
                elif tamaño_caja_e>caja_e.size and cola_preferentes_e.size==0 and cola_normal_e.size==0:
                    at1,at2,at3,at4,at5=cola_p_g.ID,cola_p_g.tipo,cola_p_g.preferencia,cola_p_g.llegada,cola_p_g.demora
                    caja_e.agregar_ultimo_clientes(at1,at2,at3,at4,at5)#AGREGAR A CAJA t    
                    cola_preferentes_g.eliminar_inicio()#ELIMINAR DE COLA 
                else:#SI NO HAY CAJAS DISPONIBLES, HORARIO DE ATENCION AUMENTA
                    interruptor=False
                #print("CLIENTE PREFERENTE: ",cola_p_g.ID,", EN COLA")
                cola_p_g=cola_p_g.siguiente
#FUNCIONES PARA EL ESTADO FINAL, SE UTILIZAN UNA VEZ SIMULADO EL FUNCIONAMIENTO DEL BANCO EN DETERMINADO INSTANTE
#TAMBIÉN SE UTILIZAN PARA GUARDAR EL INSTANTE FINAL UNA VEZ TERMINADO EL PROGRAMA(OUTPUT)
def final_caja(caja_g,guardar_archivo,cajas_anteriores):
    caja1=caja_g.inicio
    while caja1!=None:
        caja1.contador_cola=caja1.contador_cola+cajas_anteriores
        print(caja1.contador_cola," ",caja1.ID," está siendo atendido en caja: ",caja1.contador_cola ," tiempo en caja: ",caja1.contador,", demora: ",caja1.demora,", tipo:",caja1.tipo,", preferencia:",caja1.preferencia)
        guardar_archivo.write(str(caja1.contador_cola)+' '+str(caja1.ID) + '\n')
        caja1=caja1.siguiente       
def final_cola(cola_normal_g,cola_preferentes_g,guardar_archivo):
    if cola_normal_g.size!=0 or cola_preferentes_g.size!=0:
        cola1=cola_preferentes_g.inicio
        while cola1!=None:
            cola1.contador_cola+=1
            print("   ",cola1.ID," está esperando su turno, tiempo en cola: ",cola1.contador_cola,",demora: ",cola1.demora,",tipo: ",cola1.tipo,", preferencia: ",cola1.preferencia)
            guardar_archivo.write(str(cola1.ID) + ' ')
            cola1=cola1.siguiente
        cola1=cola_normal_g.inicio
        while cola1!=None:
            cola1.contador_cola+=1
            print("   ",cola1.ID," está esperando su turno, tiempo en cola: ",cola1.contador_cola,",demora: ",cola1.demora,",tipo: ",cola1.tipo,", preferencia: ",cola1.preferencia)
            guardar_archivo.write(str(cola1.ID) + ' ')
            cola1=cola1.siguiente
    else:
        guardar_archivo.write('-')        
def final_atendidos(atendidos_g,guardar_archivo,i,cajas_anteriores):
    atendido=atendidos_g.inicio
    while atendido!=None:
        atendido.caja=atendido.caja+cajas_anteriores
        print("   ",atendido.ID," ya se atendió en caja ",atendido.caja, ",demora: ",atendido.demora,", tipo: ",atendido.tipo,", preferencia: ",atendido.preferencia)
        guardar_archivo.write(str(atendido.ID) + ' ')
        atendido=atendido.siguiente       
#MUESTRA EL ESTADO FINAL DEL INSTANTE ESCOGIDO Y GUARDA LOS DATOS EN UN ARCHIVO TXT
def estado_final(i):
    guardar_archivo=open("banco.out.txt","w")
    print("CLIENTES EN CAJA G")
    cajas_anteriores=0
    final_caja(caja_g,guardar_archivo,cajas_anteriores)
    
    print("CLIENTES EN CAJA T") 
    cajas_anteriores=tamaño_caja_g
    final_caja(caja_t,guardar_archivo,cajas_anteriores)

    print("CLIENTES EN CAJA E")
    cajas_anteriores=cajas_anteriores + tamaño_caja_t
    final_caja(caja_e,guardar_archivo,cajas_anteriores)
    guardar_archivo.write('\n')
    guardar_archivo.write('\n')

    print("CLIENTES EN COLA G")
    final_cola(cola_normal_g,cola_preferentes_g,guardar_archivo)
    guardar_archivo.write('\n')

    print("CLIENTES EN COLA T")
    final_cola(cola_normal_t,cola_preferentes_t,guardar_archivo)
    guardar_archivo.write('\n')

    print("CLIENTES EN COLA E")
    final_cola(cola_normal_e,cola_preferentes_e,guardar_archivo)
    guardar_archivo.write('\n')
    
    
    if atendidos_g.size!=0 or atendidos_e.size!=0 or atendidos_t.size!=0:
        print("ATENDIDOS CAJA G")
        cajas_anteriores=0
        final_atendidos(atendidos_g,guardar_archivo,i,cajas_anteriores)
        print("ATENDIDOS CAJA T")
        cajas_anteriores=tamaño_caja_g
        final_atendidos(atendidos_t,guardar_archivo,i,cajas_anteriores)
        print("ATENDIDOS CAJA E")
        cajas_anteriores=cajas_anteriores + tamaño_caja_t
        final_atendidos(atendidos_e,guardar_archivo,i,cajas_anteriores)
    else:
        guardar_archivo.write('-') 
#AQUI SE EJECUTA LA SIMULACION DEL BANCO(INLCUYE LAS OPERACIONES EN BANCO) Y EL ESTADO FINAL
def banco(tiempo,lista_g_p,lista_g_n,lista_t_p,lista_t_n,lista_e_p,lista_e_n,tamaño_caja_g,tamaño_caja_t,tamaño_caja_e,cola_preferentes_g,cola_preferentes_t,cola_preferentes_e,cola_normal_g,cola_normal_t,cola_normal_e,caja_g,caja_t,caja_e,atendidos_g,atendidos_t,atendidos_e):#AQUI SE EJECUTA LA SIMULACION DEL BANCO
    i=0 
    interruptor=True
    interruptor2=False
    if tiempo==int(-1):#SI EL USUARIO INDICÓ QUE QUIERE VER EL ÚLTIMO INSTANTE DEL PROGRAMA
        interruptor2=True
        tiempo=i+1

    while i<=tiempo and interruptor==True:#ESTADO DE CLIENTES PARA CADA INSTANTE(0,1,2,3...)
        #print("-----------------------------------")
        #print("INSTANCIA ",i)
        #print("-----------------------------------")
        recorrer_cola(tamaño_caja_g,caja_g,cola_preferentes_g)  
        recorrer_clientes(tamaño_caja_g,caja_g,cola_preferentes_g,lista_g_p,i)
        recorrer_cola(tamaño_caja_g,caja_g,cola_normal_g)
        recorrer_clientes(tamaño_caja_g,caja_g,cola_normal_g,lista_g_n,i)
                             
        recorrer_cola(tamaño_caja_t,caja_t,cola_preferentes_t)   
        recorrer_clientes(tamaño_caja_t,caja_t,cola_preferentes_t,lista_t_p,i)
        recorrer_cola(tamaño_caja_t,caja_t,cola_normal_t)
        recorrer_clientes(tamaño_caja_t,caja_t,cola_normal_t,lista_t_n,i)
                 
        recorrer_cola(tamaño_caja_e,caja_e,cola_preferentes_e)
        recorrer_clientes(tamaño_caja_e,caja_e,cola_preferentes_e,lista_e_p,i)  
        recorrer_cola(tamaño_caja_e,caja_e,cola_normal_e) 
        recorrer_clientes(tamaño_caja_e,caja_e,cola_normal_e,lista_e_n,i)
        
        otras_cajas(tamaño_caja_t,caja_t,cola_normal_t,cola_preferentes_t,tamaño_caja_e,caja_e,cola_normal_e,cola_preferentes_e,cola_preferentes_g)
        otras_cajas(tamaño_caja_g,caja_g,cola_normal_g,cola_preferentes_g,tamaño_caja_e,caja_e,cola_normal_e,cola_preferentes_e,cola_preferentes_t)    
        otras_cajas(tamaño_caja_g,caja_g,cola_normal_g,cola_preferentes_g,tamaño_caja_t,caja_t,cola_normal_t,cola_preferentes_t,cola_preferentes_e)
        otras_cajas(tamaño_caja_t,caja_t,cola_normal_t,cola_preferentes_t,tamaño_caja_e,caja_e,cola_normal_e,cola_preferentes_e,cola_normal_g)
        otras_cajas(tamaño_caja_g,caja_g,cola_normal_g,cola_preferentes_g,tamaño_caja_e,caja_e,cola_normal_e,cola_preferentes_e,cola_normal_t) 
        otras_cajas(tamaño_caja_g,caja_g,cola_normal_g,cola_preferentes_g,tamaño_caja_t,caja_t,cola_normal_t,cola_preferentes_t,cola_normal_e)
            

        #print("***********************************************************************************")
        #print("CLIENTES EN CAJA G: ")
        opera_caja(caja_g,atendidos_g)

        #print("***********************************************************************************")
        #print("CLIENTES EN CAJA T: ")
        opera_caja(caja_t,atendidos_t)
        
        #print("***********************************************************************************")
        #print("CLIENTES EN CAJA E: ")
        opera_caja(caja_e,atendidos_e)

        if lista_g_p.size>0 or lista_g_n.size>0 or  lista_t_p.size>0 or  lista_t_n.size>0 or lista_e_p.size>0 or lista_e_n.size>0 or caja_g.size>0 or caja_t.size>0 or caja_e.size>0 or cola_normal_e.size>0 or cola_normal_g.size>0 or cola_normal_t.size>0 or cola_preferentes_e.size>0 or cola_preferentes_g.size>0 or cola_preferentes_t.size>0:
            pass
        else:
            interruptor=False
        if interruptor2==True:#SI EL CLIENTE QUIERE VER EL INSTANTE FINAL, ENTONCES "tiempo" TIENE QUE SER SIEMPRE MAYOR QUE i, ASI EL CICLO SE DETIENE SOLO CUANDO LLEGA AL FINAL Y NO ANTES
            tiempo+=1
        
        i+=1
    
         
    print("----------------------------------------------")    
    print("-----------------------------------------------")
    print("ESTADO FINAL INSTANCIA ",i-1)
    estado_final(i)
  
    #REINICIAR TODAS LAS LISTAS

print("¡BIENVENIDO AL PROGRAMA SIMULA TU BANCO!")

tiempo=0
pregunta=2

while tiempo>=0 and pregunta!=0:

    while True :
        try :
            print("Si desea ver el instante final ingrese -1, de lo contrario solo ingrese el instante")
            tiempo = int( input ( "Ingresar aquí: " ) )
            while tiempo<0 and tiempo!=-1:
                print("Por favor ingrese un instante de tiempo válido")
                tiempo = int( input ( "Ingresar aquí: " ) )
            break
        except :
            print ( " Oops ! Ingreso no válido . Intente nuevamente ... " )
    
    lista_cajas=Lista()
    #Aquí se almacenan los clientes que aun no han llegado o llegan en el instante t(es decir, que llegaron recien)
    #Van saliendo de las listas a medida que van entrando en cola o en caja
    lista_g_p=Lista()
    lista_g_n=Lista()
    lista_t_p=Lista()
    lista_t_n=Lista()
    lista_e_p=Lista()
    lista_e_n=Lista()
    #Clientes que están en cola, entran en caja y desaparecen de la cola cuando hay cupo disponible 
    cola_preferentes_g=Lista()
    cola_preferentes_t=Lista()
    cola_preferentes_e=Lista()
    cola_normal_g=Lista()
    cola_normal_t=Lista()
    cola_normal_e=Lista()
    #Aquí se almacenan los clientes que cumplen su tiempo en caja
    atendidos_g=Lista()
    atendidos_t=Lista()
    atendidos_e=Lista()
    #Aqui se almacenan los clientes que están en caja, su tiempo en esta depende de su tiempo de demora una vez que entran, luego salen de caja
    caja_g=Lista()
    caja_t=Lista()
    caja_e=Lista()

    tamaño_caja_g,tamaño_caja_t,tamaño_caja_e=leer_archivo_caja()
    leer_archivo_clientes(lista_g_p,lista_g_n,lista_t_p,lista_t_n,lista_e_p,lista_e_n)
    
    print("")
    print("ESTADO DE CLIENTES PARA CADA INSTANTE DE TIEMPO")
    print("")
 
    print("NUMERO TOTAL DE CLIENTES: ",lista_g_p.size + lista_g_n.size + lista_t_p.size + lista_t_n.size + lista_e_p.size + lista_e_n.size)    
        
    banco(tiempo,lista_g_p,lista_g_n,lista_t_p,lista_t_n,lista_e_p,lista_e_n,tamaño_caja_g,tamaño_caja_t,tamaño_caja_e,cola_preferentes_g,cola_preferentes_t,cola_preferentes_e,cola_normal_g,cola_normal_t,cola_normal_e,caja_g,caja_t,caja_e,atendidos_g,atendidos_t,atendidos_e) 
  
    while True :
        try :
            print("   ")
            pregunta=int(input("Para ver otro instante pulse 1, para terminar pulse 0: "))
            while pregunta!=0 and pregunta!=1 and pregunta!=-1:
                print("Por favor ingresar una de las opciones dadas:")
                pregunta=int(input("Para ver otro instante pulse 1, para terminar pulse 0: "))

            break
        except :
            print ( " Oops ! Ingreso no válido . Intente nuevamente ... " )
    tiempo=0

    if pregunta==0:
        print("HAZ FINALIZADO EL PROGRAMA, ¡HASTA PRONTO!")

    

    

        
    
   

