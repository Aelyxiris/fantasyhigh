from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import numpy as np
from textwrap import dedent

KEY = {"STR": "Strength", "DEX": "Dexterity", "CON": "Constitution",
       "INT": "Intelligence", "WIS": "Wisdom", "CHA": "Charisma"}


def mk(text=""):
    """ Formats text into markdown quote style.

    Args:
        text (str): The text to format. Defaults to an empty string.
    Returns:
        str: The formatted text in markdown quote style.
    """
    return f"> {text}\n"


def get_soup(url):
    """ Retrieves the BS4 content from a D&D Beyond character or monster sheet URL/file.

    Args:
        url (str): The URL of the D&D Beyond character or monster sheet, or a local HTML file.
    Returns:
        tuple : A tuple containing the BeautifulSoup object, the name of the character/monster,
               and the type of scrape ('character' or 'monster').
    
    Notes: Autodetects file or URL, and whether it's a character or monster sheet.
    """
    if url.startswith("https://www.dndbeyond.com/"):
        if 'characters' in url.split('/'):
            scrape = 'character'
        elif 'monsters' in url.split('/'):
            scrape = 'monster'
        else:
            raise ValueError("The URL does not point to a character or monster sheet.")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            page.wait_for_load_state("networkidle")  # Wait for JS to finish

            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')

            browser.close()

    elif url.endswith('.html'):
        try:
            with open(url, 'r') as file:
                html = file.read()
                src = html.split('<!--')[1]
            soup = BeautifulSoup(html, 'html.parser')
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{url}' does not exist.")
        except Exception as e:
            raise Exception(f"An error occurred while reading the file: {e}")
        
        # Determine if it's a character or monster sheet based on the content
        if 'characters' in src.split('/'):
            scrape = 'character'
        elif 'monsters' in src.split('/'):
            scrape = 'monster'
        else:
            raise ValueError("The file does not point to a character or monster sheet.")
        
    else:
        raise ValueError("Invalid URL. Please provide a valid character/monster URL or file.")
    
    if scrape == 'character':
        name = soup.title.string.split("'")[0].strip()
    else:
        name = soup.title.get_text().split('-')[0].strip()

    return soup, name, scrape


def scrape_character(soup, name):
    """ Scrapes D&D Beyond character sheets and formats the data into markdown.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the character sheet HTML.
        name (str): The name of the character.
    Returns:
        str: The formatted character sheet in markdown.
    """

    # Scrape table info

    labels = [a.get_text().upper()
              for a in soup.find_all('span', class_="ddbc-ability-summary__abbr")]
    signs = [a.get_text()
             for a in soup.find_all(
                 'span',
                 class_="styles_sign__NdR6X styles_largeSign__V9-jS styles_labelSignColor__Klmbs")]
    
    bonus = [a.find_all('span')[1].get_text()
             for a in soup.find_all('span',
                                    class_="styles_numberDisplay__Rg1za" +
                                    " styles_signed__scf97 styles_large__3C8uq")]
    
    bonus = [i[0] + i[1] for i in zip(signs, bonus)][:-2]
    base = [a.get_text() for a in soup.find_all('div', class_="ddbc-ability-summary__secondary")]

    # Scrape skills

    bard = 'Bard' in soup.find('span', class_="ddbc-character-summary__classes").get_text().split()

    skill_names = [a.get_text().strip()
                   for a in soup.find_all('div', class_="ct-skills__col--skill")[1:]]
    skill_names = [''.join([i.strip() + ' ' for i in s.splitlines()]).strip() for s in skill_names]
    stat = [a.get_text().strip() for a in soup.find_all('div', class_="ct-skills__col--stat")[1:]]
    stat = [''.join([i.strip() + ' ' for i in s.splitlines()]).strip() for s in stat]
    nums = ["+" + a.find('span', attrs={"class": False}).get_text()
            for a in soup.find_all('div', class_="ct-skills__col--modifier")[1:]]
    prof = [a.find('span', attrs={"aria-label": True}).get('aria-label')
            for a in soup.find_all('div', class_="ct-skills__col--proficiency")[1:]]
    if bard:
        mask = [a == 'Proficient' or a == 'Expert' for a in prof]
        half = " and half-proficient in all other skills" if 'Half Proficient' in prof else ""
    else:
        mask = [not (a == 'Not Proficient') for a in prof]
        half = ""

    skill_names = np.array(skill_names)[mask].tolist()
    stat = [KEY[s] for s in np.array(stat)[mask].tolist()]
    nums = np.array(nums)[mask].tolist()
    skills = [f"{skill} {num}" for skill, stat, num in zip(skill_names, stat, nums)]

    armor_class = soup.find('div', attrs={"data-testid": "armor-class-value"}).get_text()
    
    speed = soup.find_all(
        'span',
        class_="styles_numberDisplay__Rg1za styles_largeDistance__YVw96 styles_large__3C8uq"
    )[0].find('span').get_text() + 'ft'

    hp = soup.find('span', attrs={"data-testid": "max-hp"}).get_text()

    # Build the markdown output

    result = "### " + name + "\n\n"

    result += mk(f"**Armor Class:** {armor_class}")
    result += mk()
    result += mk(f"**Hit Points:** {hp}")
    result += mk()
    result += mk(f"**Speed:** {speed}")
    result += mk()
    table = f"""
    > | {labels[0]}  | {labels[1]}  | {labels[2]}  | {labels[3]}  | {labels[4]}  | {labels[5]}  |
    > |------|------|------|------|------|------|
    > | {base[0]}    | {base[1]}   | {base[2]}   | {base[3]}   | {base[4]}   | {base[5]}    |
    > | ({bonus[0]}) | ({bonus[1]}) | ({bonus[2]}) | ({bonus[3]}) | ({bonus[4]}) | ({bonus[5]}) |
    """[1:]
    result += dedent(table)
    result += mk()
    result += mk(f"**Skills:** {', '.join(skills)}" + half)

    return result


def scrape_monster(soup, name):
    """Scrapes D&D Beyond monster sheets and formats the data into markdown.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the monster sheet HTML.
        name (str): The name of the monster.
    Returns:
        str: The formatted monster sheet in markdown.
    """

    misc = [a.get_text().strip('\n ')
            for a in soup.find_all('span',
                                   class_='mon-stat-block-2024__attribute-data-value')]

    ac, init, hp, speed = misc

    hproll = soup.find('span',
                       class_='mon-stat-block-2024__attribute-data-extra').get_text().strip('\n ')

    hp += ' ' + hproll

    tables = soup.find_all('table')

    def get_table_data(tables):
        data = []
        for table in tables:
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                lb = row.find('th').get_text()
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([lb] + [ele for ele in cols if ele])
        return [['', '', 'MOD', 'SAVE']] + data

    more = soup.find_all('div', class_='mon-stat-block-2024__tidbit')
    more = [a.find('span', class_='mon-stat-block-2024__tidbit-data').get_text().strip('\n ')
            for a in more]

    skills, senses, languages, cr = more

    # Build the markdown output

    result = "### " + name + "\n\n"

    result += mk(f"**Armor Class:** {ac}")
    result += mk()
    result += mk(f"**Initiative:** {init}")
    result += mk()
    result += mk(f"**Hit Points:** {hp}")
    result += mk()
    result += mk(f"**Speed:** {speed}")
    result += mk()
    table = get_table_data(tables)
    for row in table:
        rowstring = '| ' + ' | '.join(row) + ' |'
        result += mk(rowstring)
        if row == table[0]:
            result += mk('|---|---|---|---|')
    result += mk()
    result += mk(f"**Skills:** {skills}")
    result += mk()
    result += mk(f"**Senses:** {senses}")
    result += mk()
    result += mk(f"**Languages:** {languages}")
    result += mk()
    result += mk(f"**Challenge Rating:** {cr}")

    return result


if __name__ == "__main__":
    url = input("Enter the URL or filename of the D&D Beyond sheet: ").strip()

    soup, name, type = get_soup(url)

    if type == 'character':
        result = scrape_character(soup, name)
    elif type == 'monster':
        result = scrape_monster(soup, name)

    print(result)
