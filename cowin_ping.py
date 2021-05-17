import sys
import yaml
import time
import requests
from os import system, name
from datetime import datetime


if len(sys.argv) < 3 or "--help" in sys.argv or "-h" in sys.argv:
    print(f"USAGE: {sys.argv[0]} [city] [minimum_age]")
    print(f"city: Mumbai, Delhi, Bengaluru (for more options, see district_mapping.yaml)")
    print(f"age: 18, 45")
    print("Use --no-refresh to run the script once and quit")
    sys.exit(1)


REFRESH_RESULTS = False if "--no-refresh" in sys.argv else True
CITY = sys.argv[1]
MIN_AGE = int(sys.argv[2])
REFRESH_RATE = 1
CITY_ID_FILE_LOCATION = "./district_mapping.yaml"


def print_to_term(appoint_list):
    def clear():
        # for windows
        if name == 'nt':
            _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

    if appoint_list:
        # Ring terminal bell if appointments available
        sys.stdout.write('\a')
        sys.stdout.flush()

    if REFRESH_RESULTS:
        if appoint_list:
            # _ = input("Press any key to continue...")
            rate = REFRESH_RATE * 5
        else:
            rate = REFRESH_RATE

        print(f"Refreshing after {rate} seconds...")
        time.sleep(rate)

        clear()
        return True
    else:
        return False


# def print_appoint(appoint_dict):
#     pass


def get_district_ids():
    try:
        with open(CITY_ID_FILE_LOCATION) as mapping_file:
            mapping = yaml.safe_load(mapping_file)
            return mapping
    except yaml.YAMLError as ye:
        print(f"#####Could not understand the district mapping file {CITY_ID_FILE_LOCATION}!#####")
        print(f"#####Error: {ye}#####")
        sys.exit(1)


def get_district_centers(district_id, date):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 "
                          "Firefox/88.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5 --compressed",
            "Origin": "https://selfregistration.cowin.gov.in",
            "Connection": "keep-alive",
            "Referer": "https://selfregistration.cowin.gov.in/",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "Trailers",
        }
        response = requests.get(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?"
                                f"district_id={district_id}&date={date}", headers=headers).json()
        return response["centers"]
    except KeyError as ke:
        print("#####API returned empty response. Refresh a few more times#####")
        print(f"Error: {ke}")
    except ValueError as ve:
        print("#####API returned wrong response. Could not decode json.#####")
        print(f"Error: {ve}")
    except Exception as e:
        print("#####Something unexpected happened. Lockdown 4.0 initiated. Asta La Vista#####")
        print("#####Error: ", e)
        return None


def main():
    try:
        city_district_ids = get_district_ids()

        while True:
            date = datetime.today().strftime('%d-%m-%Y')
            print(f"CITY: {CITY} \nMINIMUM_AGE: {MIN_AGE} \n\n")

            print("SLOTS\tDATE\t\tPINCODE\tVACCINE\t\tNAME_OF_CENTRE\n")

            appoint_list = []
            session_count = 0
            center_set = set()

            for dis_name, dis_id in city_district_ids[CITY].items():

                print(f"\nDistrict: {dis_name}")

                district_centers = get_district_centers(dis_id, date)

                if not district_centers:
                    continue

                for center in district_centers:
                    for session in center["sessions"]:

                        if session["min_age_limit"] == MIN_AGE:
                            center_set.add(center["center_id"])
                            session_count += 1
                            if session["available_capacity"] > 0:
                                appointment = [session["available_capacity"], session["date"], center["pincode"],
                                               session["vaccine"], center["name"]]
                                for field in appointment:
                                    print(field, end="\t")
                                print(end="\n")

                                appoint_list.append(appointment)

            print(f"\n...\nGot {len(appoint_list)} appointment(s) from {session_count} applicable slots(s) and "
                  f"{len(center_set)} center(s) overall.")

            if not print_to_term(appoint_list):
                sys.exit(0)

    except KeyboardInterrupt:
        print("\n\nCaught an interrupt. Quitting")


if __name__ == "__main__":
    sys.exit(main())
