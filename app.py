import numpy as np
from math import pi

from flask import Flask, render_template, request
from .calculations import (
    calculate_optical_properties,
    calculate_photovoltaic_properties,
    calculate_energy_yield,
    calculate_total_load,
    calculate_number_of_solar_cells, plot_to_uri
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    # Get form data
    wavelength = float(request.form["wavelength"])

    # SAM Passivation Layer Properties
    # sam_type = request.form["sam_type"]
    sam_ri = float(request.form["sam_ri"])
    sam_k = float(request.form["sam_k"])
    sam_thickness = float(request.form["sam_thickness"])

    passivation_params = (sam_ri, sam_k, sam_thickness)

    # Substrate Properties
    n_substrate = float(request.form["substrate_ri"])
    d_substrate = float(request.form["substrate_thickness"])

    # Transparent Electrode Properties
    n_fto = float(request.form["electrode_ri"])
    k_fto = float(request.form["electrode_k"])
    d_fto = float(request.form["electrode_thickness"])

    # Photoanode (TiO2) Properties
    n_photoanode = float(request.form["photoanode_ri"])
    k_photoanode = float(request.form["photoanode_k"])
    d_photoanode = float(request.form["photoanode_thickness"])

    # Mimosa pudica Dye Properties
    n_dye = float(request.form["dye_ri"])
    k_dye = float(request.form["dye_k"])
    d_dye = float(request.form["dye_thickness"])

    # Calculate optical properties
    a, r, t = calculate_optical_properties(
        wavelength,
        n_substrate,
        d_substrate,
        n_fto,
        k_fto,
        d_fto,
        n_photoanode,
        k_photoanode,
        d_photoanode,
        n_dye,
        k_dye,
        d_dye,
        passivation_params,
    )

    # Calculate photovoltaic properties
    Efficiency = calculate_photovoltaic_properties(a, wavelength)

    # Additional data (for solar irradiance and load)
    solar_irradiance = float(request.form["solar_irradiance"])
    area_m2 = float(
        request.form.get("area", 1.0)
    )  # Defaulting area to 1.0 if not provided
    hours_per_day = float(request.form["num_hours"])
    # days = int(request.form["num_days"])

    # Calculate energy yield
    energy_yield = calculate_energy_yield(
        solar_irradiance, Efficiency, area_m2
    )

    # Calculate total load
    appliance_loads = [
        float(request.form["refrigerator_load"]) * hours_per_day,
        float(request.form["freezer_load"]) * hours_per_day,
        float(request.form["fan_load"]) * hours_per_day,
        float(request.form["ac_load"]) * hours_per_day,
        float(request.form["other_load"]) * hours_per_day,
    ]
    total_load = calculate_total_load(appliance_loads)

    # Calculate number of solar cells
    number_of_cells = calculate_number_of_solar_cells(total_load, energy_yield)
    
    
    # Time values for plotting
    wavelength_values = np.linspace(1, wavelength, 100)
    t_values = np.linspace(0, t, 100)
    t_load = np.linspace(0, total_load, 100)
    yield_values = np.linspace(0, energy_yield, 100)
    
    delta_substrate_plot = plot_to_uri(wavelength_values, (2 * np.pi * n_substrate * d_substrate) / wavelength_values, 'Wavelength', 'Substrate phase shift')
    
    delta_fto_plot = plot_to_uri(wavelength_values, (2 * pi * n_fto * d_fto) / wavelength_values, 'Wavelength', 'FTO phase shift')
    
    delta_photoanode_plot = plot_to_uri(wavelength_values, (2 * pi * n_photoanode * d_photoanode) / wavelength_values, 'Wavelength', 'Photoanode phase shift')
    
    delta_dye_plot = plot_to_uri(wavelength_values, (2 * pi * n_dye * d_dye) / wavelength_values, 'Wavelength', 'Dye phase shift')
    
    reflectance_vs_transmittance_plot = plot_to_uri(t_values, (1 - t_values - a), 'Transmittance', 'Reflectance')
    
    absorbance_vs_transmittance_plot = plot_to_uri(t_values, (1 - t_values- r), 'Transmittance', 'Absorbance')
    
    number_of_cells_vs_total_load_plot = plot_to_uri(t_load, (t_load // energy_yield), 'Total Appliance Load', 'Number of Solar Cells')
    
    number_of_cells_vs_energy_yield_plot = plot_to_uri(yield_values, (total_load // yield_values), 'Energy Yield', 'Number of Solar Cells')


    return render_template(
        "result.html",
        energy_output=energy_yield,
        efficiency=Efficiency,
        num_cells=number_of_cells,
        delta_substrate_plot=delta_substrate_plot,
        delta_fto_plot=delta_fto_plot,
        delta_photoanode_plot=delta_photoanode_plot,
        delta_dye_plot=delta_dye_plot,
        reflectance_vs_transmittance_plot=reflectance_vs_transmittance_plot,
        absorbance_vs_transmittance_plot=absorbance_vs_transmittance_plot,
        number_of_cells_vs_total_load_plot=number_of_cells_vs_total_load_plot,
        number_of_cells_vs_energy_yield_plot=number_of_cells_vs_energy_yield_plot
    )


if __name__ == "__main__":
    app.run(debug=True)
