import re
import random
from datetime import datetime, timedelta


# *************************   Task 1   *************************

def get_days_from_today(date: str) -> int:
  """Returns the number of days from today to the given date string in 'YYYY-MM-DD' format.
  If the date format is incorrect, prints an error message and returns None.

  Args:
    date (str): The date string in 'YYYY-MM-DD' format.

  Returns:
    int: The number of days from today to the given date, or None if the format is incorrect.
  """
  try:
    date_obj = datetime.strptime(date, "%Y-%m-%d")
  except ValueError:
    print("Wrong data format")
    return None
  else:
    days_diff = date_obj.date() - datetime.now().date()

    return -days_diff.days

# Task 1 example usage
print(get_days_from_today("2000-01-01"))


# *************************   Task 2   *************************

def get_numbers_ticket(min: int, max: int, quantity: int) -> list:
  """Generates a sorted list of unique random numbers within a specified range.
  Args:
    min (int): The minimum value of the range (inclusive).
               Should be between 1 and 999.
    max (int): The maximum value of the range (inclusive).
               Should be between 1 and 999.
    quantity (int): The number of unique random numbers to generate.
                    Should be a positive integer.
  Returns:
    list: A sorted list of unique random numbers within the specified range.
  """
  if min not in range(1,1000) or max not in range(1,1000) or quantity <= 0 or (max < min) or (max - min) < quantity:
    return []

  s = set()

  while len(s) != quantity:
    num = random.randint(min, max)
    s.add(num)

  return sorted(s)

# Task 2 example usage
lottery_numbers = get_numbers_ticket(1, 49, 6)
print("Ваші лотерейні числа:", lottery_numbers)


# *************************   Task 3   *************************

def normalize_phone(phone_number: str) -> str:
  """
  Normalizes a phone number by removing unwanted characters and ensuring
  it has the correct format.
    Args:
        phone_number (str): The raw phone number string.
    Returns:
        str: The normalized phone number in the format +380XXXXXXXXX.
  """
  pattern = r"[^0-9+]"
  replacement = ""

  norm_number = re.sub(pattern, replacement, phone_number)
  if norm_number[0] != "+":
    if norm_number[0:2] != "38":
      norm_number = "+38" + norm_number
    else:
      norm_number = "+" + norm_number

  return norm_number


# Task 3 example usage

raw_numbers = [
    "067\\t123 4567",
    "(095) 234-5678\\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)


# *************************   Task 4   *************************

def check_holiday(date_obj: datetime, diff: int) -> str:
  """ Helper function to adjust birthday dates falling on weekends.
  If the birthday falls on a Saturday or Sunday, it moves the date
  to the next Monday"""
  if date_obj.isoweekday() == 6:
     if diff < 5:
      date_obj = date_obj + timedelta(days=2)
     else:
      # Differeence between birthday and today is more than 7 days,
      # so we skip this birthday
      return None
  elif date_obj.isoweekday() == 7:
     if diff < 6:
      date_obj = date_obj + timedelta(days=1)
     else:
      return None

  return f"{date_obj.year}.{date_obj.month}.{date_obj.day}"


def get_upcoming_birthdays(users: list) -> list:
  """Returns a list of users with birthdays in the next 7 days, adjusting for weekends.
  If a birthday falls on a weekend, the congratulation date is moved to the next Monday
  Args:
    users (list): A list of dictionaries, each containing 'name' and 'birthday' keys.
                  The 'birthday' value should be in 'YYYY.MM.DD' format.    
    Returns:
       list: A list of dictionaries with 'name' and 'congratulation_date' keys."""
  
  ret = []

  today_obj = datetime.now().date()
  YEAR = today_obj.year

  for i in range(len(users)):
    user_date_obj = datetime.strptime(str(YEAR) + users[i]["birthday"][4:], "%Y.%m.%d").date()
    user_date_ny_obj = datetime(year=YEAR+1, month=user_date_obj.month, day=user_date_obj.day).date()

    diff = user_date_obj - today_obj
    diff_ny = user_date_ny_obj - today_obj

    if diff.days >= 0 and diff.days <= 6:
        day = check_holiday(user_date_obj, diff.days)
        if day:
            ret.append({"name":users[i]["name"], 'congratulation_date':day})
    elif diff_ny.days <= 6:
        day = check_holiday(user_date_ny_obj, diff_ny.days)
        if day:
            ret.append({"name":users[i]["name"], 'congratulation_date':day})

  return ret


# Task 4 example usage

users = [
    {"name": "John Doe", "birthday": "1985.10.09"},
    {"name": "Jane Smith", "birthday": "1990.10.05"}
]

upcoming_birthdays = get_upcoming_birthdays(users)
print("Список привітань на цьому тижні:", upcoming_birthdays)
