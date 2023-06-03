from flask import Flask, render_template
import pandas as pd
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)
csv_file = "logwater.txt"  # Replace with the path to your CSV file
csv_file = os.path.abspath(csv_file)
df = pd.DataFrame()


def highlight_dry_cells(val):
    if "Dry" in val:
        return "background-color: yellow"
    else:
        return ""


def load_data():
    global df
    df = pd.read_csv(csv_file, names=["timestamp", "day/night", "drystate"])
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["day/night"] = df["day/night"].str.replace("night =", "")
    df["day/night"] = df["day/night"].str.replace("True", "Night")
    df["day/night"] = df["day/night"].str.replace("False", "Day")
    df["drystate"] = df["drystate"].str.replace("DRYSTATE =", "")
    df["drystate"] = df["drystate"].str.replace("True", "Dry")
    df["drystate"] = df["drystate"].str.replace("False", "Wet")


class FileModifiedEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == csv_file:
            load_data()


def start_file_monitor():
    event_handler = FileModifiedEventHandler()
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(csv_file), recursive=False)
    observer.start()


@app.route("/")
def display_table():
    global df
    df_filtered = df.tail(20)
    df_filtered = df_filtered.sort_values(by="timestamp", ascending=False)
    df_style = df_filtered.style.applymap(highlight_dry_cells, subset=["drystate"])
    table_html = df_style.hide_index().render()
    # table_html = df_style.to_html(index=False)
    return render_template("table.html", table_html=table_html)


if __name__ == "__main__":
    load_data()  # Load data initially
    print(csv_file, os.path.exists(csv_file))
    start_file_monitor()  # Start file monitoring
    app.run(host="0.0.0.0", port=5000)
