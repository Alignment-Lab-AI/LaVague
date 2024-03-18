import gradio as gr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By # import used by generated selenium code
from selenium.webdriver.common.keys import Keys # import used by generated selenium code
from .action_engine import ActionEngine
import re

class CommandCenter:
    title = """
    <div align="center">
    <h1>🌊 Welcome to LaVague</h1>
    <p>Redefining internet surfing by transforming natural language instructions into seamless browser interactions.</p>
    </div>
    """

    def __init__(
        self,
        actionEngine=ActionEngine(),
        chromePath=None,
        chromedriverPath=None,
    ):
        self.actionEngine = actionEngine

        ## Setup chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1600,900") # Size of screenshots
        if chromePath is not None:
            chrome_options.binary_location = chromePath
        if chromedriverPath is not None:
            webdriver_service = Service(chromedriverPath)
        self.driver = webdriver.Chrome(
            service=webdriver_service, options=chrome_options
        )

    def __process_url(self):
        def process_url(url):
            self.driver.get(url)
            self.driver.save_screenshot("screenshot.png")
            # This function is supposed to fetch and return the image from the URL.
            # Placeholder function: replace with actual image fetching logic.
            return "screenshot.png"
        return process_url

    def __process_instruction(self, max_tokens):
        def process_instructions(query, url_input):
            if url_input != self.driver.current_url:
                self.driver.get(url_input)
            state = self.driver.page_source
            query_engine = self.actionEngine.get_query_engine(state)
            streaming_response = query_engine.query(query)

            source_nodes = streaming_response.get_formatted_sources(max_tokens)

            response = ""

            for text in streaming_response.response_gen:
                # do something with text as they arrive.
                response += text
                yield response, source_nodes
        return process_instructions

    def __extract_first_python_code(self, markdown_text):
        # Pattern to match the first ```python ``` code block
        pattern = r"```python(.*?)```"

        # Using re.DOTALL to make '.' match also newlines
        match = re.search(pattern, markdown_text, re.DOTALL)
        if match:
            # Return the first matched group, which is the code inside the ```python ```
            return match.group(1).strip()
        else:
            # Return None if no match is found
            return None

    def __exec_code(self):
        def exec_code(code, full_code):
            code = self.__extract_first_python_code(code)
            html = self.driver.page_source
            driver = self.driver # define driver for exec
            try:
                exec(code)
                output = "Successful code execution"
                status = """<p style="color: green; font-size: 20px; font-weight: bold;">Success!</p>"""
                full_code += code
            except Exception as e:
                output = f"Error in code execution: {str(e)}"
                status = """<p style="color: red; font-size: 20px; font-weight: bold;">Failure! Open the Debug tab for more information</p>"""
            return output, code, html, status, full_code
        return exec_code

    def __update_image_display(self):
        def update_image_display():
            self.driver.save_screenshot("screenshot.png")
            url = self.driver.current_url
            return "screenshot.png", url
        return update_image_display

    def __show_processing_message(self):
        return lambda: "Processing..."

    def run(self, base_url, instructions, max_tokens=1500):
        with gr.Blocks() as demo:
            with gr.Tab("LaVague"):
                with gr.Row():
                    gr.HTML(self.title)
                with gr.Row():
                    url_input = gr.Textbox(
                        value=base_url,
                        label="Enter URL and press 'Enter' to load the page.",
                    )

                with gr.Row():
                    with gr.Column(scale=7):
                        image_display = gr.Image(label="Browser", interactive=False)

                    with gr.Column(scale=3):
                        with gr.Accordion(label="Full code", open=False):
                            full_code = gr.Code(
                                value="", language="python", interactive=False
                            )
                        code_display = gr.Code(
                            label="Generated code",
                            language="python",
                            lines=5,
                            interactive=True,
                        )

                        status_html = gr.HTML()
                with gr.Row():
                    with gr.Column(scale=8):
                        text_area = gr.Textbox(
                            label="Enter instructions and press 'Enter' to generate code."
                        )
                        gr.Examples(examples=instructions, inputs=text_area)
            with gr.Tab("Debug"):
                with gr.Row():
                    with gr.Column():
                        log_display = gr.Textbox(interactive=False, lines=20)
                    with gr.Column():
                        source_display = gr.Code(
                            language="html",
                            label="Retrieved nodes",
                            interactive=False,
                            lines=20,
                        )
                with gr.Row():
                    with gr.Accordion(label="Full HTML", open=False):
                        full_html = gr.Code(
                            language="html",
                            label="Full HTML",
                            interactive=False,
                            lines=20,
                        )

            # Linking components
            url_input.submit(
                self.__process_url(),
                inputs=[url_input],
                outputs=[image_display],
            )
            text_area.submit(
                self.__show_processing_message(), outputs=[status_html]
            ).then(
                self.__process_instruction(max_tokens),
                inputs=[text_area, url_input],
                outputs=[code_display, source_display],
            ).then(
                self.__exec_code(),
                inputs=[code_display, full_code],
                outputs=[log_display, code_display, full_html, status_html, full_code],
            ).then(
                self.__update_image_display(),
                inputs=[],
                outputs=[image_display, url_input],
            )
        demo.launch(share=True, debug=True)