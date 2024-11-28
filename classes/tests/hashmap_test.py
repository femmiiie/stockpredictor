from timeit import default_timer as timer
from classes.hashmap import *
import random
from datetime import datetime, timedelta

def gen_date(start_year=1900, end_year=2100):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime("%Y-%m-%d")

def hashmap_perf_test():
  date_list = [gen_date() for i in range(100)]

  def_start = timer()
  default = {}
  for i in date_list:
    default[i] = i

  for i in date_list:
    default[i]

  def_end = timer()
  def_difference = def_end - def_start


  cust_start = timer()
  custom = HashMap()
  for i in date_list:
    custom[i] = i

  for i in date_list:
    print(custom[i])

  cust_end = timer()
  cust_difference = cust_end - cust_start

  print(f"Default Dictionary Time: {def_difference}")
  print(f"Custom Hashmap Time: {cust_difference}")

hashmap_perf_test()