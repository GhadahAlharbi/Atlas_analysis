import awkward as ak
import matplotlib.pyplot as plt
import numpy as np

from load_data import load_data

def plot_histogram(awkward_array, title, xlabel):
    """
    Plots a histogram of the given data array.

    Args:
        awkward_array (Awkward Array): Data to be plotted as a histogram.
        title (str): Title of the histogram.
        xlabel (str): Label for the x-axis.

    Description:
        This function takes an Awkward Array, converts it to a NumPy array for compatibility with Matplotlib,
        and plots a histogram. This is used to visualize the distribution of data points, such as lepton transverse momentum.
    """
    # Convert Awkward Array to NumPy array to utilize NumPy's histogramming capabilities
    numpy_array = ak.to_numpy(awkward_array)

    # Generate histogram data using NumPy
    counts, bins = np.histogram(numpy_array, bins=30)

    # Calculate the width of each bin for visual representation
    widths = bins[1:] - bins[:-1]
    bin_centers = bins[:-1] + widths / 2

    # Create a bar plot to represent the histogram
    plt.figure(figsize=(10, 6))
    plt.bar(bin_centers, counts, width=widths, edgecolor='black', align='center')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Counts')
    plt.grid(True)
    plt.show()  # Display the plot

def create_visualization(data):
    """
    Main function to process and visualize data.

    Args:
        data (dict): Dictionary containing data loaded from various sources.

    """
    # Check if required data is available and call the plotting function
    if 'Signal (m_H = 125 GeV)' in data and 'lep_pt' in data['Signal (m_H = 125 GeV)'].fields:
        plot_histogram(data['Signal (m_H = 125 GeV)']['lep_pt'], 'Lepton PT Distribution in Signal Events', 'Lepton PT [GeV]')
    else:
        print("Required data not available for plotting.")

if __name__ == "__main__":
    data = load_data()  
    if data:
        print("Data loaded successfully.")
        create_visualization(data)  # Execute the visualization function with the loaded data
    else:
        print("Failed to load data.")
