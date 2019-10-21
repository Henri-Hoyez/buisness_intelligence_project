import numpy as np
import uuid
import datetime
import pandas as pd
import os
import unidecode


cities = {}
cities["UNITED_STATES"] = [city.upper() for city in ["New York", "Chicago", "Los Angeles", "Boston", "San Francisco"]]
cities["FRANCE"] = [city.upper() for city in ["Paris","Marseille","Lyon","Toulouse","Nice","Nantes","Montpellier","Strasbourg","Bordeaux","Lille"]]
cities["CANADA"] = [city.upper() for city in ["Alberta","Colombie-Britannique","Manitoba","Nouveau-Brunswick","Terre-Neuve-et-Labrador","Nouvelle-Écosse","Ontario","Île-du-Prince-Édouard","Québec","Saskatchewan","Territoires du nord-ouest","Nunavut","Yukon"]]
cities["CHINA"] = [city.upper() for city in ["Shanghai","Pékin","Canton","Shenzhen","Dongguan"]]
cities["GERMANY"] = [city.upper() for city in ["Berlin","Hambourg","Munich","Cologne","Francfort-sur-le-Main","Stuttgart","Düsseldorf","Dortmund"]]
cities["UNITED_KINGDOM"] = [city.upper() for city in ["Londres","Birmingham","Glasgow","Manchester","Édimbourg","Liverpool","Leeds"]]
cities["SPAIN"] = [city.upper() for city in ["Madrid","Barcelone","Séville","Valencia","Bilbao"]]
countries = ["FRANCE","UNITED_STATES","CANADA","CHINA","GERMANY","UNITED_KINGDOM","SPAIN"]
countries_code = ["FR","US","CA","CN","DE","UK","ESP"]
#countries_cutomers_count = [1618474,12484979,4308817,20967793,1944205,2924028,500902]
countries_cutomers_count = [1618,12484,4308,20967,1944,2924,500]
print(np.sum(countries_cutomers_count))

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def create_customers(nb_data,country_name,country_code):
    genders = ["MAN","WOMAN"]
    ages = np.arange(18,90)
    
    random_id = [str(uuid.uuid4()) for i in range(nb_data)]
    random_genders = np.random.choice(genders,size = nb_data)
    random_ages = np.random.choice(ages,size= nb_data)
    
    dataframe = pd.DataFrame(list(zip(random_id,random_genders,random_ages)),columns =["ID_CUSTOMER","GENDER","AGE"])
    dataframe.to_csv("./generated_cars_data/customers/"+country_code.replace(" ","_").upper()+"_customers.csv", index=False)
    
def create_times(date_count,country_code):
    times_range = pd.date_range(start='1/1/2015', end='31/12/2018')
    dataframe = pd.DataFrame(list(zip(times_range,times_range.year,times_range.month,times_range.day)),columns=["ID_TIME","YEAR","MONTH","DAY"])
    dataframe.to_csv("./generated_cars_data/times/times.csv", index=False)
    
def create_sales(data_car_path,data_customers_path,times_customers_path,country_name,country_code,city):    
    car_data = pd.read_csv(data_car_path,encoding="latin-1")
    customers_data = pd.read_csv(data_customers_path,encoding="latin-1")
    times_data = pd.read_csv(times_customers_path,encoding="latin-1")

    cars_weight  = np.random.normal(0,1,len(car_data["ID_PRODUCT"]))
    cars_weight = softmax(cars_weight)  

    random_car_ids = np.random.choice(car_data["ID_PRODUCT"],size=len(customers_data["ID_CUSTOMER"]),p=cars_weight)
    random_time_ids = np.random.choice(times_data["ID_TIME"],size=len(customers_data["ID_CUSTOMER"]))
    cities_weights = np.random.normal(0,1,len(city))
    cities_weights = softmax(cities_weights)
    random_cities = np.random.choice(city,size=len(customers_data["ID_CUSTOMER"]),p= cities_weights)
    
    dataframe = pd.DataFrame(list(zip(random_car_ids,random_time_ids,customers_data["ID_CUSTOMER"],[unidecode.unidecode(random_city.replace(" ","_").replace("-","_").upper()) for random_city in random_cities])),columns=["ID_PRODUCT","ID_TIME","ID_CUSTOMER","CITY"])
    dataframe.to_csv("./generated_cars_data/sales/"+country_code.replace(" ","_").upper()+"_sales.csv", index=False)
   
def create_stores(cities,country,country_code):
    country = [country]*len(cities)
    dataframe = pd.DataFrame(list(zip([unidecode.unidecode(city.replace(" ","_").replace("-","_").upper()) for city in cities],country)),columns=["CITY","COUNTRY"])
    dataframe.to_csv("./generated_cars_data/stores/"+country_code.replace(" ","_").upper()+"_stores.csv", index=False)
    
def create_data(countries,coutries_code,countries_cutomers_count,cities,nb_date):
    if not os.path.exists("./generated_cars_data"): os.mkdir("./generated_cars_data")
    if not os.path.exists("./generated_cars_data/times"): os.makedirs("./generated_cars_data/times")
    if not os.path.exists("./generated_cars_data/customers"): os.makedirs("./generated_cars_data/customers")
    if not os.path.exists("./generated_cars_data/sales"): os.makedirs("./generated_cars_data/sales")
    if not os.path.exists("./generated_cars_data/stores"): os.makedirs("./generated_cars_data/stores")
    
    for country_data in list(zip(countries,coutries_code,countries_cutomers_count)):
        data_car_path = "products/car_cleaned_data_with_uuid.csv"
        data_customers_path =  "generated_cars_data/customers/"+country_data[1]+"_customers.csv"
        data_times_path =  "generated_cars_data/times/times.csv"
        create_customers(country_data[2],country_data[0],country_data[1])
        create_times(nb_date,country_data[1])
        create_sales(data_car_path,data_customers_path,data_times_path,country_data[0],country_data[1],cities[country_data[0]])
        create_stores(cities[country_data[0]],country_data[0],country_data[1])
        print(country_data[0])

if __name__ == "__main__":
    create_data(countries,countries_code,countries_cutomers_count,cities,100)
