
import random #importamos random para generar numeros al azar
import simpy

bandera = True
def RAM (env, RAM):
    while bandera == True:
        DuracionMemoriaRAM = random.randint(1,10)
        print(RAM, 'Empieza a usar memoria %d' % env.now,' tiempo de espera ',DuracionMemoriaRAM)
        yield env.timeout(DuracionMemoriaRAM)



#Simulacion Simpy
env = simpy.Environment() 

env.process(RAM('Memoria RAM',env))
env.run(until=25)  #correr la simulacin hasta el tiempo = 15
