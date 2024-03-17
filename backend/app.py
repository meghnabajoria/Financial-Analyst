from flask import Flask, request, jsonify
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import requests
import google.generativeai as genai
import time

genai.configure(api_key="AIzaSyD2ut1rrUIzbOSFuW7g-0PT6MGIwjcFAXM")
app = Flask(__name__)


# def configure_chrome_options():
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('log-level=3')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--disable-gpu')
#     return chrome_options


# def create_webdriver():
#     return webdriver.Chrome(options=configure_chrome_options())


def get_content(link):
   
    try:
        response = requests.get(link)
        time.sleep(10)

        soup = BeautifulSoup(response.get_content, 'html.parser')
        results = soup.find_all('li', class_='listing__item listing__item--alternate')

        for item in results[:3]:
            link_element = item.find('a', class_='listing__link')
            if link_element:
                link = link_element.get('href')
                print("=============", link)
                context_in_one_list = get_content(link)
                context += ' '.join(context_in_one_list)
            else:
                print("Link not found.")
    except Exception as main_error:
        return f"Error during main processing: {main_error}"

def clean_text(text):
    # Remove special characters like \n and *
    cleaned_text = text.replace('\n', ' ').replace('*', '')
    return cleaned_text

    
@app.route('/ask', methods=['POST'])
def index():
    if request.method == 'POST':
        context = ""
        data = request.get_json()
        question = data.get('question','')
        print(question)

        search_params = {'searchTerm': question}
        url = f'https://www.kiplinger.com/search?{urlencode(search_params)}'
        print(url)

        try:
            response = requests.get(url)
            time.sleep(10)

            soup = BeautifulSoup(response.content, 'html.parser')
            results = soup.find_all('li', class_='listing__item listing__item--alternate')

            for item in results[:3]:
                link_element = item.find('a', class_='listing__link')
                if link_element:
                    link = link_element.get('href')
                    print("=============", link)
                    context_in_one_list = get_content(link)
                    context += ' '.join(context_in_one_list)
                else:
                    print("Link not found.")
        except Exception as main_error:
            return f"Error during main processing: {main_error}"
        
        prompt = f"{question}\n\nContext:\n{context}"
        model = genai.GenerativeModel('gemini-pro')
        result = model.generate_content(prompt)
        answer = clean_text(result.text)
        return jsonify({
            'answer': answer
        })
        # return result.text

if __name__ == '__main__':
    app.run(debug=True)
