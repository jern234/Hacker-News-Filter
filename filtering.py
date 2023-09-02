import requests
import webbrowser
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import simpledialog, messagebox

# Solicita datos a la API Hacker News hasta el número de páginas indicado


def requests_from_pages(num_pages):

    All_links = []
    All_subtext = []

    for i in range(num_pages):

        res = requests.get('https://news.ycombinator.com/news?p='+str(i+1))
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.titleline > a')
        subtext = soup.select('.subtext')

        All_links = All_links+links
        All_subtext = All_subtext+subtext
    return [All_links, All_subtext]

# Ordena en base a los votos


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

# Extrae el título, el link y los votos, y filtra en base a los votos mínimos de interés >200


def create_custom_hn(links, subtext,min_votes):

    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points >= min_votes:
                hn.append({'title': title, 'link': href, 'votes': points})

    return sort_stories_by_votes(hn)

# Función que convierte la lista de diccionarios en una cadena de texto formateada


def get_text_from_list(data_list):

    text = ""
    for dicti in data_list:
        text += f"Title: {dicti['title']} Votes: {dicti['votes']}\nLink: {dicti['link']}\n\n"
    return text

# Función que maneja la obtención y procesamiento del input del usuario


def get_user_input():
    user_input = base_input.get()
    votes_input_value = votes_input.get()

    try:
        user_input = int(user_input)
        votes_input_value=int(votes_input_value)

        if user_input > 0:
            dummy_list = requests_from_pages(user_input)
            text = get_text_from_list(
                create_custom_hn(dummy_list[0], dummy_list[1],votes_input_value))
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, text)
            result_text.config(state=tk.DISABLED)

        else:
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(
                tk.END, "Ingrese un valor numérico válido para el número de páginas.")
            result_text.config(state=tk.DISABLED)
    except ValueError:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(
            tk.END, "Ingrese un valor numérico válido para el número de páginas.")
        result_text.config(state=tk.DISABLED)

# Función que maneja el cierre de la ventana


def close_window():
    if messagebox.askokcancel("Salir", "¿Seguro que quieres salir?"):
        root.destroy()


# Crea la ventana principal de interacción
root = tk.Tk()
root.title("Hacker News Filter")
root.geometry("800x600")


# Etiqueta para el mínimo de votos
votes_label = tk.Label(root, text="Mínimo de Votos", font=("Helvetica", 13, "bold"))
votes_label.pack(pady=10)

# Cuadro de entrada para el mínimo de votos
votes_input = tk.Entry(root, width=30, font=("Helvetica", 12))
votes_input.pack(pady=5)


# Etiqueta para el título del input
input_label = tk.Label(
    root, text="Páginas de la 1-?", font=("Helvetica", 13, "bold"))
input_label.pack(pady=10)

#Cuadro de entrada
base_input = tk.Entry(root, width=30, font=("Helvetica", 12))
base_input.pack(pady=5)

get_input_button = tk.Button(
    root, text="Listo", command=get_user_input, font=("Helvetica", 12))
get_input_button.pack()

#Results
results_label = tk.Label(root, text="Resultados desde el más votado al menos votado", font=("Helvetica", 13, "bold"))
results_label.pack(pady=10)

result_text = tk.Text(root, wrap=tk.WORD,
                      state=tk.DISABLED, font=("Helvetica", 12))
result_text.pack(fill=tk.BOTH, expand=True)
result_text.configure(bg="lightgray", fg="black")



# Crear barras de desplazamiento
vertical_scrollbar = tk.Scrollbar(root, command=result_text.yview)
result_text.config(yscrollcommand=vertical_scrollbar.set)
vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")

horizontal_scrollbar = tk.Scrollbar(
    root, command=result_text.xview, orient=tk.HORIZONTAL)
horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
result_text.config(xscrollcommand=horizontal_scrollbar.set)

root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()
