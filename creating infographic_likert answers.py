# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:04:20 2024

@author: Rachel N, PhD

This program creates a waffle chart infographic based on user input or imported data.
The infographic represents different categories of responses (e.g., levels of agreement or satisfaction) with colored icons.

To use this program, the user needs to have a dataset in either Excel (.xlsx) or CSV (.csv) format.
The first column of the dataset should contain the answer choices, and each subsequent column should contain
the number of responses for each answer choice. The program will create a separate waffle chart for each column of responses.

When running the program, the user will be prompted to import data.
If the user chooses to import data, they will be asked to specify the file type and file name.
If the user chooses not to import data, they will be asked to manually input the number of responses for each answer choice.

Each waffle chart will be displayed on the screen and saved as a .png file.
The file name will be the title of the figure.
If no title is provided, the file name will be the current date and time.

"""

from pywaffle import Waffle
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os
import numpy as np

# Define the categories and colors
categories = {
    '1': ['StronglyDisagree', 'SomewhatDisagree', 'Neither', 'SomewhatAgree', 'StronglyAgree', 'NA'],
    '2': ['ExtremelyDissatisfied', 'SomewhatDissatisfied', 'Neither', 'SomewhatSatisfied', 'ExtremelySatisfied', 'NA']
}
colors = ['darkorange', 'gold', 'gray', 'lightblue', 'blue', 'darkgray']

# Function to insert space after specific words
def insert_space(category):
    words_to_check = ['Strongly', 'Extremely', 'Somewhat']
    # Check if category is a string
    if isinstance(category, str):
        for word in words_to_check:
            if word in category:
                category = category.replace(word, word + ' ')
    return category

# Ask the user if they want to import data
import_data = input("Do you want to import data? (yes/no) ").lower()

if import_data in ['yes', 'y']:
    # Ask the user for the file type
    file_type = input("What is the file type of your data? (excel/csv) ").lower()

    # Import the data
    if file_type == 'excel':
        file_name = input("Enter the name of your Excel file (including the .xlsx extension): ")
        df = pd.read_excel(file_name)
    elif file_type == 'csv':
        file_name = input("Enter the name of your CSV file (including the .csv extension): ")
        df = pd.read_csv(file_name)

    # Replace NaN values with 'NA'
    df = df.replace(np.nan, 'NA')

    # Create a new directory to save the figures
    directory = "printed_figures_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(directory, exist_ok=True)

    # For each column in the dataframe (excluding the first), create a waffle chart
    for column in df.columns[1:]:
        data = dict(zip([insert_space(category) for category in df.iloc[:, 0].tolist()], df[column].tolist()))
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=data,
            icons='child',
            font_size=12,
            legend={'loc': 'center left', 'bbox_to_anchor': (1, 0.5)},
            colors=colors,
            figsize=(8, 6),  # Adjust the size of the figure
            block_arranging_style='new-line',
            starting_location='NW'
        )

        # Use the column header as the title of the figure
        title = column
        plt.title(title)

        # Save the figure as a .png file with the title and current date and time as the file name
        plt.savefig(f"{directory}/{title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        plt.show()

else:
    # Ask the user for the type of infographic
    infographic_type = input("Do you want to create an infographic about agreement or satisfaction? Type 1, A, or agree for agreement and 2, S, or Satisfaction for satisfaction: ")

    # Initialize an empty dictionary to store the data
    data = {}

    # For each category, ask the user for the number of people
    for i in range(6):
        num_people = int(input(f"Enter the number of people for {categories[infographic_type][i]}: "))
        data[categories[infographic_type][i]] = num_people

    # Create the waffle chart
    fig = plt.figure(
        FigureClass=Waffle,
        rows=5,
        values=data,
        icons='child',
        font_size=12,
        legend={'loc': 'center left', 'bbox_to_anchor': (1, 0.5)},
        colors=colors,
        figsize=(8, 6),  # Adjust the size of the figure
        block_arranging_style='new-line',
        starting_location='NW'
    )

    # Ask the user if they want to create a title for the figure
    create_title = input("Do you want to create a title for the figure? (yes/no) ").lower()
    if create_title in ['yes', 'y']:
        title = input("What do you want to title it? ")
        plt.title(title)
    else:
        title = datetime.now().strftime("%Y%m%d_%H%M%S")  # Use the current date and time as the title

    plt.savefig(f"{title}.png")  # Save the figure as a .png file
    plt.show()