from selenium import webdriver
import chromedriver_autoinstaller
import pandas as pd
import csv
from starter import *


# gets top scores from and writes them to a csv file
def checker():
    sizes = ['small', 'medium', 'large']
    bestDirectory = {}
    driver = webdriver.Chrome()
    for size in sizes:
        for j in range(1, 161):
            driver.get('https://170-leaderboard.vercel.app/input/' + size + '/' + f'{j}')
            score = driver.find_element("xpath", '/html/body/div/div/div/div/table/tbody/tr[1]/td[3]')
            bestDirectory[f'{size}{j}'] = score.text

    with open('bestscores.csv', 'w') as wrt:
        writer = csv.writer(wrt)
        writer.writerow(['Graph', 'Score'])
        for i in bestDirectory.keys():
            k = []
            k.append(i)
            k.append(bestDirectory[i])
            writer.writerow(k)

def read_partition(G, path: str):
    with open(path) as fp:
        arr = json.load(fp)
    size = arr[-1]["nodeId"] - arr[0]["nodeId"]
    if size != 99 and size != 299 and size != 999:
        print(path + "IS BADLY FORMED")
    for i in range(len(arr)):
        team = arr[i]["communityId"] + 1
        G.nodes[i]['team'] = team
    return G

def compareScores():
    best = pd.read_csv('bestscores.csv')
    id = best['Graph']
    sc = best['Score']
    sizes = ['small']
    dict = {}
    for size in sizes:
        for j in range(1, 261):
            G = read_input('./inputs/' + size + str(j) + '.in')
            name = size + str(j)
            scor = float('inf')
            lis = []
            for i in range(2, 27):  
                read_partition(G, './sample_partition_2/'+ name + '_part' + str(i)+ '.in')
                scor = score(G)
                lis.append(scor)
            dict[name] = min(lis)

            
    count = 0
    for k in range(160):
        if id[k] == list(dict.keys())[k]:
            print(id[k], sc[k], list(dict.values())[k])
            if sc[k] >= list(dict.values())[k]:
                count += 1
    print(count)



            
if __name__ == "__main__":
    chromedriver_autoinstaller.install()
    compareScores()

