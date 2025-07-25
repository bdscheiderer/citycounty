import csv

class County:
    def __init__(self, name, population, class_, township, seat):
        self.name = name
        self.population = population
        self.class_ = class_
        if township == "" or township == " ":
            self.township = "No"
        else:
            self.township = township
        self.seat = seat 

    def __str__(self):
        return f"{self.name} County, Population: {self.population}, Class: {self.class_}, Township: {self.township}, Seat: {self.seat}"

class City:
    def __init__(self, name, county, class_, population):
        self.name = name
        self.county = county
        self.population = population
        self.class_ = class_

    def __str__(self):
        return f"{self.name} City, Population: {self.population}, Class: {self.class_}, Seat: {self.county}"

city_data = "data/city2020.csv"     # Headers: Name, County, Class, Population
county_data = "data/county2020.csv" # Headers: Name, Population, Class, Township, Seat


def main():

    county_list = []
    with open(county_data, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        line_count = 0
        if reader.fieldnames:
            print("CSV Headers:", reader.fieldnames)
            print(type(reader.fieldnames))
        else:
            print("No headers found or file is empty.")
        for row_dict in reader:
            # Header names match class attribute names
            obj = County(row_dict['Name'], row_dict['Population'], row_dict['Class'], row_dict['Township'], row_dict['Seat'])
            county_list.append(obj)
            line_count += 1
        print(f"County data succesfully loaded. {line_count} lines processed.")

    city_list = []
    with open(city_data, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        line_count = 0
        if reader.fieldnames:
            print("CSV Headers:", reader.fieldnames)
        else:
            print("No headers found or file is empty.")
        for row_dict in reader:
            # Header names match class attribute names
            obj = City(row_dict['Name'], row_dict['County'], row_dict['Class'], row_dict['Population'])
            city_list.append(obj)
            line_count += 1
        print(f"City data succesfully loaded. {line_count} lines processed.")

    string = input("Enter city or county name: ")
    list = []
    for county in county_list:
        if county.name.lower() == string.lower():
            list.append(county)
    for city in city_list:
        if city.name.lower() == string.lower():
            list.append(city)
    if len(list) == 0:
        print("No matches found.")
    else:
        print("Found the following matches:")
        for item in list:
            print(item)

if __name__ == "__main__":
    main()