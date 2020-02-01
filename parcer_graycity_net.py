import requests
from bs4 import BeautifulSoup
import re
# from docx import Document
import time

# Получаем html страницу
def get_html(url):
    try:
        r = requests.get(url)    # Получаем метод Response
        r.encoding = 'utf8'      # У меня были проблемы с кодировкой, я задал в ручную
        return r.text            # Вернем данные объекта text
    except Exception:
        print ('Соеденение разорвано. Пытаемся соедениться снова.') 
        # sleep for a bit in case that helps
        time.sleep(1)
        # try again
        return get_html(url)

# Получаем текст книги со страницы
def get_textToRead(html):
    soup = BeautifulSoup(html, "html.parser")
    textToRead = soup.find('div', id='textToRead') 
    return textToRead

# Получаем ссылки на остальные страницы книги
def get_pages(html):
    soup = BeautifulSoup(html, "html.parser")        
    productDivs = soup.find('div', attrs={'class' : 'splitnewsnavigation2 ignore-select'})    
    url_pages_list = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(productDivs))  
    return url_pages_list

# Обрабатываем текст
def convet_Text(text_with_tags):
    # Удаляем лишние теги
    invalid_tags = ['div', 'script', 'a', 'img', 'center']
    for tag in invalid_tags: 
        for match in text_with_tags.findAll(tag):
            match.replaceWithChildren() 
    
    text_with_multiple_spaces = text_with_tags.get_text("\n") # Разделяем текст на абзатцы
    
    text_with_multiple_spaces  = re.sub(' +', ' ', text_with_multiple_spaces ) # Удаляем лишние пробелы
    
    text_lines = text_with_multiple_spaces.splitlines(keepends = True)
    
    text = ''
    for line in text_lines:
        line = line.replace("\t", "")     
        if line!='\n' and line!=' \n' and line!='   \n' and line!='   \n':
            text = text + line 
    return text        
    

#Получаем ссылки, текст, обрабатываем их
def get_textFromURL(url_adress):
    print ('Обрабатываем страницу: ' + url_adress)
    html = get_html(url_adress)    
    text_with_tags = get_textToRead(html)
    text = convet_Text(text_with_tags)
    url_pages_list = get_pages(html)
    for url in url_pages_list:
        print ('Обрабатываем страницу: ' + url) 
        html = get_html(url)
        text_with_tags = get_textToRead(html)
        text = text + convet_Text(text_with_tags)            
    return text
    
url = 'https://graycity.net/vasily-mahanenko/509302-a_song_of_shadow.html' #Указываем корневой адрес книги
file_name_with_html = url.split('/')[-1]
l = file_name_with_html.find('.')
file_name = file_name_with_html[:l]
text =  get_textFromURL(url)
output = open(file_name + '.txt', 'w', encoding='utf-8')
output.write (text)
output.close()
       
# document = Document()
# document.add_paragraph(text)
# document.save(file_name + '.docx')