import pandas as pd

preamble = r"""
\documentclass[12pt,a4paper]{book}
\usepackage[catalan]{babel}

\begin{document}

\tableofcontents
"""

# Specify the file paths
csv_in = 'retalls.csv'
tex_out = open('retalls_maquetats.tex', 'w')

# Read CSV file into a DataFrame
df = pd.read_csv(csv_in)

# Sort the DataFrame based on multiple columns (e.g., 'Column1' and 'Column2')
df_sorted = df.sort_values(by=['Autor', 'Llibre', 'Pàgina', 'Posició', 'Data', 'Hora'])

tex_out.write(preamble)

author, book = '', ''
for i in range(len(df_sorted)):
    # Access elements in a row using .iloc
    row = df.iloc[i]
    
    if row.iloc[0] != author:
        author = row.iloc[0]
        tex_out.write(f"\n\n\\chapter{{{author}}}\n")

    if row.iloc[1] != book:
        book = row.iloc[1]
        tex_out.write(f"\n\\section{{{book}}}\n\n")

    tex_out.write(f"\\subsubsection*{{{row.iloc[5]}, pàgina {row.iloc[3]}, posició {row.iloc[4]}}}\n")
    tex_out.write(f"\\begin{{quote}}\n\t{row.iloc[2]}\n\\end{{quote}}\n\n")


tex_out.write(f"\\end{{document}}")
