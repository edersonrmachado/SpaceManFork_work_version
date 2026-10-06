## SIMULATION

{
    "print_simulation_debug": false,
    "print_link_margin_debug": false,
    "print_doppler_debug": false,
    "simulation_start": {
        "year": 2026,
        "day": 8,
        "month": 10,
        "hour": 0,
        "minute": 0,
        "second": 0
    },
    "simulation_end": {
        "year": 2026,
        "day": 10,
        "month": 10,
        "hour": 0,
        "minute": 0,
        "second": 0
    }
}

## RESULTS
{
    "results_file": "../data/eirpEU433_12_30_gt0_t.csv"
}

## SATELLITE

{
    "num_sats": 100,
    "min_elevation_angle":5
}

## ENDPOINT

{
    "ed_geometry": {
        "central_point": {
            "lat": -3.5158,
            "lon": 23.5801
        },
        "circle_radius_km": 100,
        "distribution_seed": null
    },
    "number_of_eds": 20,
    "pkt_per_endpoint": 100,
    "policy_tx": "random_secure"
}

### LORA
[
    {
        "sf": 7,
        "bw": 125,
        "ldro": 0,
        "frequency": 433.375,
        "pkt_len": 245
    }
]
### LINK MARGIN
{
    "iot_node": {
        "pt_dbm": 21,
        "lftx": 1,
        "gt": 0
    },
    "propagation_losses": {
        "la": -0.11,
        "li": -0.16,
        "ld": -3.0,
        "lp": -3.0
    },
    "satellite_receiver": {
        "gr": 0,
        "lfrx": 1,
        "nf": 6.5,
        "temp_0": 290,
        "gf": -1.0,
        "ta": 290
    }
}


### DOPPLER
{   
     "derivative_num_of_points":3,
     "derivative_step_sec":10e-6   
    
}