import math

def reward_function(params):
    '''
    EAC5 AWS-DeepRacer
    '''
    
    # Leemos los parámetros de entrada
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']# velocitat de l'agent en metres per segon (m/s)
    waypoints = params['waypoints']# llista de (x,y) com a fites al llarg del centre de la pista
    closest_waypoints = params['closest_waypoints']# índexs de les dues fites (waypoints) més pròxims
    heading = params['heading']# viratge de l'agent en graus
    
    # Començar amb una petita recompensa
    reward = 1e-3

    # Determinar si l'agent es troba en un camí recte o en una cantonada
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    
    # Calcular la direcció de la línia central basant-se en les següents fites
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)
    
    # Calcular la diferència entre la direcció de la pista i la direcció del cotxe
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
        
    # Recompensa per anar més de pressa en les rectes i penalitza per anar ràpid en les corbes
    if direction_diff < 10:
        reward += speed * 2
    elif direction_diff < 30:
        reward += speed * 1.5
    else:
        reward += speed * 0.5
    
    # Calcula 3 marcadors que es troben a diferents distàncies de la línia central
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Doneu una recompensa més alta si el cotxe està més a prop de la línia central i viceversa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # probablement s'ha estavellat/a prop del camí
        
    # Retorna sempre un valor de punt flotant (float)
    return float(reward)