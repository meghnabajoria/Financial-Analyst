from selenium.webdriver.chrome.options import Options
from flask import Flask, request, render_template
from urllib.parse import urlencode
from selenium import webdriver
from bs4 import BeautifulSoup
import openai
import time

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

    try:
        driver = create_webdriver()
        driver.get(link)
        time.sleep(10)

        page_source = driver.page_source
        soup2 = BeautifulSoup(page_source, 'html.parser')
        paragraphs = soup2.find_all('p')
        text_content = [p.get_text() for p in paragraphs]
        return text_content

    except Exception as e:
        print(f"Error during content retrieval for link '{link}': {e}")
        return []

    finally:
        try:
            driver.quit()
        except Exception as quit_error:
            print(f"Error while quitting the driver: {quit_error}")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        context = ""
        question = request.form['question']
        api_key = request.form['api_key']

        if not question or not api_key:
            return render_template('error.html', message="Invalid request. Please provide both question and API key.")

        openai.api_key = api_key

        search_params = {'searchTerm': question}
        url = f'https://www.kiplinger.com/search?{urlencode(search_params)}'

        try:
            driver = create_webdriver()
            driver.get(url)
            time.sleep(10)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            results = soup.find_all('li', class_='listing__item listing__item--alternate')

            for item in results[:1]:
                link_element = item.find('a', class_='listing__link')
                if link_element:
                    link = link_element.get('href')
                    context_in_one_list = get_content(link)
                    context += ' '.join(context_in_one_list)
                else:
                    print("Link not found.")
        except Exception as main_error:
            return render_template('error.html', message=f"Error during main processing: {main_error}")

        finally:
            try:
                driver.quit()
            except Exception as quit_error:
                print(f"Error while quitting the driver: {quit_error}")

        prompt = f"{question}\n\nInput:\n{context}"
        prompt = " ".join(prompt.split()[:3800])

        try:
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=200,
                n=1,
                stop=None
            )
            result = response.choices[0].text.lstrip()
            return render_template('index.html', result=result)

        except openai.error.OpenAIError as openai_error:
            return render_template('error.html', message=f"OpenAI API Error: {openai_error}")

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
