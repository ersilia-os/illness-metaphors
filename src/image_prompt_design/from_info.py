from . import BaseImagePromptDesigner, ImagePromptDesignRequest


class ImageDescriptionFromInfo(BaseImagePromptDesigner):
    def __init__(self, disease_name, results_path=None):
        BaseImagePromptDesigner.__init__(disease_name, results_path=results_path)
        self.info = self.read_info_json()

    def _get_landscape(self):
        pass

    def run(self):
        pass