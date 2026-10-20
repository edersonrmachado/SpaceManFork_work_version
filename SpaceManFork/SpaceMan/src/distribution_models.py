import numpy as np

def calculate_num_eds(density, radius):
    """Calculates number of EDs in for in a given area in accordance with density"""
    
    radius_m=radius*1000
    area=np.pi*(radius_m**2)
    lambda_area=density*area
    
    rng = np.random.default_rng()
    num_of_eds = rng.poisson(lambda_area)
    
    return num_of_eds

def calculate_num_tx_per_ed(ed_tx_density_per_sec,period_s):
    """ Calculatees the number of tx per ed in order to have the average tx delivery rate"""
    
    mean_tx_ed = ed_tx_density_per_sec*period_s
    
    rng = np.random.default_rng()
    tx_per_ed = rng.poisson(mean_tx_ed)
    
    return tx_per_ed