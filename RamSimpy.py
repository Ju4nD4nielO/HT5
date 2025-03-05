import random  # Importamos random para generar números al azar
import simpy

RANDOM_SEED = 42 
INTERVALO = 10  # Genera nuevos procesos cada x tiempo
INST_CPU = 3  # Numero de instrucciones que ejecuta el CPU por cada ciclo de reloj

random.seed(RANDOM_SEED)

def procesos(env, numero, ram, cpu): #simula la vida de cada proceso
    
    print(str(env.now) + ": " + numero + " llega al sistema (Nuevo)") # Llegada de nuevo proceso
    
    # Proceso solicita memoria RAM y espera hasta que haya dispomnible
    RAM_necesaria = random.randint(1, 10)
    print("Proceso: " + str(numero) + " solicita " + str(RAM_necesaria) + " de RAM")
    yield ram.get(RAM_necesaria)
    print("Proceso: " + str(numero) + " obtiene " + str(RAM_necesaria) + " unidades de RAM (Listo)")

    # Se asigna numero de instrucciones al proceso y se pone ready
    instrucciones_totales = random.randint(1, 10)
    print("Proceso: " + str(numero) + " tiene " + str(instrucciones_totales) + " instrucciones por ejecutar")


    while instrucciones_totales > 0: # Ciclo de ejecución de procesos
        with cpu.request() as req:
            yield req  # Solicita acceso al CPU
            # Reduce las instrucciones pendientes según INST_CPU
            instrucciones_ejecutadas = min(INST_CPU, instrucciones_totales)
            instrucciones_totales -= instrucciones_ejecutadas
            print(f"Proceso: {numero} ejecuta {instrucciones_ejecutadas} instrucciones. Restantes: {instrucciones_totales}")

            # verifica si se termino de ejecutar todas las instrucciones
            if instrucciones_totales == 0:
                # Estado: Terminated
                print(f"{env.now}: {numero} termina su ejecución (Terminated)")
                break
            else:
                # Decide aleatoriamente si pasa a ready o waiting
                numero_aleatorio = random.randint(1, 2)
                if numero_aleatorio == 1: # Pasa a Waiting I/O
                    print(f"{env.now}: {numero} entra en estado Waiting ")
                    yield env.timeout(random.randint(1, 5))  # simula tiempo que pasa en waiting
                    print(f"{env.now}: {numero} sale de Waiting y vuelve a Ready")
                else:
                    # Pasa a ready
                    print(f"{env.now}: {numero} vuelve a la cola Ready")

            

    # Devuelve la RAM asignada cuando el proceso termina
    ram.put(RAM_necesaria)
    print(str(env.now) + f" {numero} libera {RAM_necesaria} de RAM y termina (Terminado)")
    
# (corredores)
def generador(env, ram, cpu, num_procesos = 25): #Generador de procesos, el num_procesos define 
                                               #el numero de procesos que generara antes de parar 
    for id in range(1, num_procesos + 1):
        env.process(procesos(env, f"Proceso {id}", ram, cpu))
        
        # Tiempo de espera exponencial antes de creacion de nuevo proceso
        yield env.timeout(random.expovariate(1.0 / INTERVALO))

# Simulación con SimPy
env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100) # La memoria solo llega hasta el numero x 
cpu = simpy.Resource(env, capacity=2) # Solo se puede ejecutar un proceso a la vez

# Inicia la generacion de los procesos
env.process(generador(env, ram, cpu))

env.run()

#Calcula y muestra el tiempo
print(f"Tiempo total de simulación: " + str((env.now)))
