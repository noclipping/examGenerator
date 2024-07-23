import json
import os

def convert_json_to_gift(json_data):
    questions = json_data["questions"]
    gift_format = ""

    for question in questions:
        gift_format += question["q_text"] + " {"
        for choice in question["q_choices"]:
            if choice["choice_correct"]:
                gift_format += "=" + choice["choice_text"] + " "
            else:
                gift_format += "~" + choice["choice_text"] + " "
        gift_format += "}\n\n"

    return gift_format

def main():
    # Prompt user for the JSON file name
    json_filename = input("Enter the JSON file name (e.g., 'example.json'): ")

    # Check if the file exists in the current directory
    if not os.path.isfile(json_filename):
        print(f"File '{json_filename}' not found in the current directory.")
        return

    # Read the JSON data from the file
    with open(json_filename, 'r') as json_file:
        json_data = json.load(json_file)

    # Convert JSON data to GIFT format
    gift_data = convert_json_to_gift(json_data)

    # Define the GIFT file name
    gift_filename = os.path.splitext(json_filename)[0] + '.gift'

    # Save the GIFT data to a file
    with open(gift_filename, 'w') as gift_file:
        gift_file.write(gift_data)

    print(f"GIFT data saved to {gift_filename}")

if __name__ == "__main__":
    main()
