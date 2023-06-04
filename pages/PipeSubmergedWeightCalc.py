# Pipe Submerged Weight Calc
# Kenneth Brian Gomez
# Saturday, June 3, 2023
#
import streamlit as st
import math
from PIL import Image

# Set page layout to wide
st.set_page_config(layout="wide")

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

# gravity is set
grav = 9.81


# function to calculate pipe dry and submerged weight
def calculate_pipe_weight(
    outer_diameter_mm,
    wall_thickness_mm,
    cra_mm,
    ext1_mm,
    ext2_mm,
    cwc_mm,
    pipe_density,
    water_density,
    content_density,
    cra_density,
    ext1_density,
    ext2_density,
    cwc_density,
):
    # Convert mm to m for calculation
    outer_diameter = outer_diameter_mm / 1000
    wall_thickness = wall_thickness_mm / 1000
    cra = cra_mm / 1000
    ext1 = ext1_mm / 1000
    ext2 = ext2_mm / 1000
    cwc = cwc_mm / 1000

    # Calculate the inner diameter
    pipe_ID = outer_diameter - 2 * wall_thickness
    cra_ID = pipe_ID - 2 * cra
    ext1_OD = outer_diameter + 2 * ext1
    ext2_OD = ext1_OD + 2 * ext2
    cwc_OD = ext2_OD + 2 * cwc

    # Calculate outer and inner radiuses
    pipe_ro = outer_diameter / 2.0
    pipe_ri = pipe_ID / 2.0
    cra_ri = cra_ID / 2.0
    ext1_ro = ext1_OD / 2.0
    ext2_ro = ext2_OD / 2.0
    cwc_ro = cwc_OD / 2.0

    # Calculate the volume of each material
    pipeline_volume = math.pi * ((pipe_ro) ** 2 - (pipe_ri) ** 2)
    cra_volume = math.pi * ((pipe_ri) ** 2 - (cra_ri) ** 2)
    ext1_volume = math.pi * ((ext1_ro) ** 2 - (pipe_ro) ** 2)
    ext2_volume = math.pi * ((ext2_ro) ** 2 - (ext1_ro) ** 2)
    cwc_volume = math.pi * ((cwc_ro) ** 2 - (ext2_ro) ** 2)

    # Calculate the weight of each section
    pipeline_weight = pipeline_volume * pipe_density
    cra_weight = cra_volume * cra_density
    ext1_weight = ext1_volume * ext1_density
    ext2_weight = ext2_volume * ext2_density
    cwc_weight = cwc_volume * cwc_density

    # Calculate buoyancy
    displaced_water_volume = math.pi * (cwc_ro - pipe_ri) ** 2

    # Calculate the weight of the displaced water
    displaced_water_weight = displaced_water_volume * water_density

    # Calculate the total pipeline dry weight
    total_pipeline_weight = (
        pipeline_weight + cra_weight + ext1_weight + ext2_weight + cwc_weight
    )

    # Calculate the submerged weight of the pipeline
    submerged_weight = total_pipeline_weight - displaced_water_weight

    # Convert the  weight from kg/m to kN/m
    submerged_weight_kN_m = submerged_weight * 9.81 / 1000
    pipeline_weight_kN_m = total_pipeline_weight * 9.81 / 1000

    return pipeline_weight_kN_m, submerged_weight_kN_m


# main program
# lets breakdown this page to two columns
col1, col2 = st.columns(2)

# User inputs
with col1:
    # These are the pipeline dimension inputs
    outer_diameter_mm = st.number_input(
        "Enter the outer diameter of the pipeline (in mm)",
        value=450.0,
        min_value=0.0,
        step=1.0,
    )
    wall_thickness_mm = st.number_input(
        "Enter the wall thickness of the pipeline (in mm)",
        value=19.0,
        min_value=0.0,
        step=1.0,
    )

    cra_mm = st.number_input(
        "Enter the CRA thickness (in mm)",
        value=3.0,
        min_value=0.0,
        step=1.0,
    )

    ext1_mm = st.number_input(
        "Enter the thickness of the first external coating (in mm)",
        value=3.0,
        min_value=0.0,
        step=1.0,
    )

    ext2_mm = st.number_input(
        "Enter the thickness of the second external coating (in mm)",
        value=3.0,
        min_value=0.0,
        step=1.0,
    )

    cwc_mm = st.number_input(
        "Enter the concrete coating thickness (in mm)",
        value=50.0,
        min_value=0.0,
        step=1.0,
    )

    # Now we ask for the densities
    pipe_density = st.number_input(
        "Enter the density of the pipeline material (in kg/m^3)",
        value=7850.0,
        min_value=0.0,
        step=1.0,
    )

    cra_density = st.number_input(
        "Enter the density of the CRA material (in kg/m^3)",
        value=8440.0,
        min_value=0.0,
        step=1.0,
    )

    ext1_density = st.number_input(
        "Enter the density of the 1st pipeline outer coating material (in kg/m^3)",
        value=2.0,
        min_value=0.0,
        step=1.0,
    )

    ext2_density = st.number_input(
        "Enter the density of the 2nd pipeline outer coating material (in kg/m^3)",
        value=2.0,
        min_value=0.0,
        step=1.0,
    )

    cwc_density = st.number_input(
        "Enter the density of the concrete material (in kg/m^3)",
        value=3040.0,
        min_value=0.0,
        step=1.0,
    )

    content_density = st.number_input(
        "Enter the density of the pipeline content (in kg/m^3)",
        value=0.0,
        min_value=0.0,
        step=1.0,
    )

    water_density = st.number_input(
        "Enter the density of water (in kg/m^3)",
        value=1000.0,
        min_value=0.0,
        step=1.0,
    )

    if st.button("Calculate"):
        dry_weight, submerged_weight = calculate_pipe_weight(
            outer_diameter_mm,
            wall_thickness_mm,
            cra_mm,
            ext1_mm,
            ext2_mm,
            cwc_mm,
            pipe_density,
            water_density,
            content_density,
            cra_density,
            ext1_density,
            ext2_density,
            cwc_density,
        )
        formatted_string_subW = "{:.2f}".format(submerged_weight)
        formatted_string_dryW = "{:.2f}".format(dry_weight)
        submerged_weight_formatted = float(formatted_string_subW)
        dry_weight_formatted = float(formatted_string_dryW)
        col2.write(f"Pipeline dry weight is {dry_weight_formatted} kN/m. \n")
        col2.write(f"Pipeline submerged weight is {submerged_weight_formatted} kN/m.")

with col2:
    image = Image.open("Images/PipelineLayers.png")
    st.image(image, caption="Pipeline internal and external coating definition.")
