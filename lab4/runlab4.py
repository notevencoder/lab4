import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import functions

# Функция для обновления графика в зависимости от выбранного значения
def update_graph(event):
    selected_option = combo_box.get()  # Получаем выбранное значение из выпадающего списка
    x = np.linspace(0, 10, 100)
    
    #if selected_option == 'sin(x)':
    #    y = np.sin(x)
    #elif selected_option == 'cos(x)':
    #    y = np.cos(x)
    #else:
    #    y = np.tan(x)
    curr_func = None
    if selected_option == '1':
         curr_func = functions.graph1()
    elif selected_option == '2':
         curr_func = functions.graph2()
    elif selected_option == '3':
        curr_func = functions.graph3()
    elif selected_option == '4':
        curr_func = functions.graph4()
    elif selected_option == '5':
        username = input("username:\n>")
        curr_func = functions.graph5(username)
    elif selected_option == '6':
        curr_func = functions.graph6()
    
      # Создаем новый график
    curr_func.figure(figsize=(6, 4))
    curr_func.title(f'График {selected_option}')
    curr_func.xlabel('x')
    curr_func.ylabel('y')

    

    # Отображаем график через plt.show
    curr_func.show()

# Создаем главное окно
root = tk.Tk()
root.title("Пример с графиком и выпадающим списком")

# Надпись
label = tk.Label(root, text="Выберите функцию для графика:")
label.pack(pady=10)

# Выпадающий список
combo_box = ttk.Combobox(root, values=["1", "2", "3", "4", "5", "6"], state="readonly")
combo_box.pack(pady=10)

# Создаем область для отображения графика
fig, ax = plt.subplots(figsize=(6, 4))
ax.set_title("График функции")
ax.set_xlabel("x")
ax.set_ylabel("y")

# Отображаем график на tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=20)

# Обработчик события выбора в выпадающем списке
combo_box.bind("<<ComboboxSelected>>", update_graph)

# Запускаем приложение
root.mainloop()


#while 1:
#    mode = input("Какую диаграмму строить?\nВыберите: 1,2,3,4,5,6? 0-exit\n>")
#    if mode == '1':
#        functions.graph1()
#    elif mode == '2':
#        functions.graph2()
#    elif mode == '3':
#        functions.graph3()
#    elif mode == '4':
#        functions.graph4()
#    elif mode == '5':
#        username = input("username:\n>")
#        functions.graph5(username)
#    elif mode == '6':
#        functions.graph6()
#    elif mode == '0':
#        exit(0)
