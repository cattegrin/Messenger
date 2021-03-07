from bs4 import BeautifulSoup
from twilio.rest import Client
import asyncio
import urllib.request
import time

sid = 'AC1a8ebc3aa32bf1ed04d4b078b3f99075'
token_file = open('token.txt', 'r')
TOKEN = token_file.read()
token_file.close()

client = Client(sid, TOKEN)


# client.messages.create(to='+13235079910', from_="+14159095746", body="You are receiving this message because you
# haven't filled out your fucking eCompliance. Fill out your fucking eCompliance.")


class person:
    def __init__(self, n, num):
        self.name = n
        self.number = num


def parse():
    data = []
    word = ''
    with open('roster.txt', 'r') as people_file:
        while True:
            char = people_file.read(1)
            if char.isspace():
                if word:
                    data.append(word)
                    word = ''
            elif char == '':
                if word:
                    data.append(word)
                break
            else:
                word += char
    return data


def get_roster():
    people_data = parse()
    people = []
    x = 0

    while x < people_data.__len__():
        # print(people_data[x] +" " + people_data[x+1] + '\n')
        people.append(person(people_data[x], people_data[x + 1]))
        x += 2

    return people


def send_message():
    people = get_roster()
    for p in people:
        #client.messages.create(to=p.number, from_="14159095746", body="Happy Founders Day  " + p.name + "!\n\n")
        client.messages.create(to=p.number, from_="14159095746", body=p.name + ",\nMeeting will be held at 7PM. \nThe Zoom link will be posted on Discord. \nWe will be voting on I-Week, so please show up on time. ")


send_message()
print("broadcast complete! ")
