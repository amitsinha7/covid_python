from csv import DictReader
from datetime import datetime
from heapq import nlargest


def covid_case(validate_date, file_name, display_numbers, only_location, location_type):
    with open(str(file_name), 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj)
        result = {}

        for row in csv_dict_reader:
            location = row['location']
            if is_valid_location(location, location_type) and is_eligible_date(row['date'], validate_date):
                new_cases = is_instance_vale(row['new_cases'])
                if new_cases > 0:
                    if is_location_available(result, location):
                        updated = new_cases + result.get(location)
                        dict1 = {location: updated}
                        result = result | dict1
                    else:
                        dict1 = {location: new_cases}
                        result.update(dict1)

        if only_location:
            res = nlargest(display_numbers, result, key=result.get)
            # printing result
            print("The top "+str(display_numbers)+" countries which are effected due to new arises cases are  " + str(res))
        else:
            res = nlargest(display_numbers, result, key=result.get)
            for val in res:
                print("The top "+str(display_numbers)+" countries which are effected due to new arises cases are " + val, ":",
                      result.get(val))


def is_instance_vale(data):
    if isinstance(data, float):
        if data == '':
            return int(0)
        return int(data)
    if isinstance(data, int):
        if data == '':
            return int(0)
        return data
    if isinstance(data, str):
        if data is not None:
            if data == '':
                return int(0)
        return int(data.rstrip('0').rstrip('.'))


def is_eligible_date(csv_date, validate_date):
    if csv_date is not None and csv_date != '':
        dts = datetime.strptime(str(csv_date), '%Y-%m-%d')
        csv_new_date = dts.strftime("%b") + "-" + dts.strftime("%Y")
        if csv_new_date == validate_date:
            return True
        else:
            return False
    else:
        return False


def is_location_available(result, location):
    if location in result.keys():
        return True
    else:
        return False


def is_valid_country(location):
    if location in {"World", "Europe", "Africa", "Asia", "European Union", "International", "South America",
                    "North America"}:
        return False
    else:
        return True


def is_valid_location(location, location_type):
    if location is not None and location != '':
        if location_type == "ALL":
            return True
        if location_type == "COUNTRY":
            return is_valid_country(location)
    else:
        return False


covid_case("Feb-2021", "C://Users//Amit Sinha//Downloads//full_data.csv", 10, True, "COUNTRY")
