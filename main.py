def save_countries_to_file(countries, filename):
    with open(filename, 'w') as file:
        for country in countries:
            file.write(country + '\n')

if __name__ == "__main__":
    countries = [
        "Albania", "Austria", "Belgium", "Croatia", "Czech Republic", 
        "Denmark", "England", "France", "Georgia", "Germany", 
        "Hungary", "Italy", "Netherlands", "Poland", "Portugal", 
        "Romania", "Scotland", "Serbia", "Slovakia", "Slovenia", 
        "Spain", "Switzerland", "Turkey", "Ukraine"
    ]

    filename = "countries.txt"
    save_countries_to_file(countries, filename)
    print(f"Countries saved to {filename}")
