import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    print('Choose a city between chicago, new york city and washington:')
    city = input('> ')
    while city not in ('chicago','new york city','washington'):
        print('invalid input ' + city)
        city = input('> ')

    # TO DO: get user input for month (all, january, february, ... , june)
    print('Choose a month between all, january, february, ... , june')
    month = input('> ')
    while month not in ('all', 'january', 'february', 'march', 'april', 'may' , 'june'):
        print('invalid input ' + month)
        month = input('> ')


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('Choose a weekday between all, monday, tuesday, ... sunday')
    day = input('> ')
    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                      'saturday', 'sunday'):
        print('invalid input ' + day)
        day = input('> ')

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the months list to get the corresponding int
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        dayi = days.index(day)

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == dayi]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month_name()

    # find the most popular month
    popular_month = df['month'].mode()[0]

    # extract day from the Start Time column to create a day column
    df['day'] = df['Start Time'].dt.weekday

    # find the most popular day index and then display the correspoding to it weekday
    popular_day = df['day'].mode()[0]
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    popular_day = days[popular_day - 1]

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most Popular Start Station:', df['Start Station'].mode()[0])
    print('Most Popular End Station:', df['End Station'].mode()[0])

    df['Start-End Station'] = df['Start Station']+' - ' + df['End Station']
    print('Most Popular Start-End Station Combination:', df['Start-End Station'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    print('Total travel time:', df['Trip Duration'].sum())
    print('Mean travel time:', df['Trip Duration'].mean())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Display counts of user types:')
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if 'Gender' in df:
        print('Display counts of gender:')
        print(df['Gender'].value_counts())
    else:
        print('Gender not available')

    if 'Birth Year' in df:
        miny = df['Birth Year'].min()
        maxy = df['Birth Year'].max()
        modey = df['Birth Year'].mode()[0]
        print('Years of birth as follows: '
              'Earliest - {}, most recent - {}, and most common - {}'.format( miny,maxy,modey ))
    else:
        print('Year of birth not available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if len(df) == 0:
            print('No Data available for selected city, month and weekday')
            break
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        i = 0
        while True:
            msg = '\nWould you like to see five (more) lines of individual trip data? '
                  'Enter yes or no.\n'
            more_data = input(msg)
            if more_data.lower() != 'yes':
                break
            print(df.iloc[i:i+5])
            i += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
