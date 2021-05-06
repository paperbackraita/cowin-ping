import sys
import time
import requests
from os import system, name
from datetime import datetime


# TODO
# Add async support for multiple districts
# Add auth header generation
# Structure program
# Get all district IDs


if len(sys.argv) != 4:
    print(f"USAGE: {sys.argv[0]} City Minimum_Age Minimum_Slots")
    print(f"City: Mumbai, Delhi or Bengaluru")
    print(f"Age: 18 or 45")
    sys.exit(1)


REFRESH_RESULTS = True
CITY = sys.argv[1]
MIN_AGE = int(sys.argv[2])
CAPACITY = int(sys.argv[3])
REFRESH_RATE = 2
DISTRICT_IDS = {
                "Mumbai":
                [
                    ("395", "Mumbai"),
                ],
                "Delhi":
                [
                    ("140", "New Delhi"),
                    ("141", "Central Delhi"),
                    ("149", "South Delhi"),
                    ("144", "South East Delhi"),
                    ("150", "South West Delhi"),
                    ("142", "West Delhi"),
                    ("145", "East Delhi"),
                    ("146", "North Delhi"),
                    ("147", "North East Delhi"),
                    ("143", "North West Delhi"),
                    ("148", "Shahdara"),
                ],
                "Bengaluru":
                [
                    ("265", "Bengaluru Urban"),
                ]
            }


print(f"CITY: {CITY} \nMINIMUM_AGE: {MIN_AGE} \nMINIMUM_CAPACITY: {CAPACITY}\n\n")


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def print_appoint(appoint_dict):
    pass

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
    except Exception:
        print("#####API returned wrong response. Could not decode json.#####")
        print("#####Possibly values in the middle of refreshing. Wait for the next try.#####")
        print("#####If this error doesn't go away in 2-3 refreshes, the auth token has expired.#####")
        return None


def main():
    date = datetime.today().strftime('%d-%m-%Y')
    session_count = 0
    center_count = 0

    try:
        while True:
            print("SLOTS\tDATE\t\tPINCODE\tNAME_OF_CENTRE\n")

            appoint_list = []
            for district, dis_name in DISTRICT_IDS[CITY]:
                print(f"\nDistrict: {dis_name}")

                district_centers = get_district_centers(district, date)

                if not district_centers:
                    continue

                for center in district_centers:
                    for session in center["sessions"]:
                        """sample session: {'session_id': 'dc046d93-0c47-4f21-8882-9618439383aa', 
                        'date': '03-05-2021', 'available_capacity': 0, 'min_age_limit': 45, 'vaccine': '', 
                        'slots': ['09:00AM-11:00AM', '11:00AM-01:00PM', '01:00PM-03:00PM', '03:00PM-05:00PM']}"""

                        session_count += 1
                        if session["min_age_limit"] == MIN_AGE and session["available_capacity"] >= CAPACITY:
                            appoint = [session["available_capacity"], session["date"], center["pincode"],
                                       center["name"]]
                            for field in appoint:
                                print(field, end="\t")
                            print(end="\n")

                            appoint_list.append(appoint)

                center_count += len(district_centers)
            print(f"\n...\nGot {len(appoint_list)} appointment(s) from {center_count} center(s) and {session_count} session(s) overall.")

            if REFRESH_RESULTS:
                if appoint_list:
                    time.sleep(REFRESH_RATE*4)
                else:
                    time.sleep(REFRESH_RATE)

                clear()
            else:
                sys.exit(0)

    except KeyboardInterrupt:
        print("\n\nQuitting")


if __name__ == "__main__":
    sys.exit(main())
