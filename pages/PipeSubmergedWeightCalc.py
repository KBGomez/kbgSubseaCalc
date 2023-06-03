# Pipe Submerged Weight Calc
# Kenneth Brian Gomez
# Saturday, June 3, 2023
#
import streamlit as st
import math

# Webpage title
st.title("Pipe Submerged Weight Calc")
st.write("#### This page calculates a pipelines dry and submerged weight")

st.write("""***""")
st.write(
    """ This page calculates the dry and submmerged weight of a pipeline.  
    Current limits takes into account only the wall thickness.  
    Pipeline coatings will be added later.  
Send me an email if you find any errors. 
 """
)
st.write("""***""")


# function to calculate submerged weight
def calculate_pipe_weight(
    outer_diameter_mm,
    wall_thickness_mm,
    material_density=7850,
    water_density=1000,
    content_density=0,
):
    # Convert mm to m for calculation
    outer_diameter = outer_diameter_mm / 1000
    wall_thickness = wall_thickness_mm / 1000

    # Calculate the inner diameter
    inner_diameter = outer_diameter - 2 * wall_thickness

    # Calculate the volume of the pipeline
    pipeline_volume = math.pi * ((outer_diameter / 2) ** 2 - (inner_diameter / 2) ** 2)

    # Calculate the pipeline weight
    pipeline_weight = pipeline_volume * material_density

    # Calculate the volume of the water displaced by the pipeline
    displaced_water_volume = math.pi * (outer_diameter / 2) ** 2

    # Calculate the weight of the displaced water
    displaced_water_weight = displaced_water_volume * water_density

    # Calculate the submerged weight of the pipeline
    submerged_weight = pipeline_weight - displaced_water_weight

    # Convert the  weight from kg/m to kN/m
    submerged_weight_kN_m = submerged_weight * 9.81 / 1000
    pipeline_weight_kN_m = pipeline_weight * 9.81 / 1000

    return pipeline_weight_kN_m, submerged_weight_kN_m


# main program
# lets breakdown this page to two columns
col1, col2 = st.columns(2)

# User inputs
with col1:
    outer_diameter_mm = st.number_input(
        "Enter the outer diameter of the pipeline (in mm)",
        value=1000.0,
        min_value=0.0,
        step=1.0,
    )
    wall_thickness_mm = st.number_input(
        "Enter the wall thickness of the pipeline (in mm)",
        value=10.0,
        min_value=0.0,
        step=1.0,
    )
    material_type = st.text_input("Enter the material type of the pipeline", "Steel")
    material_density = st.number_input(
        "Enter the density of the pipeline material (in kg/m^3)",
        value=7850.0,
        min_value=0.0,
        step=1.0,
    )

    if st.button("Calculate"):
        dry_weight, submerged_weight = calculate_pipe_weight(
            outer_diameter_mm, wall_thickness_mm, material_density
        )
        formatted_string_subW = "{:.2f}".format(submerged_weight)
        formatted_string_dryW = "{:.2f}".format(dry_weight)
        submerged_weight_formatted = float(formatted_string_subW)
        dry_weight_formatted = float(formatted_string_dryW)
        col2.write(
            f"The dry weight of the {material_type} pipeline is {dry_weight_formatted} kN/m. \n"
            f"The submerged weight of the {material_type} pipeline is {submerged_weight_formatted} kN/m."
        )
