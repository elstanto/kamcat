import pymupdf
import os
import sys
import csv
from progress.bar import Bar

def get_files() -> tuple[str, str]:
    """
    Check local directory for single pdf and csv file, return filenames
    """
    pdf_files = [f for f in os.listdir('.') if os.path.isfile(f) and '.pdf' in f]
    csv_files = [f for f in os.listdir('.') if os.path.isfile(f) and '.csv' in f]
    if len(pdf_files) != 1 or len(csv_files) != 1:
        print("Must have only one PDF and one CSV file in this folder!")
        input("Press enter to quit...")
        sys.exit(1)
    return (pdf_files[0], csv_files[0])

def process_catalogue(pdf, csv_file):
    products = csv.DictReader(csv_file)
    default_fontsize = 8
    default_x = 0
    default_y = 0
    try:
        defaults = next(products)
        default_fontsize = defaults['Font Size']
        default_x = defaults['X Offset']
        default_y = defaults['Y Offset']
    except:
        print("Can't find defaults in csv! Please use template.")
        input("Press enter to quit...")
    products = list(products)

    with Bar('Processing', max=pdf.page_count) as bar:
        for page in pdf:
            textpage = page.get_textpage()
            for product in products:
                font_size = default_fontsize
                x = default_x
                y = default_y
                if product['Font Size'] != "":
                    font_size = product['Font Size']
                if product['X Offset'] != "":
                    x = product['X Offset']
                if product['Y Offset'] != "":
                    y = product['Y Offset']
                product_instances = page.search_for(product['Code'], textpage=textpage)
                if product_instances != None:
                    for product_instance in product_instances:
                        page.insert_text(
                            [product_instance.x0 + float(x), product_instance.y0 + float(y)],
                            text="£{:,.2f}".format(float(product['Price'])),
                            fontsize=float(font_size),
                            color=(0.8,0,0)
                        )
            bar.next()

def main():
    print("Kam Catalogue Pricer, Version 1.0, August 2024")
    print("Any questions to laurence@stant.phd")
    print("Loading files..")
    pdf_path, csv_path = get_files()
    pdf = pymupdf.open(pdf_path)
    print("Processing catalogue..")
    with open(csv_path) as csv_file:
        process_catalogue(pdf, csv_file)
    print("Saving catalogue...")
    pdf.save("priced_" + pdf_path)
    input("Press enter to quit...")

if __name__ == "__main__":
    main()
