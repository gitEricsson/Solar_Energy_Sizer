# Solar Energy Sizer

The Solar Energy Sizer is a comprehensive tool for estimating the energy yield, efficiency, and number of solar cells required for a solar energy system. This Python-based(Flask) application is particularly useful for individuals and professionals planning or optimizing solar energy installations.

## Features

- **Optical Properties Calculation**: Calculates reflectance, transmittance, and absorbance of a solar module.
- **Photovoltaic Properties Calculation**: Computes short-circuit current density (Jsc), open-circuit voltage (Voc), fill factor (FF), and power conversion efficiency (η).
- **Energy Yield Calculation**: Determines the energy yield based on solar irradiance, efficiency, area, and time parameters.
- **Load Calculation**: Calculates the total load from various appliances and determines the number of solar cells required to meet the energy demand.
- **User-Friendly Interface**: Provides an intuitive UI for entering inputs and displaying the calculated results.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.9
- Flask 3.0.3

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/solar-energy-calculator.git
   cd solar-energy-calculator
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Set the Flask environment**:

   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```

   On Windows, use:

   ```bash
   set FLASK_APP=app.py
   set FLASK_ENV=development
   ```

2. **Run the Flask application**:

   ```bash
   flask run

   # For hot reloading
   flask --debug run
   ```

3. **Access the application**:

   Open your browser and go to `http://127.0.0.1:5000/`.

## Project Structure

```plaintext
solar-energy-calculator/
│
├── app.py               # Main application file containing Flask routes
├── calculations.py      # Contains all the calculation functions
├── templates/           # HTML templates
│   ├── index.html       # Main form for user input
│   └── result.html      # Display calculation results
├── static/
│   ├── style.css        # Stylesheet for the application
│   └── script.js        # JavaScript for the application (if needed)
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```
