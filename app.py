from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from accelerate import Accelerator
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from urllib.parse import quote

BASE_URL = "https://www.kiplinger.com/"

app = Flask(__name__)

accelerator = Accelerator()

model_name = "databricks/dolly-v2-3b"
model = AutoModelForCausalLM.from_pretrained(model_name)

# Apply torch_dtype and device_map after loading
model = model.to(torch.bfloat16)
model = accelerator.prepare(model, device_maps="auto", offload_folder="D:\\FinancialAnalyst\\offloaded")

# Create the Hugging Face pipeline once
generate_text = pipeline(model=model, device=0)

generate_text = pipeline(model="databricks/dolly-v2-7b", torch_dtype=torch.bfloat16,
                         trust_remote_code=True, device_map="auto", offload_folder="D:\\FinancialAnalyst\\offloaded")
hf_pipeline = HuggingFacePipeline(pipeline=generate_text)
llm_context_chain = LLMChain(llm=hf_pipeline,
                             prompt=PromptTemplate(input_variables=["instruction", "context"],
                                                   template="{instruction}\n\nInput:\n{context}"))


def get_content(link):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(link)
        time.sleep(10)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        paragraphs = soup.find_all('p')
        text_content = [p.get_text() for p in paragraphs]

        return ' '.join(text_content)

    except Exception as e:
        return f"Error during content retrieval: {e}"

    finally:
        driver.quit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    instruction = request.form['instruction']

    url = f"{BASE_URL}?q={quote(instruction)}"

    context = get_content(url)
    limited_context = ' '.join(context)[:500]  # Limit context length

    with accelerator.device():
        result = llm_context_chain.predict(instruction=instruction,
                                           context=limited_context).lstrip()

    return render_template('index.html', url=url, result=result)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
