
import random  # Importamos random para generar números al azar
import simpy

RANDOM_SEED = 42 
INTERVALO = 10  # Genera nuevos procesos cada x tiempo
INST_CPU = 3  # Numero de instrucciones que ejecuta el CPU por cada ciclo de reloj

random.seed(RANDOM_SEED)

def procesos(env, numero, ram, cpu): #simula la vida de cada proceso
    
    print(str(env.now) + ": " + numero + " llega al sistema (New)") # Llegada de nuevo proceso
    
    # Proceso solicita memoria RAM y espera hasta que haya dispomnible
    RAM_necesaria = random.randint(1, 10)
    print("Proceso: " + str(numero) + " solicita " + str(RAM_necesaria) + " de RAM")
    yield ram.get(RAM_necesaria)
    print("Proceso: " + str(numero) + " obtiene " + str(RAM_necesaria) + " unidades de RAM (Ready)")

    # Se asigna numero de instrucciones al proceso y se pone ready
    instrucciones_tot = random.randint(1, 10)
    print("Proceso: " + str(numero) + " tiene " + str(instrucciones_tot) + " instrucciones por ejecutar")

    while instrucciones_tot > 0: #Ciclo de ejecucion de procesos
        with cpu.request() as req:
            yield req
            print(str(env.now) + ": " + str(numero) + " es atendido por el CPU (Running)")

            instrucciones_ejecutadas = min(INST_CPU, instrucciones_tot)
            yield env.timeout(1)  # Simular el tiempo de ejecución
            instrucciones_tot -= instrucciones_ejecutadas
            print(f"{env.now}: {numero} ejecuta {instrucciones_ejecutadas} instrucciones. Le quedan {instrucciones_tot}")

            if instrucciones_tot == 0:
                print(str(env.now) + ": Proceso : " + str(numero) + " ha terminado de ejecutar instrucciones (Terminated)")
                break

            else:
                aleatorio = random.randint(1,2)

                if aleatorio == 1: # El proceso pasa a waiting I/O
                    print(str(env.now) + ": " + str(numero) + " se va a I/O (Waiting)")
                    yield env.timeout(1) # Tiempo de espera
                    print(str(env.now) + ": " + str(numero) + " regresa a estado (Ready)")

                else: # El proceso regresa a ready para ser atendido por el CPU
                    print(str(env.now) + ": " + str(numero) + " Regresa a estado (Ready)")


def generador(env, ram, cpu, num_procesos=25): #Generador de procesos, el num_procesos define 
                                               #el numero de procesos que generara antes de parar
    for id in range(1, num_procesos + 1):
        env.process(procesos(env, f"Proceso {id}", ram, cpu))
        
        # Tiempo de espera exponencial antes de creacion de nuevo proceso
        yield env.timeout(random.expovariate(1.0 / INTERVALO))


# Simulación con SimPy
env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)
cpu = simpy.Resource(env, capacity=1) # Capacity es: CPU con x numero de nucleos

# Inicia la generacion de los procesos
env.process(generador(env, ram, cpu))

env.run()
