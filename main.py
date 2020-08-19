import json
import os
import re

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

        # load the file from the coverage file with the given index
        file_data = data[index]

        # get text and ranges from the file
        text = file_data['text']
        ranges = file_data['ranges']    

        # lookup for media occurances in the file, currently not fully covered by the coverage file
        media_indexes = [m.start() for m in re.finditer('@media', text)]

        media_ranges = []

        for media_index in media_indexes:
            
            # iterate through media rule with counter
            text_position = media_index

            # search for the start bracket of the media rule
            while(text[text_position] != '{'):
                text_position += 1
            
            bracket_position = text_position
            text_position += 1
            count_bracket = 1

            # search for the end bracket of the media rule
            while(count_bracket):
                if(text[text_position] == '{'):
                    count_bracket += 1
                if(text[text_position] == '}'):
                    count_bracket -= 1
                text_position += 1

            text_position -= 1

            media_ranges.append([media_index, bracket_position, text_position])
        
        # check if ranges are between media rules
        media_rules = []

        # assemble usedonly css file
        for range in ranges:
            start = range['start']
            end = range['end']
            media_index = -1

            # find if media rule exists
            for index, media_range in enumerate(media_ranges):
                media_start = media_range[1]
                media_end = media_range[2]

                # check if rule is inside media rule
                if(start > media_start and end < media_end):
                    media_index = index
            
            media_rules.append([start, end, media_index])

        # assemble the media rules in string and save to css file
        css_string = ''
        append_string = ''
        last_index = -1
        count = 1

        for media_rule in media_rules:

            start = media_rule[0]
            end = media_rule[1]
            index = media_rule[2]

            # get the text string to be appended
            # append_string += text[start:end]

            # check for end of media rule
            if (last_index != index and last_index != -1):
                css_string += '}'

            # check if new media rule started
            if (last_index != index and index != -1):

                # apply media rule and rule
                css_string += text[media_ranges[index][0]:media_ranges[index][1]+1]
            
            css_string += text[start:end]
            last_index = index
            count += 1

            # check if end is there and media rule still active
            if(len(media_rules) == count and index != -1):
                css_string += '}'

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