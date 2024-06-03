import os
import pandas as pd

def create_pages(predictions_df):
    
    # Define the directory containing images and the output directory for markdown files
    image_directory = './user_plots/'
    output_directory = './pages/'
    
    
    # Iterate over each row in the DataFrame
    for index, row in predictions_df.iterrows():
        name = row['d_name']
        savename = row['f_name']
        
        group = row['Which team(s) do you belong to?']
        group = group.replace(";"," and ")
        table_path = image_directory + f"{savename}.svg"
        
        # Create markdown content
        markdown_content = f"""---
layout: default
---

# Results of {name} 
    
Part of {group}
    
See your results in the table below:
    
![{name}]({table_path}?raw=true)

[Back](https://christianbanggribsvad.github.io/em_spillet.github.io/)"""
        # Define the output file path
        output_file_path = output_directory + f"{savename}.md"
        
        # Write the markdown content to the file
        with open(output_file_path, 'w',encoding='UTF-8') as file:
            file.write(markdown_content)
    
    print("Markdown pages have been created successfully.")
