import numpy as np
import awkward as ak
from load_data import load_data

def calculate_invariant_mass(pt, eta, phi, E):
    """
    Calculates the invariant mass of an event based on the lepton's kinematic variables.
    
    Args:
        pt (Awkward Array)
        eta (Awkward Array)
        phi (Awkward Array)
        E (Awkward Array)
        
    Returns:
        Awkward Array: Invariant mass calculated for each event.
    """
    exp_eta = np.exp(ak.to_numpy(eta))
    cosh_eta = (exp_eta + 1/exp_eta) / 2
    sinh_eta = (exp_eta - 1/exp_eta) / 2

    cosh_eta = ak.from_numpy(cosh_eta)
    sinh_eta = ak.from_numpy(sinh_eta)

    mass_squared = E**2 - (pt**2 * (cosh_eta**2 - sinh_eta**2))

    mass = ak.from_numpy(np.sqrt(ak.to_numpy(mass_squared)))
    return mass

def apply_event_selection(data, mass_window=(80, 250)):
    """
    Filters events based on the calculated invariant mass and selects events within a specified mass window.
    
    Args:
        data (dict): Dictionary of datasets categorized by type (e.g., signal, background).
        mass_window (tuple): Tuple specifying the lower and upper bounds of the invariant mass window.
    
    Returns:
        dict: A dictionary containing processed data for each sample within the mass window.
    """
    selected_data = {}
    for sample, events in data.items():
        if events is None:
            continue
        
        m4l = calculate_invariant_mass(events['lep_pt'], events['lep_eta'], events['lep_phi'], events['lep_E'])

        # Ensure that the mask is applied correctly
        mask = (m4l > mass_window[0]) & (m4l < mass_window[1])
        mask = ak.fill_none(mask, False)  # Replace any None values with False to avoid errors

        selected_data[sample] = events[mask]
        print(f"{sample}: {len(selected_data[sample])} events selected after mass window.")
    return selected_data

if __name__ == "__main__":
    data = load_data()
    if data:
        print("Data loaded successfully.")
        processed_data = apply_event_selection(data)
        print(f"Processed data ready for further analysis.")
    else:
        print("Data loading failed.")