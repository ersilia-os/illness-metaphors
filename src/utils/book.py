import os
import shutil

root = os.path.dirname(os.path.abspath(__file__))


class PrepareGitBook(object):
    def __init__(self, results_dir=None, book_dir=None):
        if results_dir is None:
            results_dir = os.path.abspath(os.path.join(root, "..", "..", "results"))
        self.results_dir = results_dir
        if book_dir is None:
            book_dir = os.path.abspath(os.path.join(root, "..", "..", "book"))
        self.book_dir = book_dir
        self.summary_file = os.path.join(book_dir, "SUMMARY.md")
        self.readme_file = os.path.join(book_dir, "README.md")
    
    @staticmethod
    def _prettify(text):
        text = text.replace("_", " ")
        text = text.capitalize()
        return text

    def _write_summary(self):
        info_files = {}
        for fn in os.listdir(os.path.join(self.results_dir, "info", "markdown")):
            shutil.copyfile(os.path.join(self.results_dir, "info", "markdown", fn), os.path.join(self.book_dir, "info", fn))
            if fn.endswith(".md"):
                info_files[fn.split(".md")[0]] = os.path.join(self.book_dir, "info", fn)
        prompt_files = {}
        for fn in os.listdir(os.path.join(self.results_dir, "prompts", "markdown")):
            shutil.copyfile(os.path.join(self.results_dir, "prompts", "markdown", fn), os.path.join(self.book_dir, "prompts", fn))
            if fn.endswith(".md"):
                prompt_files[fn.split(".md")[0]] = os.path.join(self.results_dir, "prompts", "markdown", fn)
        keys = sorted(info_files.keys())
        with open(self.summary_file, "w") as f:
            f.write("# Summary\n\n")
            for k in keys:
                t = self._prettify(k)
                f.write(f"* [{t}](info/{k}.md)\n")
                f.write(f"  * [Prompts](prompts/{k}.md)\n")

    def run(self):
        self._write_summary()
    