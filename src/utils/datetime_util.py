from datetime import datetime, date


def iso_time_now() -> str:
    return date.today().isoformat()


def week_number(date: datetime = datetime(2025, 6, 1)) -> int:
    # Find the first day of the month
    first_day = date.replace(day=1)

    # Calculate the week number
    adjusted_day = (
        date.day + first_day.weekday() + 1
    )  # Shift day by the weekday of the first day
    # print("date:",date)
    # print("first_day",first_day)
    # print((adjusted_day // 7))

    return adjusted_day // 7
