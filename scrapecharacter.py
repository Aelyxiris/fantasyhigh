from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import numpy as np

url = input("Enter the URL of the D&D Beyond character sheet: ").strip()
if not url.startswith("https://www.dndbeyond.com/characters/"):
    raise ValueError("Invalid URL. Please provide a valid D&D Beyond character sheet URL.")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_load_state("networkidle")  # Wait for JS to finish

    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')

    browser.close()

key = {"STR": "Strength", "DEX": "Dexterity", "CON": "Constitution",
         "INT": "Intelligence", "WIS": "Wisdom", "CHA": "Charisma"}

# Scrape table info

labels = [a.get_text().upper() for a in soup.find_all('span', class_="ddbc-ability-summary__abbr")]
signs = [a.get_text() for a in soup.find_all('span', class_="styles_sign__NdR6X styles_largeSign__V9-jS styles_labelSignColor__Klmbs")]
bonuses = [a.find_all('span')[1].get_text() for a in soup.find_all('span', class_="styles_numberDisplay__Rg1za styles_signed__scf97 styles_large__3C8uq")]
bonuses = [i[0] + i[1] for i in zip(signs, bonuses)][:-2]
base = [a.get_text() for a in soup.find_all('div', class_="ddbc-ability-summary__secondary")]

# Scrape skills

skill_names = [a.get_text().strip() for a in soup.find_all('div', class_="ct-skills__col--skill")[1:]]
skill_names = [''.join([i.strip() + ' ' for i in s.splitlines()]).strip() for s in skill_names]
stat = [a.get_text().strip() for a in soup.find_all('div', class_="ct-skills__col--stat")[1:]]
stat = [''.join([i.strip() + ' ' for i in s.splitlines()]).strip() for s in stat]
nums = ["+" + a.find('span', attrs={"class": False}).get_text() for a in soup.find_all('div', class_="ct-skills__col--modifier")[1:]]
prof = [a.find('span', attrs={"aria-label": True}).get('aria-label') == 'Proficient' for a in soup.find_all('div', class_="ct-skills__col--proficiency")[1:]]
skill_names = np.array(skill_names)[prof].tolist()
stat = [key[s] for s in np.array(stat)[prof].tolist()]
nums = np.array(nums)[prof].tolist()
skills = [f"{skill} {num}" for skill, stat, num in zip(skill_names, stat, nums)]

armor_class = soup.find('div', attrs={"data-testid": "armor-class-value"}).get_text()
speed = soup.find_all('span', class_="styles_numberDisplay__Rg1za styles_largeDistance__YVw96 styles_large__3C8uq")[0].find('span').get_text() + 'ft'
hp = soup.find('span', attrs={"data-testid": "max-hp"}).get_text()
name = soup.title.string.split("'")[0].strip()

result = "### " + name + "\n\n"
def add(text=""):
    global result
    result += f"> {text}\n"

add(f"**Armor Class:** {armor_class}")
add()
add(f"**Hit Points:** {hp}")
add()
add(f"**Speed:** {speed}")
add()
table = f"""
> | {labels[0]}  | {labels[1]}  | {labels[2]}  | {labels[3]}  | {labels[4]}  | {labels[5]}  |
> |------|------|------|------|------|------|
> | {base[0]}    | {base[1]}   | {base[2]}   | {base[3]}   | {base[4]}   | {base[5]}    |
> | ({bonuses[0]}) | ({bonuses[1]}) | ({bonuses[2]}) | ({bonuses[3]}) | ({bonuses[4]}) | ({bonuses[5]}) |
"""[1:]
result += table
add()
add(f"**Skills:** {', '.join(skills)}")

print(result)