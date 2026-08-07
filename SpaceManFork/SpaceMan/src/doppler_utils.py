from datetime import datetime


def date_str2unix_ts(date_str):

    # format string
    # %Y: Year, %m: Month, %d: Day
    # %H:%M:%S: Time
    # _GMT: Literal text
    # %z: UTC offset (+0000)
    date_format = "%Y_%m_%d_%H:%M:%S_GMT%z"

    # Convert string to datetime object
    dt = datetime.strptime(date_str, date_format)

    # Convert datetime object to Unix timestamp
    unix_timestamp = int(dt.timestamp())

    return unix_timestamp


if __name__ == '__main__':
    print(date_str2unix_ts("2025_11_04_02:15:00_GMT+0000"))
