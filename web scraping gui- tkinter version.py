import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import re
from tkinter import *
from tkinter import ttk
def webscrape():
    #opens the search page
    page = requests.get("https://google.com/search?q=" + str(search.get()), headers={'User-Agent': 'Mozilla/5.0'})
    #retrieves data from page
    data = page.text
    #converts data into useable form
    soup = bs(data, "html.parser")
    
    ls= [] #this is used to pre record all the links
    for link in soup.find_all('a'):
        ls.append(link.get("href"))
        #algorithm to get all links
    return(ls)

def get_info(links_list):
    links=[]
        
    for i in range(0, len(links_list)):
        searchable = re.findall(".*?/url.*?", links_list[i], re.IGNORECASE)
        if searchable != []:
            new = links_list[i].replace("/url?q=", "")
            new_link = re.sub("&sa.*", "", new)
            links.append(new_link)
            #gets all useable links
            

        keys = input("What are the keywords you wish to use to fine tune the information? Separate them with a comma and a space. ")
        keywords = keys.split(", ")
        #the above 2 commands get all keywords used to fine-tune search

        k = 0
        alr_printed = []
        used_keywords = []
        i = 0
        used_links = []

        while i < len(links):
            linky = links[i]
            used_links.append(linky)
            #the below 3 lines of code open the webpage
            new_page = requests.get(linky)
            new_data = new_page.text
            new_soup = bs(new_data, "html.parser")
            

            
            #stores curent keyword
            keyword = str(keywords[k])
            
            to_be_printed = []
            
            #finds all paragraph tags
            content = new_soup.find_all('p')

            #splits content to use single list element per paragraph
            split_content = []
            for i in range(0, len(content)):
                splitt = str(content[i]).split("\n")
                split_content.append(str(splitt))
                
            #stores information to be used
            info_2_b_used = []
            
            length = len(split_content)
        
        for s in range(0, len(split_content)):
            is_found = re.findall(keyword, str(split_content[s]), re.IGNORECASE)
            if len(is_found) != 0:
                info_2_b_used.append(split_content[s])
            
        for i in range(0, len(info_2_b_used)):
            info = str(info_2_b_used[i])
            new_info = info.replace("['", "")
            new_info = new_info.replace("]'", "")
            new_info = re.sub("<[^<]+?>", "", info)
            if new_info not in alr_printed:
                print(new_info + "link:  " + str(linky))
                alr_printed.append(new_info)
        
        if len(links) == len(used_links):
            links.clear()
            k = k + 1
            i = 0
        else:
            i = i + 1
            continue

def focus_window_2():
    root.iconify()
    window_2.deiconify()
    window_3.iconify()
    window_4.iconify()
    webscrape()
    get_info(ls)
    
def focus_window_3():
    root.iconify()
    window_2.iconify()
    window_3.deiconify()
    window_4.iconify()
    
def focus_window_4():
    root.iconify()
    window_2.iconify()
    window_3.iconify()
    window_4.deiconify()
    
root = Tk()
root.title("Web Scraper")

welcome_message = ttk.Label(root, text='Welcome to web scraper').grid(column=2, row=1, padx=5, pady=5)

search_message = ttk.Label(root, text='Search Query').grid(column=1, row=2, padx=5, pady=5)
search = StringVar()

search_entry = ttk.Entry(root, textvariable=search).grid(column=2, row=2, padx=5, pady=5)






keywords_message = ttk.Label(root, text='Keywords to use').grid(column=1, row=3, padx=5, pady=5)
keywords = StringVar()

keywords_entry = ttk.Entry(root, textvariable=keywords).grid(column=2, row=3, padx=5, pady=5)
search_button = ttk.Button(root, text='Enter', command=focus_window_2).grid(column=3, row=3, padx=5, pady=5)

help_button = ttk.Button(root, text='Help').grid(column=1, row=4, padx=5, pady=5)





window_2 = Toplevel()
window_2.iconify()
results_text = ttk.Label(window_2, text='Results per page:').grid(column=1, row=1, padx=5, pady=5)

results_num = ttk.Scale(window_2, orient=HORIZONTAL, length=200, from_=1.0, to=100.0).grid(column=2, row=1, padx=5, pady=5)

chosen_key_text = ttk.Label(window_2, text='Chosen keyword:').grid(column=2, row=2, padx=5, pady=5)
chosen_key = StringVar()
chosen_key_box = ttk.Combobox(window_2, textvariable=chosen_key, values=('Val1'), state='readonly').grid(column=3, row=2, padx=5, pady=5)

enter_button = ttk.Button(window_2, text='Enter', command=focus_window_3).grid(column=4, row=2, padx=5, pady=5)

set_same = ttk.Button(window_2, text='Set same value for all').grid(column=3, row=3, padx=5, pady=5)

help_button_2 = ttk.Button(window_2, text='Help').grid(column=1, row=4, padx=5, pady=5)

window_3 = Toplevel()
window_3.iconify()

tick_box_text = ttk.Label(window_3, text='Tick box to select text').grid(column=1, row=1, padx=5, pady=5)
curr_keyword_text = ttk.Label(window_3, text='Current keyword: ',).grid(column=1, row=2, padx=5, pady=5)
curr_keyword = StringVar()
curr_keyword_box = ttk.Combobox(window_3, textvariable=curr_keyword, values=('keyword'), state='readonly').grid(column=1, row=2, padx=5, pady=5)

text_list = ['text1', 'text2', 'text3']
text_list_var = StringVar(value=text_list)
text_listbox = Listbox(window_3, listvariable=text_list_var, selectmode='multiple').grid(column=1, row=3, padx=5, pady=5)

more_results = ttk.Button(window_3, text='More results').grid(column=1, row=4, padx=5, pady=5)

submit_keyword = ttk.Button(window_3, text='Submit this keyword').grid(column=2, row=4, padx=5, pady=5)
unsubmit_keyword = ttk.Button(window_3, text='Unsubmit this keyword').grid(column=2, row=4, padx=5, pady=5)
submit_all = ttk.Button(window_3, text='Submit all', command=focus_window_4).grid(column=3, row=4, padx=5, pady=5)

results_displayed = ttk.Label(window_3, text='[Dispayed num] of [total num] results shown').grid(column=1, row=5, padx=5, pady=5)

help_button_3 = ttk.Button(window_3, text='Help').grid(column=1, row=6, padx=5, pady=5)

window_4 = Toplevel()
window_4.iconify()

all_selected = ttk.Label(window_4, text='All selcted text: ').grid(row=1, padx=5, pady=5)
selected_text = Text(window_4, width=20, height=20, state='disabled').grid(row=2, padx=5, pady=5)
copy_button = ttk.Button(window_4, text='Copy to clipboard',).grid(row=3, padx=5, pady=5)
back_button = ttk.Button(window_4, text='Go back').grid(row=4, padx=5, pady=5)
done_button = ttk.Button(window_4, text='Done').grid(row=5, padx=5, pady=5)
help_button = ttk.Button(window_4, text='Help').grid(row=6, padx=5, pady=5)
root.mainloop()