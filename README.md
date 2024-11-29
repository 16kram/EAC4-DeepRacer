# EAC5 AWS-DeepRacer Reward Function

Este script define una función de recompensa personalizada para el entorno de simulación **AWS DeepRacer**. La función calcula una recompensa basada en varios factores como la velocidad del agente, la dirección del coche con respecto a la pista, y la proximidad a la línea central de la pista.

## Descripción

La función `reward_function` evalúa cómo el coche debe comportarse en función de los parámetros de entrada proporcionados. El objetivo es proporcionar una recompensa mayor cuando el coche se mantiene cerca del centro de la pista y viaja rápidamente en las rectas, penalizando cuando se desvía o va demasiado rápido en las curvas.

## Parámetros de Entrada

La función `reward_function` toma un diccionario de parámetros de entrada llamado `params`, que contiene la siguiente información sobre el estado del coche y la pista:

- **track_width**: El ancho total de la pista (en metros).
- **distance_from_center**: La distancia del coche desde el centro de la pista (en metros).
- **speed**: La velocidad del agente en metros por segundo (m/s).
- **waypoints**: Una lista de tuplas `(x, y)` representando los puntos de referencia (waypoints) a lo largo del centro de la pista.
- **closest_waypoints**: Un par de índices que corresponden a los dos waypoints más cercanos al coche.
- **heading**: El ángulo de orientación del coche en grados, donde 0 grados es hacia el norte.

## Lógica de la Función de Recompensa

1. **Cálculo de la dirección de la pista**: La dirección de la pista se determina utilizando los puntos de referencia cercanos al coche. Se calcula el ángulo de la línea central de la pista entre los dos waypoints más cercanos.

2. **Cálculo de la diferencia de dirección**: La diferencia entre la dirección de la pista y la dirección del coche se calcula y se normaliza para asegurarse de que esté entre 0 y 180 grados.

3. **Recompensa basada en la velocidad y la dirección**:
   - Si la diferencia de dirección entre la pista y el coche es pequeña (menos de 10 grados), se da una recompensa mayor si el coche va rápido.
   - Si la diferencia de dirección es mayor (hasta 30 grados), la recompensa se reduce.
   - Si la diferencia de dirección es grande, se da una recompensa menor para incentivar el comportamiento adecuado en las curvas.

4. **Recompensa por proximidad al centro**: Se calcula la proximidad del coche al centro de la pista y se ajusta la recompensa:
   - Si el coche está muy cerca del centro (menos de un 10% del ancho de la pista), se le da una recompensa máxima.
   - Si está a una distancia moderada, la recompensa es más baja.
   - Si el coche está lejos del centro o se ha desviado demasiado, la recompensa es mínima.

## Código

```python
import math

def reward_function(params):
    '''
    EAC5 AWS-DeepRacer
    '''
    
    # Leemos los parámetros de entrada
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']  # velocidad del agente en metros por segundo (m/s)
    waypoints = params['waypoints']  # lista de (x, y) como waypoints a lo largo del centro de la pista
    closest_waypoints = params['closest_waypoints']  # índices de los dos waypoints más cercanos
    heading = params['heading']  # orientación del agente en grados
    
    # Comenzamos con una pequeña recompensa
    reward = 1e-3

    # Determinar si el agente está en una recta o en una curva
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    
    # Calculamos la dirección de la línea central con respecto a los waypoints
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)
    
    # Calculamos la diferencia entre la dirección de la pista y la dirección del coche
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
        
    # Recompensa por velocidad en las rectas y penalización en las curvas
    if direction_diff < 10:
        reward += speed * 2
    elif direction_diff < 30:
        reward += speed * 1.5
    else:
        reward += speed * 0.5
    
    # Definimos marcadores a diferentes distancias de la línea central
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Recompensa más alta si el coche está cerca del centro de la pista
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # probablemente ha chocado o está muy fuera de la pista
        
    # Retorna un valor de recompensa como un número flotante
    return float(reward)
