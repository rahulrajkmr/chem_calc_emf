"""
Galvanic cell calculator.

This file is beginner Python. It:
1) stores electrode data
2) finds anode / cathode from E° values
3) calculates E°cell
4) uses the Nernst equation for non-standard conditions
"""

import math
from pyscript import document


# R = gas constant (J / mol·K), F = Faraday constant (C / mol)
R = 8.314
F = 96485

# Each electrode is a dictionary: name, metal symbol, ion, electrons, E°.
ELECTRODES = [
    {"id": "li", "name": "Lithium", "metal": "Li", "ion": "Li+", "electrons": 1, "E0": -3.04},
    {"id": "k", "name": "Potassium", "metal": "K", "ion": "K+", "electrons": 1, "E0": -2.92},
    {"id": "ba", "name": "Barium", "metal": "Ba", "ion": "Ba2+", "electrons": 2, "E0": -2.90},
    {"id": "ca", "name": "Calcium", "metal": "Ca", "ion": "Ca2+", "electrons": 2, "E0": -2.87},
    {"id": "na", "name": "Sodium", "metal": "Na", "ion": "Na+", "electrons": 1, "E0": -2.71},
    {"id": "mg", "name": "Magnesium", "metal": "Mg", "ion": "Mg2+", "electrons": 2, "E0": -2.37},
    {"id": "al", "name": "Aluminum", "metal": "Al", "ion": "Al3+", "electrons": 3, "E0": -1.66},
    {"id": "mn", "name": "Manganese", "metal": "Mn", "ion": "Mn2+", "electrons": 2, "E0": -1.18},
    {"id": "zn", "name": "Zinc", "metal": "Zn", "ion": "Zn2+", "electrons": 2, "E0": -0.76},
    {"id": "cr", "name": "Chromium", "metal": "Cr", "ion": "Cr3+", "electrons": 3, "E0": -0.74},
    {"id": "fe", "name": "Iron", "metal": "Fe", "ion": "Fe2+", "electrons": 2, "E0": -0.44},
    {"id": "cd", "name": "Cadmium", "metal": "Cd", "ion": "Cd2+", "electrons": 2, "E0": -0.40},
    {"id": "co", "name": "Cobalt", "metal": "Co", "ion": "Co2+", "electrons": 2, "E0": -0.28},
    {"id": "ni", "name": "Nickel", "metal": "Ni", "ion": "Ni2+", "electrons": 2, "E0": -0.25},
    {"id": "sn", "name": "Tin", "metal": "Sn", "ion": "Sn2+", "electrons": 2, "E0": -0.14},
    {"id": "pb", "name": "Lead", "metal": "Pb", "ion": "Pb2+", "electrons": 2, "E0": -0.13},
    {"id": "h", "name": "Hydrogen", "metal": "H2", "ion": "H+", "electrons": 2, "E0": 0.00},
    {"id": "cu", "name": "Copper", "metal": "Cu", "ion": "Cu2+", "electrons": 2, "E0": 0.34},
    {"id": "ag", "name": "Silver", "metal": "Ag", "ion": "Ag+", "electrons": 1, "E0": 0.80},
    {"id": "hg", "name": "Mercury", "metal": "Hg", "ion": "Hg2+", "electrons": 2, "E0": 0.85},
    {"id": "pt", "name": "Platinum", "metal": "Pt", "ion": "Pt2+", "electrons": 2, "E0": 1.20},
    {"id": "au", "name": "Gold", "metal": "Au", "ion": "Au3+", "electrons": 3, "E0": 1.50},
]


def find_electrode(electrode_id):
    for item in ELECTRODES:
        if item["id"] == electrode_id:
            return item
    return ELECTRODES[0]


def format_voltage(value):
    return f"{value:+.3f} V"


def gcd(a, b):
    a = abs(a)
    b = abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


def reaction_text(electrode, count, as_ion):
    number = "" if count == 1 else str(count)
    if as_ion:
        return number + electrode["ion"]
    return number + electrode["metal"]


def calculate_cell(electrode_a, electrode_b, conc_a, conc_b, temp_c):
    # The electrode with the more negative E° is the anode (oxidation).
    if electrode_a["E0"] <= electrode_b["E0"]:
        anode = electrode_a
        cathode = electrode_b
        anode_conc = conc_a
        cathode_conc = conc_b
    else:
        anode = electrode_b
        cathode = electrode_a
        anode_conc = conc_b
        cathode_conc = conc_a

    e_standard = cathode["E0"] - anode["E0"]

    # n is the number of electrons transferred in the balanced cell reaction.
    n = lcm(anode["electrons"], cathode["electrons"])
    anode_count = n // anode["electrons"]
    cathode_count = n // cathode["electrons"]

    oxidation = (
        reaction_text(anode, anode_count, False)
        + " → "
        + reaction_text(anode, anode_count, True)
        + f" + {n}e-"
    )
    reduction = (
        reaction_text(cathode, cathode_count, True)
        + f" + {n}e- → "
        + reaction_text(cathode, cathode_count, False)
    )
    overall = (
        reaction_text(anode, anode_count, False)
        + " + "
        + reaction_text(cathode, cathode_count, True)
        + " → "
        + reaction_text(anode, anode_count, True)
        + " + "
        + reaction_text(cathode, cathode_count, False)
    )

    # Q = [anode ion]^a / [cathode ion]^c   (metals/solids = 1)
    Q = (anode_conc ** anode_count) / (cathode_conc ** cathode_count)

    temp_k = temp_c + 273.15
    # Nernst equation: E = E° - (RT / nF) ln Q
    e_nernst = e_standard - (R * temp_k / (n * F)) * math.log(Q)
    log_term = (2.303 * R * temp_k) / (n * F)

    return {
        "anode": anode,
        "cathode": cathode,
        "e_standard": e_standard,
        "e_nernst": e_nernst,
        "n": n,
        "Q": Q,
        "log_term": log_term,
        "oxidation": oxidation,
        "reduction": reduction,
        "overall": overall,
        "anode_conc": anode_conc,
        "cathode_conc": cathode_conc,
        "temp_c": temp_c,
        "temp_k": temp_k,
        "same": electrode_a["id"] == electrode_b["id"],
    }


def fill_dropdown(select_id, selected_id):
    select = document.querySelector("#" + select_id)
    html = ""
    for item in ELECTRODES:
        chosen = " selected" if item["id"] == selected_id else ""
        label = f'{item["name"]} ({item["ion"]})  {item["E0"]:+.2f} V'
        html += f'<option value="{item["id"]}"{chosen}>{label}</option>'
    select.innerHTML = html


def update_series_table(anode_id, cathode_id):
    rows = ""
    for item in ELECTRODES:
        css = ""
        tag = ""
        if item["id"] == anode_id and item["id"] == cathode_id:
            css = "highlight-anode"
            tag = " same electrode"
        elif item["id"] == anode_id:
            css = "highlight-anode"
            tag = " anode"
        elif item["id"] == cathode_id:
            css = "highlight-cathode"
            tag = " cathode"

        if item["electrons"] == 1:
            half = f'{item["ion"]} + e- → {item["metal"]}'
        else:
            half = f'{item["ion"]} + {item["electrons"]}e- → {item["metal"]}'

        rows += (
            f'<tr class="{css}">'
            f'<td>{item["name"]}{tag}</td>'
            f"<td>{half}</td>"
            f'<td>{item["E0"]:+.2f}</td>'
            "</tr>"
        )
    document.querySelector("#series_table").innerHTML = rows


def read_number(element_id):
    text = document.querySelector("#" + element_id).value
    return float(text)


def update_results(event=None):
    electrode_a = find_electrode(document.querySelector("#electrode_a").value)
    electrode_b = find_electrode(document.querySelector("#electrode_b").value)

    try:
        temp_c = read_number("temp_c")
        conc_a = read_number("conc_a")
        conc_b = read_number("conc_b")
    except Exception:
        document.querySelector("#results").innerHTML = (
            "<h2>Results</h2><p class='warn'>Please enter numbers for temperature and concentrations.</p>"
        )
        return

    if conc_a <= 0 or conc_b <= 0:
        document.querySelector("#results").innerHTML = (
            "<h2>Results</h2><p class='warn'>Concentrations must be greater than 0.</p>"
        )
        return

    result = calculate_cell(electrode_a, electrode_b, conc_a, conc_b, temp_c)
    anode = result["anode"]
    cathode = result["cathode"]

    if result["e_nernst"] > 0:
        status = "<p class='ok'>The cell is spontaneous as written (E &gt; 0).</p>"
    elif result["e_nernst"] < 0:
        status = "<p class='warn'>The cell is not spontaneous as written (E &lt; 0).</p>"
    else:
        status = "<p>E = 0, so there is no driving force.</p>"

    if result["same"]:
        status = "<p>Same electrodes make a concentration cell. E° = 0, but E can still be non-zero if the concentrations differ.</p>"

    html = f"""
        <h2>Results</h2>
        <div class="roles">
            <div class="role anode">
                <strong>Anode (oxidation)</strong>
                <p>{anode["name"]}</p>
                <p>E° = {format_voltage(anode["E0"])}</p>
            </div>
            <div class="role cathode">
                <strong>Cathode (reduction)</strong>
                <p>{cathode["name"]}</p>
                <p>E° = {format_voltage(cathode["E0"])}</p>
            </div>
        </div>
        <p>Standard EMF</p>
        <p class="emf">{format_voltage(result["e_standard"])}</p>
        <p>E°cell = E°cathode − E°anode = {cathode["E0"]:+.3f} − ({anode["E0"]:+.3f})</p>
        {status}
        <div class="block">
            <p>Oxidation</p>
            <code>{result["oxidation"]}</code>
        </div>
        <div class="block">
            <p>Reduction</p>
            <code>{result["reduction"]}</code>
        </div>
        <div class="block">
            <p>Overall reaction</p>
            <code>{result["overall"]}</code>
        </div>
        <div class="block">
            <p>Nernst equation</p>
            <code>n = {result["n"]} electrons
Q = [{anode["ion"]}]^{result["n"] // anode["electrons"]} / [{cathode["ion"]}]^{result["n"] // cathode["electrons"]}
Q = ({result["anode_conc"]})^{result["n"] // anode["electrons"]} / ({result["cathode_conc"]})^{result["n"] // cathode["electrons"]} = {result["Q"]:.4g}
T = {result["temp_c"]:.2f} °C = {result["temp_k"]:.2f} K
E = E° − (2.303 RT / nF) log10 Q
E = {result["e_standard"]:+.3f} − ({result["log_term"]:.5f}) log10({result["Q"]:.4g})
E = {format_voltage(result["e_nernst"])}</code>
        </div>
        <p class="emf">{format_voltage(result["e_nernst"])}</p>
        <p>Cell voltage from the Nernst equation</p>
    """
    document.querySelector("#results").innerHTML = html
    update_series_table(anode["id"], cathode["id"])

    # Update voltmeter display
    voltmeter_display = document.querySelector("#voltmeter-display")
    if voltmeter_display:
        voltmeter_display.innerText = f"{abs(result['e_nernst']):.2f} V"


fill_dropdown("electrode_a", "zn")
fill_dropdown("electrode_b", "cu")
update_results()
