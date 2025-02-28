
import random  # Importamos random para generar números al azar
import simpy

def RAM(env, nombre):
    while True:
        # Generar duración de RAM 
        DuracionMemoriaRAM = random.randint(1, 10)
        print(f"{nombre} empieza a usar memoria en el tiempo {env.now}, tiempo de espera {DuracionMemoriaRAM}")
        yield env.timeout(DuracionMemoriaRAM)

        # Generar duración de quieto 
        DuracionQuieto = random.randint(1, 2)
        print(f"{nombre} se queda quieto en el tiempo {env.now}, tiempo de espera {DuracionQuieto}")
        yield env.timeout(DuracionQuieto)

        # Detener la simulación cuando llega a 25
        if env.now > 25:
            print("Se acabó el tiempo de simulación")
            break  # Sale del bucle while

# Simulación con SimPy
env = simpy.Environment()

env.process(RAM(env, "Memoria RAM"))
env.run(until=25)

