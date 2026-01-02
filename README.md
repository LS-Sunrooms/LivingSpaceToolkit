# Livingspace Toolkit

#  ![LivingspaceLogo](livingspacetoolkit/Resource/Livingspace_Sunrooms_logo.png)

## Introduction

The purpose of this project is to create a toolkit that LivingSpace Sunrooms customer service can use to create custom 
orders for Livingspace sunrooms.

## Getting Started

The requirements are listed in the pyproject.toml file. It is recommended the developer uses `uv` for project
management.

### Requirements

The program needs the following packages: 

- [Pyside6](https://pypi.org/project/PySide6/)
- [PyYAML](https://pypi.org/project/PyYAML/)

### Installing

To build the project into an executable use Nuitka.
1. Install dependencies: `uv sync` & `uv sync --group dev`
2. Activate the Python environment and open a terminal in that environment.
3. The directory you should be in is the top level directory with the pyproject.toml file.
4. To compile the project into an executable run the following command: `nuitka livingspacetoolkit/main.py`
   1. The options for this compilation are listed in the main.py file.

### Usage:

To use this app effectively you must first select a scenario. These scenarios are two variables that are needed to solve
the rest of the equations given the overhang distance, panel thickness, end cut type, and widths of the three walls that
will be connected to the existing structure. Selecting a scenario will enable or disable some text boxes depending on 
what you need to input

If you select a scenario that uses the pitch then you can choose to input it as either a ratio or an angle. Ratios are
comely used and its basically how many inches the roof will rise per foot. So a 5.5/12 means it will rise 5.5 inches for
every foot the roof is from the existing structure. 

The overhang is the distance the roof will stick out from the wall of the sunroom. These serve many purposes for
architecture such as protection from rain, shading, and rain water management. The watermark for this text box is
`0' or 0" ` and that means you can input the distance as a length using standard American inch or feet. These include:
`12"`, `12in`, `1'`, `1ft`. If you do not include a unit of measure it will assume inches.

Livingspace Sunrooms use two different types of roof panels, Eco Green and Aluminum. These two panel types have a
different set of panel thicknesses for each. When you select the panel type the available set of panel thickness will
populate the combo box. 

The next selection is the end cuts. This is how the ends of the panels will be cut before they are delivered on site.
Uncut means they will be cut on site. Plum cut means they will be cut before delivery and will be cut such that the ends
will be perpendicular to the ground. 

Fascia is left as a checkbox. Fascia is an architectural term for a vertical frieze or band under a roof edge. This is
visible to outside observers and can be important for the appearance of the sunroom. Fascia is only available for uncut
roof edges at certain panel thicknesses. If your selection meets the criteria then the checkbox will be automatically
enabled and checked.

The center of the app has more text boxes that you fill in based on the scenario selected. You must always fill out the
A, B, and C walls because you need to have the dimensions of the new sunroom. Just like the overhang text box you can
put your lengths in inches, feet, or a combination of the two. That means these are acceptable inputs: `10' - 5"`,
`10ft - 5in`, `125in`, `125"`, `125 1/2"`, `10 1/8' - 9 3/4"`, `125`.  It should figure out fractions but my RegEx
skills do need work.

The diagrams are there to give a visual representation of the sunroom you are designing. For the studio type sunroom the
house wall is the existing structure. On the top diagram it is opposite the B Wall. On the bottom diagram the A, B, and
C walls shown are their widths. For the cathedral the house wall is, again, opposite the B wall but you should visualize
it as two studio types that are back-to-back.

To give the user a better understanding of what the fields in the center are allow me to provide some quick definitions.
The Peak Height is the at the base of the roof panel as it attaches to the existing structure. The base of the panel
attaches to the structure and the bottom of the panel that is attached is the peak measured from the ground. The Max
Height is the maximum allowable height the sunroom can be. The Wall Heights are the height of the sunroom walls. The
Soffit Height is the distance, from the ground, to the point where the overhang begins. A soffit is the structure that
connects the roof panels to the walls. Finally, the Drip Edge Height is the distance, from the ground, to the edge of
the top of the roof panel where rain water would fall off. You usually attach a gutter system here.

Once you've filled in the fields that are enabled, selected your roofing type, panel thickness, end cuts, and if you
want fascia you can press the Calculate button. It will run the math and give you the rest of the sunroom dimensions.
It will also give you the total area of the roof, the number of panels the roof needs assuming the panels are 32" wide,
the length of the hang rails (used to make a flush connection the existing structure), and the length of the fascia
for each side if selected. The results will also compute the number of ceiling panels needed based on the roof area.
These calculations are company specific and based on the supplier's specification. The ceiling panels are placed on top
of the roof to protect against weather.

Since this program was written specifically for Livingspace Sunrooms these numbers are designed to work with their ERP
system.

### Testing

Unlike the previous version of this project I have included a dozens of tests. These test the core functions and the gui
interface. From the project directory run `pytest` if you have the `dev` group installed using `uv`.

### Screenshots

![Disabled View](images/Screenshot_1.png)

![StudioView](images/Screenshot_2.png)

![CathedralView](images/Screenshot_3.png)

## Future Work

As of version V2.0.0 I just finished refactoring the entire project. Hopefully it will be easier for the next engineer
to maintain. The basic math for the sunroom calculations were kept the same and any updates to the math will be done by
someone who knows what they're doing.

## Versioning

This project uses semantic versioning. The current version is V2.0.0

## Authors

* **Chris McGlown Jr.** - *Initial Work* - [CMcGlownJr](https://gitlab.com/cmcglownjr)

## License

(©) 2025 LivingSpace Sunrooms. All rights reserved.
