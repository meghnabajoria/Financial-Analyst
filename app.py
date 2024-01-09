from flask import Flask, request, render_template
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import urlencode
import openai

app = Flask(__name__)

def configure_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return chrome_options

def create_webdriver():
    return webdriver.Chrome(options=configure_chrome_options())

def get_content(link):

    # Ignore SSL errors
    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True

    driver = create_webdriver()

    try:
        driver.get(link)
        time.sleep(10)
        page_source = driver.page_source
        soup2 = BeautifulSoup(page_source, 'html.parser')
        paragraphs = soup2.find_all('p')
        text_content = [p.get_text() for p in paragraphs]

        return text_content

    except Exception as e:
        print(f"Error during content retrieval: {e}")

    finally:
        driver.quit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form['question']
        openai.api_key = request.form['api_key']

        driver = create_webdriver()

        search_params = {'searchTerm': question}
        url = f'https://www.kiplinger.com/search?{urlencode(search_params)}'

        driver.get(url)

        time.sleep(10)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        top_3_content = soup.find_all('li', class_='listing__item listing__item--alternate')
        context = ""
        for item in top_3_content[:2]:
            link_element = item.find('a', class_='listing__link')
            if link_element:
                link = link_element.get('href')
                context_in_one_list = get_content(link)
                context += ' '.join(context_in_one_list)
            else:
                print("Link not found.")
        driver.quit()

        prompt = f"{question}\n\nInput:\n{context}"
        prompt = " ".join(prompt.split()[:3800])

        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200,  # Assuming a maximum context length of 4096 tokens
            n=1,
            stop=None
        )

        result = response.choices[0].text.lstrip()
        return render_template('index.html', result=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
