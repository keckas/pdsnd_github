import time
import pandas as pd
import numpy as np

# List of data files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Dictionaries of known input keywords
INPUT_KEYWORDS_CITIES = { 'chicago' : 'chicago',
                          'new york city': 'new york city',
                          'new york': 'new york city',
                          'ny': 'new york city',
                          'nyc': 'new york city',
                          'washington': 'washington' }
INPUT_KEYWORDS_MONTHS = { 'january': 1,
                          'jan': 1,
                          '1': 1,
                          'february': 2,
                          'feb': 2,
                          '2': 2,
                          'march': 3,
                          'mar': 3,
                          '3': 3,
                          'april': 4,
                          'apr': 4,
                          '4': 4,
                          'may': 5,
                          '5': 5,
                          'june': 6,
                          'jun': 6,
                          '6': 6,
                          'july': 7,
                          'jul': 7,
                          '7': 7,
                          'august': 8,
                          'aug': 8,
                          '8': 8,
                          'september': 9,
                          'sep': 9,
                          '9': 9,
                          'october': 10,
                          'oct': 10,
                          '10': 10,
                          'november': 11,
                          'nov': 11,
                          '11': 11,
                          'december': 12,
                          'dec': 12,
                          '12': 12,
                          'all': 99,
                          '-': 99,
                          '': 99 }
INPUT_KEYWORDS_WEEKDAYS = { 'monday': 1,
                            'mon': 1,
                            '1': 1,
                            'tuesday': 2,
                            'tu': 2,
                            'tue': 2,
                            'tues': 2,
                            '2': 2,
                            'wednesday': 3,
                            'wed': 3,
                            '3': 3,
                            'thursday': 4,
                            'th': 4,
                            'thu': 4,
                            'thur': 4,
                            'thurs': 4,
                            '4': 4,
                            'friday': 5,
                            'fri': 5,
                            '5': 5,
                            'saturday': 6,
                            'sat': 6,
                            '6': 6,
                            'sunday': 7,
                            'sun': 7,
                            '0': 7,
                            '7': 7,
                            'all': 99,
                            '-': 99,
                            '': 99 }

# List of months and weekdays in text form
OUTPUT_KEYWORDS_MONTHS = ['', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
OUTPUT_KEYWORDS_WEEKDAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            keyword = input("Would you like to see data for Chicago, New York or Washington?\n>>> ").lower()
        finally:

            # look up inputed value in a dictionary of known keywords
            if keyword in INPUT_KEYWORDS_CITIES:
                city = INPUT_KEYWORDS_CITIES[keyword]
                break
            else:
                print("Unknown city \"{}\".".format(keyword))

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            keyword = input("For which month? (eg. January, Jan, 1, ...) Type \"all\" if you want whole year.\n>>> ").lower()
        finally:

            # look up inputed value in a dictionary of known keywords
            if keyword in INPUT_KEYWORDS_MONTHS:
                month = INPUT_KEYWORDS_MONTHS[keyword]
                # Check whether month between January and June (otherwise data not available), 99 means "all"
                if (month <= 6 or month == 99):
                    break
                else:
                    print("Data for given month \"{}\" not available. Choose month between January and June.".format(OUTPUT_KEYWORDS_MONTHS[month]))
            else:
                print("Unknown month \"{}\".".format(keyword))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            keyword = input("For which day of the week? (eg. Monday, Mon, 1, ..., Sunday = 0). Type \"all\" if you want whole year.\n>>> ").lower()
        finally:

            # look up inputed value in a dictionary of known keywords
            if keyword in INPUT_KEYWORDS_WEEKDAYS:
                day = INPUT_KEYWORDS_WEEKDAYS[keyword]
                break
            else:
                print("Unknown day of the week \"{}\".".format(keyword))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Read from CSV file
    print("\nLoading data for city \"{}\"".format(city.title()), end="", flush=True)
    df = pd.read_csv(CITY_DATA[city])

    # Calculate data for filtering
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["weekday"] = df["Start Time"].dt.dayofweek+1
    df["hour"] = df["Start Time"].dt.hour

    # Filter months (99 means no filter)
    if month < 99 :
        print(", {} only".format(OUTPUT_KEYWORDS_MONTHS[month].title()), end="", flush=True)
        df = df.loc[df["month"] == month]

    # Filter days of week (99 means no filter)
    if day < 99 :
        print(", {} only".format(OUTPUT_KEYWORDS_WEEKDAYS[day].title()), end="", flush=True)
        df = df.loc[df["weekday"] == day]

    print(" completed.\n", flush=True)
    print('-'*40)

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month (if no filter)
    if month == 99:
        print("Most common month: {} ({} trips)".format(OUTPUT_KEYWORDS_MONTHS[df["month"].mode()[0]].title(),df["month"].value_counts().iloc[0]))
    else:
        print("Data filter: {} only.".format(OUTPUT_KEYWORDS_MONTHS[month].title()))

    # display the most common day of week (if no filter)
    if day == 99:
        print("Most common day of week: {} ({} trips)".format(OUTPUT_KEYWORDS_WEEKDAYS[df["weekday"].mode()[0]].title(),df["weekday"].value_counts().iloc[0]))
    else:
        print("Data filter: {} only.".format(OUTPUT_KEYWORDS_WEEKDAYS[day].title()))

    # display the most common start hour
    print("Most common start hour: {} ({} trips)".format(df["hour"].mode()[0],df["hour"].value_counts().iloc[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # add columnt for trips (start + end station)
    df["trip"] = df["Start Station"] + " --> " + df["End Station"]

    # display most commonly used start station
    print("Most common used start station: {} (used {} times)".format(df["Start Station"].mode()[0].title(),df["Start Station"].value_counts().iloc[0]))

    # display most commonly used end station
    print("Most common used end station: {} (used {} times)".format(df["End Station"].mode()[0].title(),df["End Station"].value_counts().iloc[0]))

    # display most frequent combination of start station and end station trip
    print("Most common trip: {} (used {} times)".format(df["trip"].mode()[0].title(),df["trip"].value_counts().iloc[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total trips
    print("Total number of trips: {}".format(df["trip"].count()))

    # display total travel time
    travel_time_sum = df["Trip Duration"].sum()
    print("Total travel time: {} days, {} hours, {} minutes and {} seconds".format(int(travel_time_sum // (60*60*24)), int(travel_time_sum // (60*60) % 24), int(travel_time_sum // 60 % 60), int(travel_time_sum % 60)))

    # display mean travel time
    travel_time_mean = int(df["Trip Duration"].mean())
    print("Mean travel time: {} hours, {} minutes and {} seconds".format(int(travel_time_mean // (60*60)), int(travel_time_mean // 60 % 60), int(travel_time_mean % 60)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types (if data available)
    if 'User Type' in df.keys():
        print("Trips by user types:")
        print(df["User Type"].value_counts().to_string()+"\n")
    else:
        print("User type not available in provided data.\n")

    # Display counts of gender (if data available)
    if 'Gender' in df.keys():
        print("Trips by user gender:")
        print(df["Gender"].value_counts().to_string()+"\n")
    else:
        print("Gender not available in provided data.\n")

    # Display earliest, most recent, and most common year of birth (if data available)
    if 'Birth Year' in df.keys():
        print("Oldest user born in year {}.".format(int(df["Birth Year"].min())))
        print("Youngest user born in year {}.".format(int(df["Birth Year"].max())))
        print("Most common year of birth: {}".format(int(df["Birth Year"].mode()[0])))
    else:
        print("Birth year not available in provided data.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # ask whether user wants to see raw data
        while True:
            try:
                raw_data = input('\nWould you like to view raw data? Enter "show" (view in console) or "save" (save to "output.csv"). Any other input means "no".\n>>> ').lower()
            finally:

                # show raw_data
                if raw_data == 'show':
                    rows = df.shape[0]
                    print("\nThere are {} rows in raw data. Showing first 5 rows, to show more press Enter. To quit enter \"exit\" and press Enter.\n".format(rows))

                    i = 0 # iterator
                    while True:
                        print(df[i:min(i+5, rows)].to_string(index=False))
                        i += 5

                        # stop when we reached the end
                        if (i >= rows):
                            print("\n"+"-"*10+"END OF RAW DATA"+"-"*10+"\n")
                            break

                        # show more rows?
                        try:
                            show_more = input('>>> Press Enter to show more. Type "exit" and press Enter to stop. ').lower()
                        finally:
                            if not show_more in {"", "yes", "more"}:
                                break;


                # save raw_data to csv
                elif raw_data == 'save':
                    try:
                        df.to_csv('output.csv')
                    except:
                        print('An exception occurred during saving file \"output.csv\". Close the file and try it again.\n')
                    else:
                        print("Raw data saved to file \"output.csv\".\n")

                # if no selection, end this analyze
                else:
                    break

        # ask if user wants to run the program again
        try:
            restart = input('\nWould you like to restart? Enter yes or no.\n>>> ').lower()
        finally:
            if restart != 'yes':
                print("\nHave a nice day!\n")
                break

if __name__ == "__main__":
	main()
