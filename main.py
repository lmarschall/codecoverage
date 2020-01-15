import json
import os

def get_urls(file_name):

    urls = []

    with open(os.path.join(os.path.dirname(__file__), file_name)) as json_file:
        data = json.load(json_file)

        for entry in data:
            urls.append(entry['url'])
        
        return urls

def create_file(file_name, index):

    css_string = ''

    with open(os.path.join(os.path.dirname(__file__), file_name)) as json_file:
        data = json.load(json_file)

        file_data = data[index]

        text = file_data['text']
        ranges = file_data['ranges']

        for range in ranges:
            start = range['start']
            end = range['end']
            css_string += text[start:end]

        text_file = open("usedonly.css", "w")
        n = text_file.write(css_string)
        text_file.close()

if __name__ == "__main__":

    loop = True

    print("Welcome to the Code Coverage Tool provided by Lukas Marschall")

    while loop:

        print("Choose your options:")
        print("1. Create used-only css file")
        print("2. Exit")

        option_choice = input("Your choice? 1|2\n")

        if(option_choice == "1"):
            file_name = input("Enter the filename: ")
            urls = get_urls(file_name)

            print("Urls in file")

            for index, url in enumerate(urls):
                print(str(index) + "-" + url)

            index = input("Choose url to create css file: ")

            create_file(file_name, int(index))

        if(option_choice == "2"):
            loop = False