# main.py
from load_data import load_data
from process_data import process_data
from calculate_metrics import apply_event_selection
from visualization_script import create_visualization

def main():
    data = load_data()
    processed_data = process_data(data)
    metrics = apply_event_selection(processed_data)
    create_visualization(metrics)

if __name__ == "__main__":
    main()
