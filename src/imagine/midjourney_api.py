import json
import time
import http.client
import pprint
import dotenv
import os
import requests

root = os.path.dirname(os.path.abspath(__file__))

dotenv.load_dotenv(os.path.join(root, "..", "..", ".env"))

IMAGINE_API_KEY = os.getenv("IMAGINE_API_KEY")


class ImagineApi(object):
    def __init__(self, disease_name, results_path=None):
        self.disease_name = disease_name
        self.disease_base_name = disease_name.replace(" ", "_").lower()
        if results_path is None:
            results_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "results")
            )
        if not os.path.exists(results_path):
            os.makedirs(results_path)
        disease_results_path = os.path.join(
            results_path, "images", self.disease_base_name
        )
        print(disease_results_path)
        if not os.path.exists(disease_results_path):
            os.makedirs(disease_results_path)
        self.results_path = results_path
        self.disease_results_path = disease_results_path

    def is_already_generated(self, request_name):
        json_file = os.path.join(self.disease_results_path, f"{request_name}.json")
        return os.path.exists(json_file)

    def do_request(self, data):

        headers = {
            "Authorization": f"Bearer {IMAGINE_API_KEY}",
            "Content-Type": "application/json",
        }

        def send_request(method, path, body=None, headers={}):
            conn = http.client.HTTPSConnection("cl.imagineapi.dev")
            conn.request(
                method, path, body=json.dumps(body) if body else None, headers=headers
            )
            response = conn.getresponse()
            data = json.loads(response.read().decode())
            conn.close()
            return data

        prompt_response_data = send_request("POST", "/items/images/", data, headers)
        pprint.pp(prompt_response_data)

        def check_image_status():
            try:
                response_data = send_request(
                    "GET",
                    f"/items/images/{prompt_response_data['data']['id']}",
                    headers=headers,
                )
                if response_data["data"]["status"] in ["completed", "failed"]:
                    print(
                        "Completed image details",
                    )
                    pprint.pp(response_data["data"])
                    return True
                else:
                    print(
                        f"Image is not finished generation. Status: {response_data['data']['status']}"
                    )
                    return False
            except:
                return False

        for _ in range(100):
            is_done = check_image_status()
            if is_done:
                break
            time.sleep(5)

        response_data = send_request(
            "GET",
            f"/items/images/{prompt_response_data['data']['id']}",
            headers=headers,
        )
        return response_data

    def generate_and_save_image_urls(self, request_name, prompt):
        data = {"prompt": prompt}
        response_data = self.do_request(data)
        response_data["request_name"] = request_name
        response_data["disease_name"] = self.disease_base_name
        json_file = os.path.join(self.disease_results_path, f"{request_name}.json")
        with open(json_file, "w") as f:
            json.dump(response_data, f, indent=4)

    def run(self):
        with open(
            os.path.join(
                self.results_path, "prompts", "json", f"{self.disease_base_name}.json"
            )
        ) as f:
            prompts = json.load(f)["midjourney_prompts"]
        for request_name, prompt in prompts.items():
            if self.is_already_generated(request_name):
                continue
            print(request_name, prompt)
            self.generate_and_save_image_urls(request_name, prompt)


class PngFetcher(object):
    def __init__(self, disease_name, results_path=None):
        self.disease_name = disease_name
        self.disease_base_name = disease_name.replace(" ", "_").lower()
        if results_path is None:
            results_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "results")
            )
        images_path = os.path.join(results_path, "images", self.disease_base_name)
        self.results_path = results_path
        self.images_path = images_path
        self.pngs_path = os.path.join(results_path, "pngs", self.disease_base_name)
        if not os.path.exists(self.pngs_path):
            os.makedirs(self.pngs_path)

    def fetch_png(self, url, request_name, image_number):
        png_filename = f"{self.disease_base_name}-{request_name}-{image_number}.png"
        png_file = os.path.join(self.pngs_path, png_filename)
        if os.path.exists(png_file):
            print(f"PNG file already exists: {png_file}")
            return True
        response = requests.get(url)
        if response.status_code == 200:
            with open(png_file, "wb") as f:
                f.write(response.content)
            print(f"PNG file saved: {png_file}")
            return True
        else:
            print(f"Failed to fetch PNG from URL: {url}")
            return False

    def fetch_pngs(self, json_file):
        request_name = json_file.split("/")[-1].split(".json")[0]
        with open(json_file, "r") as f:
            data = json.load(f)
            urls = data["data"]["upscaled_urls"]
            for i, url in enumerate(urls):
                for _ in range(10):
                    is_done = self.fetch_png(url, request_name, i)
                    if is_done:
                        break

    def run(self):
        for fn in os.listdir(self.images_path):
            json_file = os.path.join(self.images_path, fn)
            self.fetch_pngs(json_file)
