import os
import pandas as pd

# Define the directory containing images and the output directory for markdown files
image_directory = './plots'
output_directory = './pages'

predictions_df = pd.read_csv("EM spillet 2024.csv")
#%%

# Iterate over each row in the DataFrame
for index, row in predictions_df.iterrows():
    name = row['Your Name']
    group = row['Which team(s) do you belong to?']
    group = group.replace(";"," and ")
    image_path = os.path.join(image_directory, f"{name}_table.png")
    
    # Create markdown content
    markdown_content = f"""
#Results of {name} 

Part of {group}

See your results in the table below:

![{name}]({image_path})

"""
    # Define the output file path
    output_file_path = os.path.join(output_directory, f"{name}.md")
    
    # Write the markdown content to the file
    with open(output_file_path, 'w') as file:
        file.write(markdown_content)

print("Markdown pages have been created successfully.")
