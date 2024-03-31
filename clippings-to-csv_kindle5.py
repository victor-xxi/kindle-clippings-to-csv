# csv library used to make the csv file
import csv, os


# rename csv if it already exists
def rename_csv(name: str) -> str:
    while(True):
        counter = 1
        while os.path.exists(f'{name}_{counter:02d}.csv'):
            counter += 1
        return f'{name}_{counter:02d}'

# convert month name to month number
def month_number(m: str) -> int:
    months_dict = {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12
    }
    return months_dict[m]

# translate the day of the week to catalan
def day_week_catalan(d: str) -> str:
    days_week_dict = {
        'lunes': 'dilluns',
        'martes': 'dimarts',
        'miércoles': 'dimecres',
        'jueves': 'dijous',
        'viernes': 'divendres',
        'sábado': 'dissabte',
        'domingo': 'diumenge'
    }
    return days_week_dict[d]

# write time in HH:MM format
def hour_format(h: str) -> str:
    return '%s:%s' % (h[:2], h[3:5])

# write sortable date YYYY-MM-DD-HH-MM
def sortable_date(y: str, m: int, d: str) -> str:
    d = int(d)
    return f'{y}-{m:02d}-{d:02d}'


# disclaimer and instructions
print("\nAvís: aquest programa (de moment) només funciona si tens el kindle en castellà.\n")
print("Introdueix el nom del fitxer")
print("- Exemple: My clippings.txt (important mantenir tant les majúscules i minúscules com el .txt)")
print("- Nota: el fitxer ha de ser a la mateixa carpeta que aquest programa.\n")


# open the file
name = input()
f_in = open(name, "r")
name = name[:len(name)-4]

# rename the csv file
if os.path.exists(f'{name}.csv'):
    name = rename_csv(name)

# create the csv file
f_out = open(f'{name}.csv', 'w', newline='')
sorted_clippings = csv.writer(f_out)
sorted_clippings.writerow(["Autor", "Llibre", "Retall", "Pàgina", "Posició", "Data", "Hora", "Dia de la setmana"])


# loop for each clipping
while True:

# clipping info
    # scan first line of the input file
    book_author = f_in.readline()
    # if there's nothing it means we're finished
    if not book_author:
        break

    # find the separation between book and author
    length = len(book_author)
    for i in range(length-2, 0, -1):
        if book_author[i] == '(':
            break
    # book and author
    book = book_author[:i-1]
    author = book_author[i+1:length-2]

    # scan second line of the input file and split it into words
    page_date_time = f_in.readline().split()
    length = len(page_date_time)
    page = ''
    for i in range(length):
        # page
        if page_date_time[i] == 'página':
            page = page_date_time[i+1]
        # position
        if page_date_time[i] == 'Pos.':
            position = page_date_time[i+1]
        # time
        if page_date_time[i] == 'Añadido':
            day_week = day_week_catalan(page_date_time[i+2])
            day = page_date_time[i+3]
            month = month_number(page_date_time[i+5])
            year = page_date_time[i+7]
            hour = hour_format(page_date_time[i+8])
            date = sortable_date(year, month, day)
    # skip the space
    f_in.readline()

# the actual clipping
    # add lines one by one
    clipping = ""
    while True:
        clip = f_in.readline()
        if clip.strip() == '==========':
            break
        clipping += clip
    # strip removes blank spaces at the end
    clipping = clipping.strip()

# add the clipping to the csv file
    sorted_clippings.writerow([author, book, clipping, page, position, date, hour, day_week])


f_in.close()
f_out.close()
