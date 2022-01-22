import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# list of valid cities for user input
lst_valid_cities = ['Chicago', 'New York City', 'Washington']

# list of valid months for user input
lst_valid_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'All']

# list of valid days for user input
lst_valid_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'All']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Args:
        none

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    char_abort = 'Q'
    city = get_user_input(lst_valid_cities, 'Which city do you want to explore? (' + ', '.join(lst_valid_cities) + '; ' + char_abort +' to quit): ', char_abort)
    if city == char_abort:
        return 0

    # get user input for month (all, january, february, ... , june)
    month = get_user_input(lst_valid_months, 'Which month do you want to explore? (' + ', '.join(lst_valid_months) + '; ' + char_abort +' to quit): ', char_abort)
    if month == char_abort:
        return 0

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_user_input(lst_valid_days, 'Which day do you want to explore? (' + ', '.join(lst_valid_days) + '; ' + char_abort +' to quit): ', char_abort)
    if day == char_abort:
        return 0

    print('-'*40)
    return city, month, day


def get_user_input(lst_valid_args, str_question, chr_abort):
    """
    Asks user as long as a valid argument is passed.

    Args:
        (str) lst_valid_args - list of valid arguments
        (str) str_question - string displayed at user input
        (str) chr_abort - character that terminates the program

    Returns:
        (str) user_input - valid argument from handed over list OR character for program termination
    """
    user_input = ""
    while (user_input not in lst_valid_args) and (user_input != chr_abort):
        user_input = input(str_question).lower().title()
    return user_input


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
    print("\nLoading data for city: {}, month(s): {}, day(s) of week: {}\n".format(city, month, day))
    print('-'*40)

    #load csv-file
    df = pd.read_csv(CITY_DATA[city.lower()])

    #convert columns to datetime / timedelta data type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Trip Duration'] = pd.to_timedelta(df['Trip Duration'], unit = 's')

    #add additional columns for further calculations
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")
    df['Start End Station Combination'] = "'" + df['Start Station'] + "' and '" + df['End Station'] + "'"

    # filter for month if a month was selected
    if month != lst_valid_months[-1]:
        df = df[df['month'] == lst_valid_months.index(month) + 1]

    # filter for day if a day was selected
    if day != lst_valid_days[-1]:
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day

    Returns:
        None
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most common month: {}, {}".format(lst_valid_months[df['month'].mode()[0]-1], df['month'].mode()[0]))

    # display the most common day of week
    print("Most common day of week: {}".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print("Most common start hour: {}".format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day

    Returns:
        None
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start station: {}".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("Most commonly used end station: {}".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print("Most frequent combination of start station and end station: {}".format(df['Start End Station Combination'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day

    Returns:
        None
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time: {}".format(df['Trip Duration'].sum()))

    # display mean travel time
    print("Average travel time: {}".format(df['Trip Duration'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day

    Returns:
        None
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Number of user types: \n{}".format(df['User Type'].value_counts()))


    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nGender count: \n{}'.format(df['Gender'].value_counts()))
    else:
        print("\nNo data for 'gender' statistics available.\n")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nEarliest year of birth: {}".format(df['Birth Year'].min()))
        print("\nMost recent year of birth: {}".format(df['Birth Year'].max()))
        print("\nMost common year of birth: {}".format(df['Birth Year'].mode()[0]))
    else:
        print("\nNo data for 'date of birth' statistics available.\n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data of filtered dataset in blocks of 5 lines.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day

    Returns:
        None
    """

    print('\nDisplaying User data \n')
    start_time = time.time()
    counter = 0
    num_lines = 5
    # Display only 'num_lines' rows at a time, ask user if he/she wants to see 'num_lines' more
    while counter < df.shape[0]:
        # Display columns from original dataset, except 1st column 'Unnamed'
        print(df[counter:counter+num_lines][df.columns[1:-3]])
        if input("\nDo you want to see 5 more lines [y for yes, other for no]? ").lower() == 'y':
            counter += num_lines
            print("\nLines {} to {} of {}: \n".format(counter+1, counter + num_lines, df.shape[0]))
        else:
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            # Check if Dataframe object is not empty
            if df.empty:
                print("\nNo data could be found.")
            else:
                # Set terminal width and max. columns to display all columns
                pd.set_option('display.max_columns', None)
                pd.set_option('display.width', 300)
                # Run individual functions to display details of Dataframe object
                time_stats(df)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)
                if input("\nDo you want to see the raw data [y for yes, other for no]? ").lower() == 'y':
                    display_raw_data(df)
                else:
                    print("\nNo raw data is displayd.\n")

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        except Exception as e:
            print("Program terminates on user's request!")
            # Debugging exception with "print('Error code: {}'.format(e))"
            break


if __name__ == "__main__":
	main()
