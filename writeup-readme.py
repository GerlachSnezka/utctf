import json
import os
from urllib.parse import unquote
from datetime import datetime

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def generate_writeup(data, year):
    categories = {}

    for challenge in data['data']:
        category = challenge['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(challenge)

    for category, challenges in categories.items():
        category_dir = os.path.join(str(year), category.lower().replace(" ", "-")) 
        os.makedirs(category_dir, exist_ok=True)

        for challenge in challenges:
            name_decoded = unquote(challenge['name'])
            name_lowercase = name_decoded.lower() 
            name_with_dash = name_lowercase.replace(" ", "-")  
            challenge_file_path = os.path.join(category_dir, f"{name_with_dash}.md")

            solved = "✔" if challenge['solved_by_me'] else "❌"
            with open(challenge_file_path, 'w') as f:
                f.write(f"---\n")
                f.write(f"title: {name_decoded}\n")
                f.write(f"description: sample - {name_decoded}\n")  
                f.write(f"points: {challenge['value']}\n")
                f.write(f"solves: {challenge['solves']}\n")
                f.write(f"---\n\n")
                f.write(f"yeh' {name_decoded}.... it was hard lol\n")

        with open(os.path.join(category_dir, 'README.md'), 'w') as readme_file:
            readme_file.write(f"# {category.capitalize()} Challenges\n\n")
            readme_file.write("List of challenges in this category:\n\n")
            for challenge in challenges:
                name_decoded = unquote(challenge['name'])
                name_with_dash = name_decoded.lower().replace(" ", "-")
                readme_file.write(f"- {name_decoded} - Solves: {challenge['solves']}\n")

    with open(os.path.join(str(year), 'README.md'), 'w') as year_readme_file:
        year_readme_file.write("# Challenge Writeup\n\n")

        for category, challenges in categories.items():
            year_readme_file.write(f"## {category.capitalize()} Challenges\n\n")

            for challenge in challenges:
                name_decoded = unquote(challenge['name'])
                name_with_dash = name_decoded.lower().replace(" ", "-")
                year_readme_file.write(f"- **{name_decoded}** ({challenge['value']} points) - Solved: {'✔' if challenge['solved_by_me'] else '❌'} - Solves: {challenge['solves']}\n\n")


def main():
    data = load_data('data.json')
    year = datetime.now().year
    generate_writeup(data, year)

    print("Writeup directory structure created successfully.")

if __name__ == "__main__":
    main()
