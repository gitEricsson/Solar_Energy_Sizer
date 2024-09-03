from math import pi, cos, sin, log
import matplotlib.pyplot as plt
import io
import urllib, base64


def calculate_optical_properties(
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
    passivation_params=None,
):
    wavelength = wavelength * 10**-9  # Convert nm to meters

    # Convert thickness to meters
    d_substrate = d_substrate * 10**-6
    d_fto = d_fto * 10**-6
    d_photoanode = d_photoanode * 10**-6
    d_dye = d_dye * 10**-6

    # Passivation Layer properties
    if passivation_params:
        n_passivation, k_passivation, d_passivation = passivation_params
        d_passivation = d_passivation * 10**-6
        delta_passivation = (2 * pi * n_passivation * d_passivation) / wavelength
        m_passivation = [
            [
                cos(delta_passivation),
                1j * sin(delta_passivation) / (n_passivation - 1j * k_passivation),
            ],
            [
                1j * (n_passivation - 1j * k_passivation) * sin(delta_passivation),
                cos(delta_passivation),
            ],
        ]
    else:
        m_passivation = [[1, 0], [0, 1]]  # Identity matrix for no passivation

    # Calculate phase shifts
    delta_substrate = (2 * pi * n_substrate * d_substrate) / wavelength
    delta_fto = (2 * pi * n_fto * d_fto) / wavelength
    delta_photoanode = (2 * pi * n_photoanode * d_photoanode) / wavelength
    delta_dye = (2 * pi * n_dye * d_dye) / wavelength

    # Calculate transfer matrices
    m_substrate = [
        [cos(delta_substrate), 1j * sin(delta_substrate) / n_substrate],
        [1j * n_substrate * sin(delta_substrate), cos(delta_substrate)],
    ]

    m_fto = [
        [cos(delta_fto), 1j * sin(delta_fto) / (n_fto - 1j * k_fto)],
        [1j * (n_fto - 1j * k_fto) * sin(delta_fto), cos(delta_fto)],
    ]

    m_photoanode = [
        [
            cos(delta_photoanode),
            1j * sin(delta_photoanode) / (n_photoanode - 1j * k_photoanode),
        ],
        [
            1j * (n_photoanode - 1j * k_photoanode) * sin(delta_photoanode),
            cos(delta_photoanode),
        ],
    ]

    m_dye = [
        [cos(delta_dye), 1j * sin(delta_dye) / (n_dye - 1j * k_dye)],
        [1j * (n_dye - 1j * k_dye) * sin(delta_dye), cos(delta_dye)],
    ]
    
    # Multiply matrices
    m_total = m_substrate  # Initialize with substrate matrix
    for matrix in [m_fto, m_photoanode, m_dye, m_passivation]:
        m_total = [
            [
                m_total[0][0] * matrix[0][0] + m_total[0][1] * matrix[1][0],
                m_total[0][0] * matrix[0][1] + m_total[0][1] * matrix[1][1],
            ],
            [
                m_total[1][0] * matrix[0][0] + m_total[1][1] * matrix[1][0],
                m_total[1][0] * matrix[0][1] + m_total[1][1] * matrix[1][1],
            ],
        ]
    
    r = abs((m_total[0][0] + m_total[0][1] - m_total[1][0] - m_total[1][1]) / (m_total[0][0] + m_total[0][1] + m_total[1][0] + m_total[1][1])) ** 2
    
    t = 4 * 1.7 / (abs(m_total[0][0] + m_total[0][1] + m_total[1][0] + m_total[1][1]) ** 2)
    
    a = 1 - r - t
        
    return (a, r, t)


def calculate_photovoltaic_properties(a, wavelength):
    # Constants for photovoltaic calculations
    h = 6.626e-34  # Planck's constant in J.s
    c = 3e8  # Speed of light in m/s
    q = 1.6e-19  # Elementary charge in C
    k_B = 1.38e-23  # Boltzmann's constant in J/K
    T = 300  # Temperature in K

    # Photon Energy at the given wavelength
    E_lambda = (h * c / wavelength)  # Energy of a photon at the given wavelength in Joules

    I_lambda = 1.2

    # Adjusting the Photon Flux Density for the provided wavelength
    Phi_lambda = I_lambda / E_lambda
    
    # Wavelength range (400 nm to 800 nm)
    lambda_1 = 400e-9  # 400 nm in meters
    lambda_2 = 800e-9  # 800 nm in meters

    # Short-Circuit Current Density (Jsc) Calculation
    Jsc = q * Phi_lambda * (lambda_2 - lambda_1)  # in A/m^2
    Jsc_mA_cm2 = Jsc * 1e3 * 1e-4  # Convert to mA/cm^2

    # Ensure Jsc_mA_cm2 is positive and greater than J0
    J0 = 1e-12  # Reverse saturation current density in mA/cm^2
    Voc = (k_B * T / q) * log((Jsc_mA_cm2 / J0) + 1)  # in Volts

    # Fill Factor (FF) Calculation
    FF = (Voc + 1) / (Voc - log(Voc + 0.72))

    # Power Conversion Efficiency (η) Calculation
    Pin = 100  # Incident solar power per unit area under AM1.5 in mW/cm^2

    Efficiency = (Jsc_mA_cm2 * Voc * FF) / Pin * 100  # in %

    return round(Efficiency, 2)


def calculate_energy_yield(solar_irradiance, efficiency, area_m2):
    # Calculate energy yield (Kwh)
    energy_yield = (
        solar_irradiance * (efficiency / 100) * area_m2
    )
    return round(energy_yield, 2)


def calculate_total_load(appliance_loads):
    total_load = sum(appliance_loads)
    return total_load


def calculate_number_of_solar_cells(total_load, energy_yield):
    if energy_yield == 0:
        number_of_cells = float("inf")  # Set to infinity or handle appropriately
    else:
        number_of_cells = total_load // energy_yield  # Ceiling division
        if number_of_cells < 1:
            return (int(1))
    return (
        int(number_of_cells) if number_of_cells != float("inf") else 0
    )  # Adjust based on your application logic

# Function to plot and save each graph
def plot_to_uri(x, y, xlabel, ylabel):
    plt.figure()
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(f'{ylabel} vs {xlabel}')
    plt.grid(True)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    # uri = string.decode('utf-8')
    return uri