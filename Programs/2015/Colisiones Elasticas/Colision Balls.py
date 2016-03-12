import pygame,pygame.mixer
from copy import deepcopy
from game_edit import edit,get_tuple,get_bool
from random import random
from math import sqrt,hypot,pi


def load_config():
    """ Permite obtener datos de el archivo config
    """
    global Width,Height,color_palabras,color_particulas1,color_particulas2,FPS,dt,color_fondo,Kv_max,Kv_min,Kr_max,Kr_min,Kd,n,merge,bound,color_medio,Max_Points
    Width = get_tuple("Data\config.txt",0)[0]
    Height = get_tuple("Data\config.txt",0)[1]
    FPS = get_tuple("Data\config.txt",1)[0]
    dt = get_tuple("Data\config.txt",2)[0]
    color_particulas1 = get_tuple("Data\config.txt",3)
    color_particulas2 = get_tuple("Data\config.txt",4)
    color_palabras = get_tuple("Data\config.txt",5)
    color_fondo = get_tuple("Data\config.txt",6)
    Kv_max = get_tuple("Data\config.txt",7)[0]
    Kv_min = get_tuple("Data\config.txt",8)[0]
    Kr_max = get_tuple("Data\config.txt",9)[0]
    Kr_min = get_tuple("Data\config.txt",10)[0]
    Kd = get_tuple("Data\config.txt",11)[0]
    n = get_tuple("Data\config.txt",12)[0]
    merge = get_bool("Data\config.txt",13)
    bound = get_bool("Data\config.txt",14)
    Max_Points = get_tuple("Data\config.txt",15)[0]
    u = []
    for i in range(3):
        u.append(int((color_particulas1[i]+color_particulas2[i])//2))
    color_medio = tuple(u)    
    print("\n**Datos cargados exitosamente**")
    
def out(pos,r):
    """ Recibe una posicion
    y un radio para determinar si un circulo esta afuera del cuadrado
    """
    if pos[0]-r > L or pos[1]-r > L:
        return True
    if pos[0]+r < 0 or pos[1]+r < 0:
        return True
    return False

def to_display(pos,L):
    """ Recibe una posicion y el largo de un cuadrado(logico) y retorna la posicion en donde se tiene que renderizar 
    """
    return [int(Margen_x +(pos[0]*Largo_caja/L)),int(Margen_y+(pos[1]*Largo_caja/L))]
def to_logic(pos,L):
    """ Recive una posicion de el display y lo pasa a un punto del cuadrado(logico)
    """
    return [((L*(pos[0]-Margen_x))/Largo_caja),((L*(pos[1]-Margen_y))/Largo_caja)]
    

def norm_coef(coef):
    """ Acota el coeficiente de restitucion, para que no sean colisiones super elasticas
    """
    if coef > 1:
        return 1
    elif coef < 0:
        return 0
    return coef

def general_d(pos1,pos2):
    """ Distancia entre dos puntos
    """
    u = 0
    for i in range(2):
        u+= (pos1[i] - pos2[i])**2
    return sqrt(u)    

def d(P1,P2):
    """ Distancia entre dos particulas
    """
    return general_d(P1.pos,P2.pos)

def atraccion(P1,P2,G):
    """ Atraccion gravitatoria entre dos particulas con una constante G
    retorna aceleracion que experimenta P1
    """
    for i in range(2):
        delta = P2.pos[i] - P1.pos[i]
        P1.a[i] += (P2.m*G*delta)/(r**3)# r = d(P1,P2), ya calculado (para reducir cantidad de calculos)
        
def merge_particulas(P1,P2,particulas):
    """ Permite que dos particulas se unan en una
    """
    P3_color = []   
    for i in range(3):
        P3_col = (P1.color[i] + P2.color[i])//2
        P3_color.append(int(P3_col))   
    if P1.m**2/P1.r < P2.m**2/P2.r:
        P1,P2 = P2,P1
    P1d = ((P1.m/P1.r)) 
    P1.coef = (P1.coef + P2.coef)/2    
    for i in range(2):
        P1.v[i] = ((P1.v[i]*P1.m) + (P2.v[i]*P2.m)) / (P1.m + P2.m)
    P1.m += P2.m
    P1.r = P1.m/P1d
    P1.color = P3_color
    particulas.remove(P2)
    
def gravedad_caja(P,g):
    """ Gravedad de la caja sobre una particula
    """
    for i in range(2):
        P.a[i] += g[i]    
        
def colisionar(P1,P2):
    """ Colision entre dos particulas, puede ser inelastica o elastica
    y ademas evita que las particulas se queden pegadas   
    """
    C = (P1.coef + P2.coef) / 2
    E = r-(P1.r + P2.r)# r = d(P1,P2), ya calculado
    for i in range(2):
        vf1 = (C*P2.m*(P2.v[i]-P1.v[i]) + P1.m * P1.v[i] + P2.m * P2.v[i]) / (P1.m + P2.m)
        P2.v[i] += (P1.m/P2.m) * (P1.v[i]-vf1)
        P1.v[i] = vf1
        collision_pos = ((P1.pos[i] * P2.r) + (P2.pos[i] * P1.r)) / (P2.r + P1.r)
        error = E * (P1.pos[i] - collision_pos)/(P1.r) # para evitar que queden atrapados juntos
        if P1.m < P2.m:
            P1.pos[i] -= 2*error
        else:    
            P2.pos[i] += 2*error

def toggle(boolean):
    """ invierte boleano
    """
    if boolean:
        return False
    else:
        return True
    
def neg():
    """ permite que la direccion sea aleatoria
    """
    u = random()
    if u < 0.5:
        return -1
    return 1

def message_to_screen(msg,color,x,y):
    """ Recibe un mensaje con un color y lo pone en la pantalla en una posicion indicada
    """
    screen_text = font.render(msg, True, color)
    display.blit(screen_text, (x,y))

def pause():
    """ Pausa simulacion
    Sonido Incluido
    """
    message_to_screen("Pausa :3",color_palabras,Width//2,int((Height//2)+Ly))
    pygame.display.update()
    sound = pygame.mixer.Sound("Data\smb_pause.wav")
    pygame.mixer.music.pause()
    pygame.mixer.Sound.play(sound)
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                simulacion = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
                    pygame.mixer.music.unpause()
                    
#-------------------------------------------------------------------------------------------------------
                    
class Particula:
    """ Particula que tiene como atributos
    posicion, Velocidad, Aceleracion, Masa, Radio, Color, Coeficiente de restitucion y
    Cola

    Se puede saber si una posicion esta dentro de ella,
    Puede rebotar si se le da una pared,
    Se desplaza y acelera
    Puede colisionar y unirse con otra particula
    Es atraida a todas las particulas
    y por ultimo puede tener una propia cola
    """
    def __init__(self,pos,velocidad,masa,radio,coef,color):
        self.pos = pos
        self.v = velocidad
        self.m = masa
        self.r = abs(radio)
        self.coef = norm_coef(coef)
        self.color = color
        self.cola = [to_display(deepcopy(self.pos),L)]
        
    def adentro(self,pos):
        """ Determina si una posicion esta adentro
        """
        u = 0
        for i in range(2):
            u += (self.pos[i] - pos[i])**2
        if u <= self.r**2:
            return True
        return False

    def get_cola(self):
        """ Obtiene cola, con un numero maximo de puntos
        """   
        nueva_parte = to_display(deepcopy(self.pos),L)
        self.cola.insert(0,nueva_parte)
        while len(self.cola) > Max_Points:
            last = self.cola[-1]
            self.cola.remove(last)
            
    def desplazar(self,dt):
        """ Se desplaza en intervalos dt
        """       
        for i in range(2):
            self.pos[i] += self.v[i]*dt
            
    def acelerar(self,dt):
        """ Acelera en intervalos dt
        """
        for i in range(2):
            self.v[i] += self.a[i]*dt

    def rebotar_pared(self,L):
        """ Rebota en una pared de largo L
        y ademas devuelve la particula si se encuentra
        fuera de el contenedor, cada colision es ponderada por
        el coeficiente de restitucion
        """    
        for i in range(2):
            if self.pos[i]-self.r <= 0:
                self.v[i] *= -self.coef
                d = -self.pos[i]+self.r
                self.pos[i] += d  
            elif self.pos[i]+self.r >= L:
                self.v[i] *= -self.coef
                d = L-(self.pos[i]+self.r)
                self.pos[i] += d
    
    def comprobar_colision(self,particulas,merge):
        """ Comprueba si la particula self, colisiono con alguna
        particula diferente de ella en una lista, y dependiendo de la configuracion
        puede colisionar o unirse
        """
        for particula in particulas:
            if particula is not self:
                global r
                r = d(self,particula)    
                if r <= self.r + particula.r:
                    if not merge:
                        colisionar(self,particula)
                    else:
                        merge_particulas(self,particula,particulas)
                
    def atraccion_neta(self,particulas,G,g):
        """ Asigna una aceleracion neta a la particula
        que depende de la atraccion gravitatoria y la gravedad de la caja
        """
        self.a = [0,0]
        gravedad_caja(self,g)
        if G != 0:
            for particula in particulas:
                if particula is not self:
                    global r
                    r = d(self,particula)
                    if r > self.r*2 + particula.r*2:
                        atraccion(self,particula,G)
                                    
class Caja:
    """ Caja que contiene consigo objetos particulas que interaccionan entre ellas y la caja.
    Tiene como atributos ademas: un largo, una aceleracion de gravedad como si se tratase de la tierra
    una constante gravitatoria, y puede controlar cosas como los tipos de colisiones, puede permitir
    que hayan colas y campos vectoriales, o que existan o no limites en la caja.
    
    """
    def __init__(self,L,g = [0,0],G = 0,particulas = [], merge= True, bound = False,colas = False):
        self.L = L 
        self.g = g
        self.G = G
        self.particulas = particulas
        self.vector_field = False
        self.merge = merge
        self.bound = bound
        self.colas = colas
    
    def generar(self, n, velocidad, radio, densidad, coef):
        """ Genera n particulas de manera aleaotira dependiendo de los limites que se le dan
        """ 
        v_max = velocidad[0]
        v_min = velocidad[1]
        r_max = radio[0]
        r_min = radio[1]
        for i in range(n):
            pos = []
            v = []
            r = random()*(r_max-r_min)+ r_min
            m = r * densidad   
            for k in range(2):
                v_eje = ((random()*(v_max-v_min))+v_min)*neg()
                pos_eje = random()*self.L
                v.append(v_eje)
                pos.append(pos_eje)
            u = Particula(pos,v,m,r,coef,color_particulas1)
            self.particulas.append(u)
            
    def agregar(self,pos,velocidad,masa,radio,coef,color):
        """ Agrega una particula con determinadas caracteristicas
        """
        p = Particula(pos,velocidad,masa,radio,coef,color)
        self.particulas.append(p)
        
    def update_logic(self,dt):
        """ Actualiza todos los parametros logicos de las particulas dentro de la caja
        """
        for particula in self.particulas:
            particula.comprobar_colision(self.particulas,self.merge)
            if self.bound:
                particula.rebotar_pared(self.L)
            particula.desplazar(dt)
            particula.atraccion_neta(self.particulas,self.G,self.g)
            particula.acelerar(dt)

    def select(self,pos):
        """ Retorna una particula selecionada en una posicion 
        """
        for particula in self.particulas:
            if particula.adentro(pos) == True:
                return particula
            
    def agarrar(self,pos,dv):
        """ Permite acelerar particulas de una posicion pos con un dv
        """ 
        for particula in self.particulas:
            if particula.adentro(pos) == True:
                for i in range(2):
                    particula.v[i] += dv[i]
                    
    def detener(self,pos):
        """ Detiene una particula de una posicion determinada
        """
        for particula in self.particulas:
            if particula.adentro(pos) == True:
                for i in range(2):
                    particula.v[i] = 0
                    
    def eliminar(self,pos):
        """ Elimina una particula en una determinada posicion
        """
        for particula in self.particulas:
            if particula.adentro(pos) == True:
                self.particulas.remove(particula)                
                    
    def probe(self,pos):
        """ Permite calcular como una particula de prueba aceleraria en un punto determinado
        """
        a = [0,0]
        try:
            for particula in self.particulas:
                r = general_d(pos,particula.pos)
                for i in range(2):
                    delta = particula.pos[i] - pos[i]
                    a[i] += (particula.m*self.G*delta)/(r**3) + self.g[i]
            return a
        except ZeroDivisionError:
            return "infinte","infinte"
        
    def cambiar_coef(self,d):
        """ Permite cambiar el coeficiente de restitucion de todas las particulas
        """
        for particula in self.particulas:
            particula.coef += d
            if particula.coef > 1:
                particula.coef = 1
            elif particula.coef < 0:
                particula.coef = 0
                
    def rapidez_promedio(self):
        """ Retorna rapidez promedio 
        """
        v = 0
        i = 0
        for particula in self.particulas:
            u = 0
            for i in range(2):
                u += particula.v[i]**2
            v+= sqrt(u)
            i += 1
        try:
            return v/i
        except:
            return 0            
                    
    def get_info(self,particula):
        """ Muestra en pantalla algunos parametros de una particula selecionada
        """
        x1 = Margen_x
        try:
            pos_plot ="Pos:"+"(" + str("{:.1e}".format(round(particula.pos[0]))) + "," + str("{:.2e}".format(particula.pos[1]))+")"
            v_plot = "V:"+"(" + str("{:.1e}".format(round(particula.v[0]))) + "," + str("{:.2e}".format(particula.v[1]))+")"
            a_plot = "A:"+"("+str("{:.1e}".format(round(particula.a[0]))) + "," + str("{:.2e}".format(particula.a[1]))+")"
            m_plot = "M:"+str("{:.1e}".format(round(particula.m)))
            r_plot = "R:"+str("{:.1e}".format(round(particula.r)))
            x2 = x1 + len(pos_plot)*Kx
            x3 = x2 + len(v_plot)*Kx
            x4 = x3 + len(a_plot)*Kx
            x5 = x4 + len(m_plot)*Kx
            message_to_screen(pos_plot,color_palabras,x1,Margen_y//10)
            message_to_screen(v_plot,color_palabras,x2,Margen_y//10)
            message_to_screen(a_plot,color_palabras,x3,Margen_y//10)
            message_to_screen(m_plot,color_palabras,x4,Margen_y//10)
            message_to_screen(r_plot,color_palabras,x5,Margen_y//10)
            p = to_display((particula.pos[0],particula.pos[1]),L)
            r = int(particula.r*Largo_caja/(self.L*4))
            pygame.draw.circle(display,color_particulas2,p,r,r//2)
    
        except:
            pos_plot = "Pos: --"
            v_plot = "V: --"
            a_plot = "A: --"
            m_plot = "M: --"
            r_plot = "R: --"
            x2 = x1 + len(pos_plot)*Kx
            x3 = x2 + len(v_plot)*Kx
            x4 = x3 + len(a_plot)*Kx
            x5 = x4 + len(m_plot)*Kx
            message_to_screen(pos_plot,color_palabras,x1,Margen_y//10)
            message_to_screen(v_plot,color_palabras,x2,Margen_y//10)
            message_to_screen(a_plot,color_palabras,x3,Margen_y//10)
            message_to_screen(m_plot,color_palabras,x4,Margen_y//10)
            message_to_screen(r_plot,color_palabras,x5,Margen_y//10)
            
    def get_vectorPoints(self):
        """ Muestra en pantalla un campo vectorial de la suma neta de las fuerzas
        """ 
        if (self.G != 0 and self.vector_field) or (self.g !=[0,0] and self.vector_field):
            r = self.L/(n*2)
            u = 4
            v = 2        
            for i in range(n):
                for k in range(n):
                    point = (int(r+(2*r*i)),int(r+(2*r*k)))
                    a = self.probe(point)
                    norm_a = sqrt(a[0]**2 + a[1]**2)
                    k = norm_a/Largo_caja*10
                    if k>=0.6:
                        k=0.6
                    try:
                        delta_x = k*a[0]*r/norm_a
                        delta_y = k*a[1]*r/norm_a
                        end_point = to_display((point[0]+delta_x,point[1]+delta_y),self.L)
                        beg_point = to_display((point[0]-delta_x,point[1]-delta_y),self.L)
                        x1 = (-a[0]*u - a[1]*v*k)/norm_a + end_point[0]
                        y1 = (-a[1]*u + a[0]*v*k)/norm_a + end_point[1]
                        x2 = (-a[0]*u + a[1]*v*k)/norm_a + end_point[0]
                        y2 = (-a[1]*u - a[0]*v*k)/norm_a + end_point[1]
                        p1 = (x1,y1)
                        p2 = (x2,y2)
                        pygame.draw.line(display,(0,0,0),end_point,beg_point)
                        pygame.draw.polygon(display, (0,0,0),(end_point,p1,p2))
                    except:
                        pass                
              
    def sim_start(self,dt,t = -1):
        """ Parte simulacion dentro de la caja
        """
        dt_inicial = deepcopy(dt)
        G_inicial = deepcopy(self.G)
        selected_particula = self.particulas[0]
        probe_pos = [self.L/2,self.L/2]

        #Parametros Default iniciales
        troll = False 
        press = False
        Up = False
        Down = False
        Right = False
        Left = False
        G_up = False
        G_down = False
        coef_up = False
        coef_down = False
        dt_up = False
        dt_down = False
        rojos = 0
        
        while t != 0:
            FpsA = clock.get_fps()
            if FpsA == 0:
                FpsA = 0.01
            N = len(self.particulas)
            if N == 0:
                coefEn = 1
            else:
                coefEn = self.particulas[0].coef
#------------------------------------------------------------------------------------------------------// Manejo Eventos            
            for event in pygame.event.get():
                posicion_mouse = pygame.mouse.get_pos()
                pos = to_logic(posicion_mouse,self.L) #Posicion normalizada acuerdo a la caja
                rel = pygame.mouse.get_rel()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    key = pygame.mouse.get_pressed()
                    if key == (1,0,0):
                        selected_particula = self.select(pos)
                        Vx = 0
                        Vy = 0
                        press = True
                    if key == (0,0,1) or key == (1,0,1):
                        self.detener(pos)
                if press == True:
                    Vx = rel[0]
                    Vy = rel[1]
                    v = [Vx,Vy]
                    self.agarrar(pos,v)
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    press = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        m = []
                        r = []
                        for particula in self.particulas:
                            m.append(particula.m)
                            r.append(particula.r)
                        try:
                            self.agregar(pos,[0,0],16*max(m), min(r),coefEn,color_particulas2)     
                            rojos += 1
                        except:
                            pass
                    if event.key == pygame.K_p:
                        pause()
                    if event.key == pygame.K_UP:
                        Up = True
                    if event.key == pygame.K_DOWN:
                        Down = True
                    if event.key == pygame.K_RIGHT:
                        Right = True
                    if event.key == pygame.K_LEFT:
                        Left = True
                    if event.key == pygame.K_w:
                        coef_up = True
                    if event.key == pygame.K_q:
                        coef_down = True
                    if event.key == pygame.K_x:
                        dt_up = True
                    elif event.key == pygame.K_z:    
                        dt_down = True
                    if event.key == pygame.K_s:
                        G_up = True
                    elif event.key == pygame.K_a:
                        G_down = True
                    if event.key == pygame.K_r:
                        self.g = [0,0]
                        dt = dt_inicial
                        self.G = G_inicial
                        for particula in self.particulas:
                            particula.coef = 1
                    if event.key == pygame.K_y:
                        self.G = 0
                    if event.key == pygame.K_t:
                        self.generar(1,((self.L*Kv_max),(self.L*Kv_min)),((self.L*Kr_max),(self.L*Kr_min)),Kd,coefEn)
                    if event.key == pygame.K_BACKSPACE:
                        self.eliminar(pos)
                    if event.key == pygame.K_h:
                        probe_pos = pos
                    if event.key == pygame.K_v:
                        self.vector_field = toggle(self.vector_field)
                    if event.key == pygame.K_m:
                        self.merge = toggle(self.merge)
                    if event.key == pygame.K_b:
                        self.bound = toggle(self.bound)
                    if event.key == pygame.K_c:
                        self.colas = toggle(self.colas)
                    if event.key == pygame.K_f:
                        dt = 0
                            
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        Up = False
                    elif event.key == pygame.K_DOWN:
                        Down = False
                    if event.key == pygame.K_RIGHT:
                        Right = False
                    elif event.key == pygame.K_LEFT:
                        Left = False

                    if event.key == pygame.K_w:
                        coef_up = False
                    elif event.key == pygame.K_q:
                        coef_down = False

                    if event.key == pygame.K_x:
                        dt_up = False
                    elif event.key == pygame.K_z:    
                        dt_down = False

                    if event.key == pygame.K_s:
                        G_up = False
                    elif event.key == pygame.K_a:
                        G_down = False
                
            if Up:
                self.g[1] -=5/FpsA
            if Down:
                self.g[1] +=5/FpsA
            if Right:
                self.g[0] +=5/FpsA
            if Left:
                self.g[0] -=5/FpsA

            if coef_up and coefEn<0.9999:
                self.cambiar_coef(0.45/FpsA)
            if coef_down and coefEn>0.0001:
                self.cambiar_coef(-0.45/FpsA)

            if dt_up:
                dt += 0.002/FpsA
            if dt_down:
                dt -= 0.002/FpsA
                if dt <= 0:
                    dt = 0
            if G_up:
                self.G += 50/FpsA
            if G_down:
                self.G -= 50/FpsA
#------------------------------------------------------------------------------------------------------// Manejo Eventos
#------------------------------------------------------------------------------------------------------// Display                
            display.fill(color_particulas1)
            pygame.draw.rect(display,color_fondo,(Margen_x,Margen_y,Largo_caja,Largo_caja))
            for particula in self.particulas:
                if not out(particula.pos,particula.r):
                    p = to_display((particula.pos[0],particula.pos[1]),self.L)
                    r = int(particula.r*Largo_caja/self.L)
                    pygame.draw.circle(display,particula.color,p,r)
                    if self.colas:
                        particula.get_cola()
                        pygame.draw.lines(display,color_medio,False,particula.cola)
                    else:
                        particula.cola = [deepcopy(to_display(particula.pos,L))]
                
            try:    
                v_promedio = self.rapidez_promedio()
                g_in_display = "g :("+str(round(self.g[0]*10)/10)+", "+str(round(self.g[1]*10)/10)+")"
                N_in_display = "NºBolas :"+str(N)
                V_in_display = "Rapidez media:" +str(round(v_promedio))
                Largo_in_display = "Largo caja:" +str(self.L)
                FPS_in_display = "FPS: "+str(round(FpsA))
                dt_in_display ="dt: " + str("{:.2e}".format(dt))
                G_in_display = "G: "+str("{:.2e}".format(self.G))
                probe_acceleration = self.probe(probe_pos)
                Probe_in_display ="Probe A:"+"(" + str("{:.2e}".format(round(probe_acceleration[0]))) + ", " + str("{:.2e}".format(probe_acceleration[0]))+")" 
                coef_in_display = "coef :"+str(round(self.particulas[0].coef*100)/100)
            except:
                pass
            try:
                message_to_screen(g_in_display,color_palabras,Margen_x//10,Margen_y)
                message_to_screen(N_in_display,color_palabras,Largo_caja+((11*Margen_x)//10),Margen_y)
                message_to_screen(V_in_display,color_palabras,Margen_x//10,Height - Margen_y + Ly) 
                message_to_screen(Largo_in_display,color_palabras,Largo_caja+((11*Margen_x)//10),Height - Margen_y + Ly)
                message_to_screen(FPS_in_display,color_palabras,Largo_caja+((11*Margen_x)//10),Height - Margen_y)
                message_to_screen(dt_in_display,color_palabras,Largo_caja+((11*Margen_x)//10),Margen_y + Ly)
                message_to_screen(G_in_display,color_palabras,Largo_caja+((11*Margen_x)//10),Margen_y + 2*Ly)
                message_to_screen(coef_in_display,color_palabras,Margen_x//10,Margen_y + Ly)
                message_to_screen(Probe_in_display,color_palabras,(Largo_caja/2)+Margen_x-(len(Probe_in_display)-10)*Kx,Height - (Margen_y/2))
                if self.merge:
                    m = "Merge"
                else:
                    m = "Collide"
                message_to_screen(m,color_palabras,Margen_x//10,Margen_y + Ly*4)
                if self.bound:
                    b = "Con Limte"
                else:
                    b = "Sin Limite"
                message_to_screen(b,color_palabras,Margen_x//10,Margen_y + Ly*5)
            except:
                pass
#------------------------------------------------------------------------------------------------------// Display
            
            self.update_logic(dt)
            self.get_info(selected_particula)
            self.get_vectorPoints()
            
            if (rojos >= 4) and not troll:
                troll = True
                pygame.mixer.music.play(-1)
            if troll:
                message_to_screen(":D",color_particulas2,Width//2,Height//2)

            pygame.display.update()    
            clock.tick(FPS)               
            t -= 1
            
        print("\n**Simulacion Terminada**")  
        pygame.quit()
#---------------------------------------------------------------------------------------------------------------------------------------------------

print("*Simulacion de Colisiones*\n")
Q = input("(R->Cambiar config) / (Enter->continuar): ")
if Q.upper() == "R":
    config_loop = True
    while config_loop:
        print("\n(1)Resolucion\n(2)FPS_lock\n(3)dt\n(4)Colores\n(5)Parametros de particulas ingresadas despues de partir\n(6)Numero de puntos de prueba para el campo vectorial\n(7)Permitir Merge\n(8)Rebote con las paredes\n(9)Numero de puntos en las colas")
        Q = input("\nIngrese configuracion a cambiar, exit para salir: ")
        if Q == "":
            break
        if Q.upper() == "EXIT":
            break
        elif int(Q) == 1:
            print("->Resolucion Actual:",get_tuple("Data\config.txt",0))
            I = input("Cambiar? ")
            if I.upper() == "SI":
                X = input("->Ingrese resolucion de la forma (A,B): ")
                edit("Data\config.txt",0,X)
        elif int(Q) == 2:
            print("->FPS Actual:",get_tuple("Data\config.txt",1)[0])
            I = input("Cambiar? ")
            if I.upper() == "SI":
                X = input("->Ingrese FPS_lock: ")
                edit("Data\config.txt",1,X)
        elif int(Q) == 3:
            print("->dt Actual:",get_tuple("Data\config.txt",2)[0])
            I = input("Cambiar? ")
            if I.upper() == "SI":
                X = input("->Ingrese dt: ")
                edit("Data\config.txt",2,X)
        elif int(Q) == 4:
            print("\nColores(RGB):\n(1)Particula1:",get_tuple("Data\config.txt",3),"\n(2)Particula2:",get_tuple("Data\config.txt",4),"\n(3)Palabras:",get_tuple("Data\config.txt",5),"\n(4)Fondo:",get_tuple("Data\config.txt",6))
            I = input("\nNºColor a cambiar(Enter para pasar): ")
            if I == "":
                pass
            elif int(I) in range(1,5):
                col = input("->Ingrese color forma(R,G,B): ")
                edit("Data\config.txt",int(I)+2,col)
        elif int(Q) == 5:
            print("\nParametros:\n(1)Velocidad_max/Largo_caja:",get_tuple("Data\config.txt",7)[0],"\n(2)Velocidad_min/Largo_caja:",get_tuple("Data\config.txt",8)[0])
            print("(3)Radio_max/Largo_caja:",get_tuple("Data\config.txt",9)[0],"\n(4)Radio_min/Largo_caja:",get_tuple("Data\config.txt",10)[0],"\n(5)Densidad/Largo_caja:",get_tuple("Data\config.txt",11)[0])
            I = input("\nNºParametro a cambiar(Enter para pasar): ")
            if I == "":
                pass
            elif int(I) in range(1,6):
                col = input("->Ingrese Nuevo Parametro: ")
                edit("Data\config.txt",int(I)+6,col)
        elif int(Q) == 6:
            print("->n Actual:",get_tuple("Data\config.txt",12)[0])
            I = input("Cambiar? ")
            if I.upper() == "SI":
                X = input("->Ingrese n: ")
                edit("Data\config.txt",12,X)
        elif int(Q) == 7:
            print("->Merge:",get_bool("Data\config.txt",13))
            I = input("Cambiar? ")
            if I.upper() == "SI":
                X = input("->Ingrese 1 para True o 0 para False: ")
                edit("Data\config.txt",13,X)
        elif int(Q) == 8:
            print("->Bound:",get_bool("Data\config.txt",14))
            I = input("Cambiar? ")
            if I.upper() == "SI":
                X = input("->Ingrese 1 para True o 0 para False: ")
                edit("Data\config.txt",14,X)
        elif int(Q) == 9:
            print("->Puntos maximos:",get_tuple("Data\config.txt",15)[0])
            I = input("Cambiar? ")
            if I.upper() == "SI":
                X = input("->Ingrese nuevo valor: ")
                edit("Data\config.txt",15,X)
        else:
            pass
        
load_config()
fontl = min(Width,Height)//30
maxLen = 16
Largo_caja = min(Width,Height)//1.1
if (Width-Largo_caja)/2 < maxLen * fontl/2.5:
    fontl = int((2.5*(Width - Largo_caja))/(2*maxLen))
Kx = fontl/2.5
Ky = fontl/1.818
Ly = Ky * 1.6
Margen_x = (Width - Largo_caja)//2
Margen_y = (Height - Largo_caja)//2
pygame.init()
pygame.mixer.init()
        
pregunta = True
while pregunta:
    pregunta = False
    Q = input("\nQuieres ocupar los parametros default?(recomendado): ")
    if Q.upper() == "NO":
        try:
            L = float(input("\n->Ingrese el largo de el contenedor cuadrado: "))
            N = int(input("->Ingrese la cantidad de pelotas a generar: "))
            gy = float(input("->Ingrese la gravedad en el eje vertical: "))
            gx = float(input("->Ingrese la gravedad en el eje horizontal: "))
            G = float(input("->Ingrese Constante atraccion gravitatoria(0 si no hay): "))
            Vmax = float(input("->Ingrese la velocidad maxima permitida: "))
            Vmin = float(input("->Ingrese la velocidad minima permitida: "))
            fit = False
            while not fit:
                fit = True
                Rmax = float(input("->Ingrese el radio maximo permitido: "))
                if 4*Rmax >= L:
                    print("\nEso definitivamente no cabe en el contenedor de largo",L)
                    fit = False
                elif N*pi*Rmax**2 > 1.5*L**2:
                    print("\nPuede que se vea muy apretada la cosa")
                    Q = input("Continuar? ")
                    if Q.upper() == "NO":
                        fit = False
            Rmin = float(input("->Ingrese el radio minimo permitido: "))
            Densidad = float(input("->Ingrese la densidad de cada pelota: "))
            c = float(input("->Ingrese el coeficiente de restitucion : "))
            t = int(input("->Ingrese el tiempo que dura la simulacion(-1 si es infinito): "))
            V = (Vmax,Vmin)
            r = (Rmax,Rmin)
            g = [gx,gy]
        except:
            print("\nError")
            pregunta = True
    else:
        N = 6
        V = (50,30)
        r = (8,2)
        L = 500
        Densidad = 1
        c = 0.98
        t = -1
        g = [0,0]
        G = 15000
    if pregunta == False:    
        print("**------------------------------------**")
        print("Entonces tendriamos:\n")
        print("El largo como",L)
        print("\nEl numero de particulas como",N)
        print("\nLa constante gravitatoria como",G)
        print("\nLa velocidad como",V)
        print("\nEl radio como",r)
        print("\nLa densidad como",Densidad)
        print("\nEl coeficientes de restitucion como",c)
        print("\nEl tiempo de simulacion es",t)
        print("\ndt :",dt)
        Q = input("\nEstas bien con esta configuracion? ")
        if Q.upper() == "NO":
            pregunta = True
            print("\nOkay, te preguntaremos de nuevo")
            input("\n(Enter para continuar)")
        else:
            input("\n(Enter para empezar simulacion)")
            print("\n******************************\n")
            font = pygame.font.SysFont(None, fontl)
            pygame.display.set_caption("Colisiones")
            clock = pygame.time.Clock()
            pygame.mixer.music.load("Data\Troll.mp3") 
            display = pygame.display.set_mode((Width,Height))
            contenedor = Caja(L,g,G,[],merge,bound)
            contenedor.generar(N,V,r,Densidad,c)
            contenedor.sim_start(dt,t)
           
        
    

