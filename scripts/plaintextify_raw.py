import json
import os
import click

from extraction.document import Document

@click.command()
@click.option("--section", help="Filter articles of a certain section")
@click.option("--keyword", help="Filter articles of a certain section")
@click.argument("inputdir")
@click.argument("outputdir")
def plaintextify(inputdir : str,
                 outputdir : str,
                 section : str,
                 keyword : str):
    """
    Takes a directory of extractions json and writes to one output directory: plaintext paragraph dumps.
    Skips empty_output.txt files and filtered by language id dir.
    """

    raw_outdir = os.path.join(outputdir, "raw_paragraphs")

    # Walk the input dir
    for subdir in os.listdir(inputdir):

        if subdir == "audio" or subdir == "video":
            continue

        # Completely skip the filtered directory
        if subdir == "lang_id_filtered":
            continue

        insubdir = os.path.join(inputdir, subdir)
        # Skip non-directories, like .DS_Store files
        if not os.path.isdir(insubdir):
            continue

        raw_sub = os.path.join(raw_outdir, subdir)
        os.makedirs(raw_sub, exist_ok=True)
        files = os.listdir(insubdir)
        for f in files:
            # This ignores empty_output.txt, which is just a list of urls where we didn't
            # extract anything, but it also covers OS files like .DS_Store
            if not f.endswith(".json"):
                continue
            filepath = os.path.join(insubdir, f)
            with open(filepath, "r", encoding="utf8") as infile:
                json_dict = json.load(infile)
                doc = Document.from_dict(json_dict)
            # Skip document if filtering by section
            if section and section != doc.section:
                continue
            if keyword and keyword not in doc.keywords:
                continue
            filename = doc.filename.replace(".html", "") + ".txt"
            raw_path = os.path.join(raw_sub, filename)
            with open(raw_path, "w", encoding="utf8") as raw_out:
                raw_out.write("\n\n".join([doc.title] + doc.paragraphs))

if __name__ == "__main__":
    plaintextify()