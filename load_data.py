import uproot
import awkward as ak
from infofile import infos 

def load_data():
    """
    Loads data from the ATLAS Open Data portal for various physics samples.
    Processes both actual collision data and simulated samples.
    
    Returns:
        A dictionary of datasets categorized by sample type (Data, Background, Signal).
    """
    data = {}
    tuple_path = "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/"
    samples = {
        'data': {'list': ['data_A', 'data_B', 'data_C', 'data_D']},
        'Background Z, t-bar': {'list': ['Zee', 'Zmumu', 'ttbar_lep'], 'color': "#6b59d3"},
        'Background ZZ*': {'list': ['llll'], 'color': "#ff0000"},
        'Signal (m_H = 125 GeV)': {'list': ['ggH125_ZZ4lep', 'VBFH125_ZZ4lep', 'WH125_ZZ4lep', 'ZH125_ZZ4lep'], 'color': "#00cdff"},
    }

    # Iterates over each sample type and loads data from ROOT files using the uproot library
    for s in samples:
        print(f'Processing {s} samples')
        frames = []
        for val in samples[s]['list']:
            # Constructs the file path based on whether the data is real or simulated
            prefix = "Data/" if s == 'data' else f"MC/mc_{infos[val]['DSID']}."
            file_path = f"{tuple_path}{prefix}{val}.4lep.root"
            try:
                # Open the ROOT file and load data into Awkward Arrays
                with uproot.open(file_path + ":mini") as tree:
                    frames.append(tree.arrays(library="ak"))
            except Exception as e:
                print(f"Failed to load data from {file_path}: {str(e)}")
                continue
        # Concatenate all frames for the sample into a single dataset
        data[s] = ak.concatenate(frames) if frames else None
    return data

if __name__ == "__main__":
    data = load_data()
    if data:
        print("Data loaded successfully.")
    else:
        print("Data loading failed.")