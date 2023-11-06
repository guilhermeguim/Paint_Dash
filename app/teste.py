import random
from datetime import datetime, timedelta
from manager import db_manager
from get_functions import get_path,get_curr_path

def generate_random_date():
    start_date = datetime(2023, 9, 17)
    end_date = datetime(2023, 9, 28)
    time_difference = (end_date - start_date).total_seconds()
    random_seconds = random.randint(0, int(time_difference))
    random_date = start_date + timedelta(seconds=random_seconds)
    return random_date.strftime("%Y-%m-%d %H:%M:%S")

def choose_random_variable(local_type_options, side_options, location_options, region_options):
    local_type = random.choice(local_type_options)
    side = random.choice(side_options)
    
    if local_type == 'exterior':
        location = random.choice(['side', 'fender', 'front door', 'rear door', 'hood', 'roof', 'tail gate', 'trunk lid'])
    else:
        location = random.choice(['side', 'front door', 'rear door', 'hood', 'back pnl', 'tail gate', 'trunk lid'])
    
    if location == 'side':
        region = random.choice(['1,1', '1,2', '1,3', '1,4', '1,5', '2,1', '2,2', '2,3', '2,4', '2,5'])
    elif location == 'fender':
        region = random.choice(['1,1', '1,2', '2,1', '2,2'])
    elif location in ['rear door', 'front door']:
        region = random.choice(['1,1', '1,2', '1,3', '2,1', '2,2', '2,3', '3,1', '3,2', '3,3'])
    elif location == 'hood':
        if side == 'rh':
            region = random.choice(['1,1', '1,2', '2,1', '2,2'])
        else:
            region = random.choice(['3,1', '3,2', '4,1', '4,2'])
    elif location == 'roof':
        if side == 'rh':
            region = random.choice(['1,1', '1,2', '1,3', '2,1', '2,2', '2.3'])
        else:
            region = random.choice(['3,1', '3,2', '3,3', '4,1', '4,2', '4.3'])
    elif location == 'tail gate':
        if side == 'lh':
            if local_type == 'exterior':
                region = random.choice(['1,1', '1,2', '2,1', '2,2'])
            else:
                region = random.choice(['1,1', '1,2', '2,1', '2,2', '3,1', '3,2'])
        else:
            if local_type == 'exterior':
                region = random.choice(['1,3', '1,4', '2,3', '2,4'])
            else:
                region = random.choice(['1,3', '1,4', '2,3', '2,4', '3,3', '3,4'])
    elif location == 'trunk lid':
        if side == 'lh':
            region = random.choice(['1,1', '1,2', '2,1', '2,2'])
        else:
            region = random.choice(['1,3', '1,4', '2,3', '2,4'])
    else:  # location == 'back pnl'
        if side == 'lh':
            region = random.choice(['1,1', '1,2', '2,1', '2,2', '3,1', '3,2', '4,1', '4,2'])
        else:
            region = random.choice(['1,3', '1,4', '2,3', '2,4', '3,3', '3,4', '4,3', '4,4'])

    date_time = generate_random_date()

    return [local_type, side, location, region,'', date_time,'37107014',1]

# Opções para as variáveis
local_type_options = ['exterior', 'interior']
side_options = ['rh', 'lh']
location_options = ['side', 'fender', 'front door', 'rear door', 'hood', 'roof', 'tail gate', 'trunk lid', 'back pnl']
region_options = ['1,1', '1,2', '1,3', '1,4', '1,5', '2,1', '2,2', '2,3', '2,4', '2,5',
                  '3,1', '3,2', '3,3', '4,1', '4,2', '4,3', '3,4', '4,4']

# Gerar 500 listas de variáveis aleatórias
result_list = [choose_random_variable(local_type_options, side_options, location_options, region_options) for _ in range(1500)]

db_path = get_path()
db_manager = db_manager(db_path)
# Exibir os resultados
for item in result_list:
    db_manager.input_data(item)
    print(item)