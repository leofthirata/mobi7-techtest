import pandas as pd


def get_average_speed(df):
    """ Function to get calculate the average speed """
    speed_df = df['raw'].map(
        lambda x: int(x[68:72], base=16) + int(x[72:74], base=16) / 10)

    return speed_df.mean()


def get_time(df):
    """ Function to get the moment the data were gathered """
    time_sec = df['raw'].map(
        lambda x: int(x[106:108], base=16) * 60 * 60 + int(x[108:110], base=16) * 60 + int(x[110:112], base=16))

    return time_sec[:-1]


def get_current_mileage(df):
    """ Function to get the current mileage """
    mileage = df['raw'].map(
        lambda x: int(x[130:134], base=16) + (int(x[134:136], base=16) / 10))

    return mileage[:-1]


def get_total_mileage(df):
    """ Function to get the total mileage """
    mileage = df['raw'].map(
        lambda x: int(x[136:144], base=16) + (int(x[144:146], base=16) / 10))

    return mileage[:-1]


def get_distance_from_x_to_y(df, begin, end):
    """
        Function to get the total distance tracked from time x to y

        PS: there are 3 methods to acquire this distance:
        - 1. Using the distance from current mileage bytes
        - 2. Using the distance from total mileage bytes
        - 3. Using the distance calculated by the average speed and the time spent from x to y
        Uncomment the lines 58-60 to see the results from the three methods listed above
    """
    hour = [int(value[106:108], base=16) for value in df['raw'].values]
    hour.pop()

    end_index = hour.index(end - 1) + 1
    begin_index = list(reversed(hour)).index(begin) + len(df) - 2

    mileage = get_current_mileage(df)
    distance_from_current_mileage = mileage[end_index] - mileage[begin_index]

    mileage = get_total_mileage(df)
    distance_from_total_mileage = mileage[end_index] - mileage[begin_index]

    time_sec = get_time(df)
    distance_calculated = get_average_speed(df) * (time_sec[end_index] - time_sec[begin_index]) / 3600

    # print(distance_from_total_mileage)
    # print(distance_from_current_mileage)
    # print(distance_calculated)

    return distance_from_current_mileage


def main():
    data = pd.read_excel('position_db.xlsx')
    df = pd.DataFrame(data, columns=['raw'])
    print(f"Velocidade média = {get_average_speed(df)}km/h")
    print(f"Distância percorrida das 10h as 11h = {get_distance_from_x_to_y(df, 10, 11)}km")


if __name__ == "__main__":
    main()
