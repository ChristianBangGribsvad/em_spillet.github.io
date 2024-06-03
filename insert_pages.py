import pandas as pd


def update_pages(predictions_df,todays_schmeichel):

    existing_markdown_path = "index_template.md"
    pages_loc = "./pages"
    output_directory = 'index.md'
     
    
    
    
    #%%
    all_teams = predictions_df["Which team(s) do you belong to?"].str.split(';').explode().unique()
    
    #%%
    # Read the content of the existing markdown file
    with open(existing_markdown_path, 'r',encoding='UTF-8') as existing_file:
        existing_content = existing_file.readlines()
    #%%
    
    team_string = []
    for team in all_teams:
        print(team)
        team_string.append(f"# {team}\n \n")
        team_string.append(f"![{team}](https://github.com/ChristianBangGribsvad/em_spillet.github.io/blob/master/assets/images/lines_{team}.svg?raw=true)\n \n")
        team_string.append(f"## {team} participants:\n")        
        filtered_df = predictions_df[predictions_df['Which team(s) do you belong to?'].str.contains(team)]
        members =  [f"- [{row['d_name']}]({pages_loc}/{row['f_name']}.html)\n" for _, row in filtered_df.iterrows()]
        for s in members:
            team_string.append(s)
        team_string.append("\n")
        team_string.append("-----------\n \n")        
        
    #print(team_string)
    s_string = []
    for name in todays_schmeichel.keys():
        output_file_path = f"[see their predictions]({pages_loc}/{todays_schmeichel[name]['fname']}.html)"
        s_string.append(f"{name} with {todays_schmeichel[name]['value']} points part of {todays_schmeichel[name]['group']} " + output_file_path)
    
    insertion_point = 0
    for i, line in enumerate(existing_content):
        if 'TEAMS' in line:
            insertion_point = i + 1
            existing_content = existing_content[:insertion_point-1] + team_string + existing_content[insertion_point:]
    for i, line in enumerate(existing_content):
        if "# Today's Schmeichel(s):" in line:
            insertion_point = i + 1
            existing_content = existing_content[:insertion_point] + s_string + existing_content[insertion_point:]
    
    # Write the updated content back to the file
        with open(output_directory, 'w',encoding='UTF-8') as existing_file:
            existing_file.writelines(existing_content)