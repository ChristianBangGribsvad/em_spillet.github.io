import pandas as pd

existing_markdown_path = "index.md"
predictions_df = pd.read_csv("EM spillet 2024.csv")
output_directory = './pages'
 

#%%
all_teams = predictions_df["Which team(s) do you belong to?"].str.split(';').explode().unique()

#%%
# Read the content of the existing markdown file
with open(existing_markdown_path, 'r',encoding='utf-8') as existing_file:
    existing_content = existing_file.readlines()
#%%

for team in all_teams:
    print(team)
    #team = "Sædbanken"
        # Insert the new links after a specific line (e.g., after the line that contains "## Links")
    insertion_point = 0
    for i, line in enumerate(existing_content):
        #print(line)
        #print(f'## {team} participants')
        if f'## {team} participants' in line:
            insertion_point = i + 1
            print("is in line")
            #break
    
            # Generate the new links content
            filtered_df = predictions_df[predictions_df['Which team(s) do you belong to?'].str.contains(team)]
            
            #print(filtered_df)
            # Generate the new links content for the filtered DataFrame
            new_links = [f"- [{row['Your Name']}]({output_directory}/{row['Your Name']}.md)\n" for _, row in filtered_df.iterrows()]
        
            #new_links = [f"- [{row['Your Name']}]({output_directory}/{row['Your Name']}.md)\n" for _, row in predictions_df.iterrows()]
            
            # Insert the new links into the existing content
            existing_content = existing_content[:insertion_point] + new_links + existing_content[insertion_point:]

# Write the updated content back to the file
    with open(existing_markdown_path, 'w',encoding='utf-8') as existing_file:
        existing_file.writelines(existing_content)