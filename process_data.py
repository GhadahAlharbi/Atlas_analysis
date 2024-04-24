import numpy as np

def process_data(data):
    """
    Processes particle physics data by applying several filters and calculates the invariant mass for selected events.
    
    Args:
        data (dict): A dictionary containing datasets categorized by sample type.
    
    Returns:
        dict: A dictionary containing processed data for each sample.
    """
    filtered_data = {}
    for sample, events in data.items():
        print(f"Initial count in {sample}: {len(events)}")

        # Filter events to include only those with exactly four leptons
        mask = events['lep_n'] == 4
        events = events[mask]
        print(f"Count after lepton filter in {sample}: {len(events)}")

        # Further filter events where the sum of lepton charges is zero and
        # either all four leptons are electrons (lep_type == 11) or muons (lep_type == 13)
        mask = (np.sum(events['lep_charge'], axis=1) == 0) & \
               ((np.sum(events['lep_type'] == 11, axis=1) == 4) |  # Four electrons
                (np.sum(events['lep_type'] == 13, axis=1) == 4))   # Four muons
        events = events[mask]
        print(f"Count after charge and type filter in {sample}: {len(events)}")

        # Calculate the invariant mass for the filtered events if any events remain after filtering
        if len(events) > 0:
            events['m4l'] = calculate_invariant_mass(events['lep_pt'], 
                                                     events['lep_eta'], 
                                                     events['lep_phi'], 
                                                     events['lep_E'])
        filtered_data[sample] = events
    
    return filtered_data

def calculate_invariant_mass(pt, eta, phi, E):
    """
    Calculates the invariant mass for events based on the lepton's transverse momentum, pseudorapidity, azimuthal angle, and energy.
    
    Args:
        pt (array)
        eta (array)
        phi (array)
        E (array)
        
    Returns:
        array: Calculated invariant mass of the events.
    """
    # Simplified version of mass calculation using numpy's cosh function for hyperbolic cosine
    return pt * np.cosh(eta)  

if __name__ == "__main__":
    from load_data import load_data  
    data = load_data()
    processed_data = process_data(data)
    print("Data processing complete.")