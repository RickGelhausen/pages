"""
Transform a BibTeX file into a single YAML file containing all bibtex entries
"""
import re
import os
import argparse
import bibtexparser
import yaml

# Dictionary to replace author names with aliases for the data column (does not affect the displayed author names)
ALIAS_DICT = {"S. Lange"              : "Sita J. Saunders",
              "S. J. Lange"           : "Sita J. Saunders",
              "S. J. Saunders"        : "Sita J. Saunders",
              "Sita J. Lange"         : "Sita J. Saunders",
              "R. Backofen"           : "Rolf Backofen",
              "Martin Mann"           : "Martin Raden",
              "M. Mann"               : "Martin Raden",
              "Bjorn Gruning"         : "Björn Grüning",
              "Bjorn Grüning"         : "Björn Grüning",
              "Björn Gruning"         : "Björn Grüning",
              "Bjoern Gruening"       : "Björn Grüning",
              "Björn A. Grüning"      : "Björn Grüning",
              "Björn A Grüning"       : "Björn Grüning",
              "Björn Andreas Grüning" : "Björn Grüning",
              "Berenice Batut"        : "Bérénice Batut",
              "Tran Van Dinh"         : "Van Dinh Tran",
              "Dinh Van Tran"         : "Van Dinh Tran",
              "Dinh V Tran"           : "Van Dinh Tran",
              "Omer Alkhnbashi"       : "Omer S. Alkhnbashi",
              "Omer S Alkhnbashi"     : "Omer S. Alkhnbashi"}

TYPE_DICT = {"article"              : "Article",
             "inproceedings"        : "Conference",
             "proceedings"          : "Conference",
             "conference"           : "Conference",
             "incollection"         : "Book",
             "inbook"               : "Book",
             "book"                 : "Book",
             "booklet"              : "Book",
             "PhDThesis"            : "PhD Thesis",
             "mastersthesis"        : "Master's Thesis",
             "default"              : "Other"}

def format_authors(authors):
    """
    Format the authors string for YAML output
    """
    authors = authors.replace("\n", " ")
    authors = re.sub(r'\s+', ' ', authors)

    author_list = authors.split(' and ')
    authors_list = []
    for author in author_list:
        parts = [part.strip() for part in author.split(',')]
        last_name = parts[0]
        first_name = " ".join(parts[1:])  # first name includes all parts except the last
        full_name = f'{first_name} {last_name}'.strip()
        full_name = ALIAS_DICT.get(full_name, full_name)
        authors_list.append(full_name)

    return authors_list

def format_title(title):
    """
    Format the title string for YAML output
    """
    title = re.sub(r'\{(.+?)\}', r'\1', title)  # Remove braces
    title = re.sub(r'\s+', ' ', title).strip()    # Normalize spaces
    return title

def create_yaml_file(bib_entries, output_file):
    """
    Build a single YAML file from the list of BibTeX entries
    """
    yaml_data = []

    for entry in bib_entries:
        bibid = entry.get('ID', '')
        authors = format_authors(entry.get('author', ''))
        journal = entry.get('journal', '') or format_title(entry.get('booktitle', '').replace("\n", " "))
        year = entry.get('year', '')
        title = format_title(entry.get('title', '').replace("\n", " "))
        link = entry.get('doi', entry.get('url', ''))
        href = f"https://doi.org/{link}" if not link.startswith(('http', 'www')) else link
        entry_type = TYPE_DICT.get(entry.get('ENTRYTYPE', ''), TYPE_DICT['default'])
        pdf_href = entry.get('pdf', '')
        abstract = entry.get('abstract', '').replace("\n", " ").strip() if 'abstract' in entry else ''

        yaml_data.append({
            'id': bibid,
            'title': title,
            'authors': authors,
            'journal': journal,
            'year': int(year),
            'type': entry_type,
            'doi': href,
            'pdf': pdf_href,
            'abstract': abstract
        })

    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, 'w', encoding="utf-8") as yaml_file:
        for entry in yaml_data:
            yaml.dump([entry], yaml_file, allow_unicode=True, sort_keys=False)
            yaml_file.write('\n')

def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(description='Convert a .bib file into a single YAML file')
    parser.add_argument('-i', '--input', help='The .bib file to parse', required=True)
    parser.add_argument('-o', '--output', help='The output YAML file name', required=True)

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as bibtex_file:
        bibtex_str = bibtex_file.read()

    bib_database = bibtexparser.loads(bibtex_str)
    create_yaml_file(bib_database.entries, args.output)

if __name__ == '__main__':
    main()
