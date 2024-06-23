import json
import time
import http.client
import pprint
import dotenv
import os
import requests
import random

root = os.path.dirname(os.path.abspath(__file__))

dotenv.load_dotenv(os.path.join(root, "..", "..", ".env"))

IMAGINE_API_KEY = os.getenv("IMAGINE_API_KEY")


class ImagineApi(object):
    def __init__(
        self, disease_name, use_reference_image=False, results_path=None, data_path=None
    ):
        self.use_reference_image = use_reference_image
        self.disease_name = disease_name
        self.disease_base_name = disease_name.replace(" ", "_").lower()
        if results_path is None:
            results_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "results")
            )
        if not os.path.exists(results_path):
            os.makedirs(results_path)
        if use_reference_image:
            subfolder = "with_reference"
        else:
            subfolder = "without_reference"
        disease_results_path = os.path.join(
            results_path, "images", subfolder, self.disease_base_name
        )
        print(disease_results_path)
        if not os.path.exists(disease_results_path):
            os.makedirs(disease_results_path)
        self.results_path = results_path
        self.disease_results_path = disease_results_path
        if data_path is None:
            data_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), "..", "..", "data", "jpegs", "reference"
                )
            )
        self.data_path = data_path

    def is_already_generated_without_reference(self, request_name):
        json_file = os.path.join(self.disease_results_path, f"{request_name}.json")
        return os.path.exists(json_file)

    def is_already_generated_with_reference(self, request_name, reference_number):
        json_file = os.path.join(
            self.disease_results_path, f"{request_name}-{reference_number}.json"
        )
        return os.path.exists(json_file)

    def get_all_reference_image_urls(self):
        jpg_filenames = []
        for fn in os.listdir(self.data_path):
            if not fn.endswith(".jpg"):
                continue
            if not fn.startswith(self.disease_base_name):
                continue
            jpg_filenames.append(fn)
        urls = []
        for jpg_filename in jpg_filenames:
            reference_number = jpg_filename.split("_")[-1].split(".jpg")[0]
            urls += [
                (
                    reference_number,
                    f"https://github.com/ersilia-os/illness-metaphors/blob/main/data/jpegs/reference/{jpg_filename}?raw=true",
                )
            ]
        return urls

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

    def generate_and_save_image_urls_without_reference(self, request_name, prompt):
        data = {"prompt": prompt}
        response_data = self.do_request(data)
        response_data["request_name"] = request_name
        response_data["disease_name"] = self.disease_base_name
        json_file = os.path.join(self.disease_results_path, f"{request_name}.json")
        with open(json_file, "w") as f:
            json.dump(response_data, f, indent=4)

    def generate_and_save_image_urls_with_reference(
        self, request_name, reference_number, prompt, reference_url
    ):
        iw = round(random.uniform(1, 2.5), 2)
        prompt = f"{reference_url} {prompt} --iw {iw}"
        data = {"prompt": prompt}
        response_data = self.do_request(data)
        response_data["request_name"] = request_name
        response_data["disease_name"] = self.disease_base_name
        response_data["reference_number"] = reference_number
        response_data["image_weight"] = iw
        json_file = os.path.join(
            self.disease_results_path, f"{request_name}-{reference_number}.json"
        )
        with open(json_file, "w") as f:
            json.dump(response_data, f, indent=4)

    def run_without_reference(self):
        with open(
            os.path.join(
                self.results_path, "prompts", "json", f"{self.disease_base_name}.json"
            )
        ) as f:
            prompts = json.load(f)["midjourney_prompts"]
        for request_name, prompt in prompts.items():
            if self.is_already_generated_without_reference(request_name):
                continue
            print(request_name, prompt)
            self.generate_and_save_image_urls_without_reference(request_name, prompt)

    def run_with_reference(self):
        with open(
            os.path.join(
                self.results_path, "prompts", "json", f"{self.disease_base_name}.json"
            )
        ) as f:
            prompts = json.load(f)["midjourney_prompts"]
        for request_name, prompt in prompts.items():
            for reference_number, reference_url in self.get_all_reference_image_urls():
                if self.is_already_generated_with_reference(
                    request_name, reference_number
                ):
                    continue
                print(request_name, reference_number, prompt)
                self.generate_and_save_image_urls_with_reference(
                    request_name=request_name,
                    reference_number=reference_number,
                    prompt=prompt,
                    reference_url=reference_url,
                )

    def clean_non_completed_json_files(self):
        for fn in os.listdir(self.disease_results_path):
            if not fn.endswith(".json"):
                continue
            with open(os.path.join(self.disease_results_path, fn), "r") as f:
                data = json.load(f)
                if data["data"]["status"] != "completed":
                    os.remove(os.path.join(self.disease_results_path, fn))

    def run(self):
        if self.use_reference_image:
            self.run_with_reference()
        else:
            self.run_without_reference()
        self.clean_non_completed_json_files()
        

class PngFetcher(object):
    def __init__(self, disease_name, results_path=None):
        self.disease_name = disease_name
        self.disease_base_name = disease_name.replace(" ", "_").lower()
        if results_path is None:
            results_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "results")
            )
        images_path_with_reference = os.path.join(
            results_path, "images", "with_reference", self.disease_base_name
        )
        images_path_without_reference = os.path.join(
            results_path, "images", "without_reference", self.disease_base_name
        )
        self.results_path = results_path
        self.images_path_with_reference = images_path_with_reference
        self.images_path_without_reference = images_path_without_reference
        self.pngs_path_with_reference = os.path.join(
            results_path, "pngs", "with_reference", self.disease_base_name
        )
        self.pngs_path_without_reference = os.path.join(
            results_path, "pngs", "without_reference", self.disease_base_name
        )
        if not os.path.exists(self.pngs_path_with_reference):
            os.makedirs(self.pngs_path_with_reference)
        if not os.path.exists(self.pngs_path_without_reference):
            os.makedirs(self.pngs_path_without_reference)

    def fetch_png_without_reference(self, url, request_name, image_number):
        png_filename = f"{self.disease_base_name}-{request_name}-{image_number}.png"
        png_file = os.path.join(self.pngs_path_without_reference, png_filename)
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

    def fetch_png_with_reference(
        self, url, request_name, image_number
    ):
        png_filename = f"{self.disease_base_name}-{request_name}-{image_number}.png"
        png_file = os.path.join(self.pngs_path_with_reference, png_filename)
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

    def fetch_pngs_without_reference(self, json_file):
        request_name = json_file.split("/")[-1].split(".json")[0]
        with open(json_file, "r") as f:
            data = json.load(f)
            urls = data["data"]["upscaled_urls"]
            if urls is None:
                return
            for i, url in enumerate(urls):
                for _ in range(10):
                    is_done = self.fetch_png_without_reference(url, request_name, i)
                    if is_done:
                        break

    def fetch_pngs_with_reference(self, json_file):
        request_name = json_file.split("/")[-1].split(".json")[0]
        with open(json_file, "r") as f:
            data = json.load(f)
            urls = data["data"]["upscaled_urls"]
            if urls is None:
                return
            for i, url in enumerate(urls):
                for _ in range(10):
                    is_done = self.fetch_png_with_reference(url, request_name, i)
                    if is_done:
                        break

    def run(self):
        for fn in os.listdir(self.images_path_without_reference):
            json_file = os.path.join(self.images_path_without_reference, fn)
            self.fetch_pngs_without_reference(json_file)
        for fn in os.listdir(self.images_path_with_reference):
            json_file = os.path.join(self.images_path_with_reference, fn)
            self.fetch_pngs_with_reference(json_file)
