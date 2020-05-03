import logging
import csv
import re
import pprint

def open_csv():
    csv_file = open('../csv/commits.csv')
    csv_reader = csv.reader(csv_file)
    return list(csv_reader)

def extract_number(str):
    regex = re.compile(r'\d+')
    value = int(regex.search(str).group())
    return value

def analyse_csv(csv_reader):
    results = {}
    for i in range(0, len(csv_reader), 3):
        # Author取り出し
        author = csv_reader[i][2]
        # addition deletion 取り出し
        length = len(csv_reader[i + 1])
        insertion = 0
        if length >= 2:
            insertion = extract_number(csv_reader[i + 1][1])
        deletion = 0
        if length >= 3:
            deletion = extract_number(csv_reader[i + 1][2])
        modification = insertion + deletion
        if author not in results.keys():
            results[author] = {}
            results[author]['insertion'] = insertion
            results[author]['deletion'] = deletion
            results[author]['modification'] = modification
        else:
            results[author]['insertion'] += insertion
            results[author]['deletion'] += deletion
            results[author]['modification'] += modification
    return results

def sum(data, key):
    result = 0
    for author in data.keys():
        result += data[author][key]
    return result

def round_down(value):
    value * 100

def calculate_proprotion(data):
    results = {}
    total_insertion = sum(data, 'insertion')
    total_deletion = sum(data, 'deletion')
    total_modification = sum(data, 'modification')
    for author in data.keys():
        results[author] = {}
        results[author]['insertion'] = '{:.0%}'.format(data[author]['insertion'] / total_insertion)
        results[author]['deletion'] = '{:.0%}'.format(data[author]['deletion'] / total_deletion)
        results[author]['modification'] = '{:.0%}'.format(data[author]['modification'] / total_modification)
    return results

def print_result(data):
    for author in data.keys():
        print('author: {} insertion: {} deletion: {} modification: {}'.format(
          author,\
          data[author]['insertion'],
          data[author]['deletion'],\
          data[author]['modification']))

result = analyse_csv(open_csv())
print('total')
print_result(result)

print('proportion')
print_result(calculate_proprotion(result))