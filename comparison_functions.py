import argparse
import argparse
import json
import os
import subprocess

def fetch_binary_packages(branch):
    """
    Получает список бинарных пакетов для заданного branch с помощью curl.
    """
    temp_file = f"temp_{branch}.json"
    command = f"curl -X 'GET' 'https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}' -H 'accept: application/json' > {temp_file}"
    subprocess.run(command, shell=True)
    with open(temp_file, "r") as f:
        packages = json.load(f)  # Загружаем весь JSON
        packages = [value for value in packages.values() if isinstance(value, list)]  # Фильтруем только списки
        packages = [item for sublist in packages for item in sublist]  # Объединяем списки
    os.remove(temp_file)  # Удаление временного файла
    return packages

def compare_package_lists(packages1, packages2):
    """
    Сравнивает два списка пакетов и возвращает JSON с результатами сравнения.
    """
    set1 = {pkg['name'] for pkg in packages1}
    set2 = {pkg['name'] for pkg in packages2}

    in_first_only = [{"name": pkg, "version-release": f"{pkg1['version']}-{pkg1['release']}"} 
                     for pkg1 in packages1 
                     for pkg in set1 - set2 
                     if pkg1['name'] == pkg]

    in_second_only = [{"name": pkg, "version-release": f"{pkg2['version']}-{pkg2['release']}"} 
                     for pkg2 in packages2 
                     for pkg in set2 - set1
                     if pkg2['name'] == pkg]

    greater_in_first = []
    for pkg1 in packages1:
        for pkg2 in packages2:
            if pkg1['name'] == pkg2['name'] and f"{pkg1['version']}-{pkg1['release']}" > f"{pkg2['version']}-{pkg2['release']}":
                if {"name": pkg1['name'], "version-release": f"{pkg1['version']}-{pkg1['release']}"} not in greater_in_first:
                    greater_in_first.append({"name": pkg1['name'], "version-release": f"{pkg1['version']}-{pkg1['release']}"} )
    return {
        "in_first_only": in_first_only,
        "in_second_only": in_second_only,
        "greater_in_first": greater_in_first
    }
