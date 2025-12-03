from textual.app import App, ComposeResult, on
from textual.widgets import Header, Footer, DirectoryTree, Markdown
from textual.containers import Horizontal
import os
import click

class NotesBrowser(App):
    """textual app to browse notes."""

    DEFAULT_CSS = """
    #tree-view {
        width: 30%;
        height: 100%;
    }
    #file-view {
        width: 70%;
        height: 100%;
        display: none; /* hidden by default */
        padding: 1;
        border: round white;
        overflow-y: auto;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "hide_file_view", "close file view"),
    ]

    def __init__(self, notes_dir: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notes_dir = notes_dir

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Horizontal(
            DirectoryTree(self.notes_dir, id="tree-view"),
            Markdown(id="file-view"),
        )

    @on(DirectoryTree.FileSelected)
    def on_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """called when a file is selected in the directory tree."""
        file_path = event.path
        file_viewer = self.query_one("#file-view", Markdown)
        
        if file_path.is_file():
            try:
                content = file_path.read_text()
                file_viewer.update(content)
                file_viewer.styles.display = "block" # show the file view
            except Exception as e:
                file_viewer.update(f"error reading file: {e}")
                file_viewer.styles.display = "block"
        else:
            # if a directory is selected, hide the file view
            file_viewer.styles.display = "none"


    def action_hide_file_view(self) -> None:
        """called when the user presses escape."""
        file_viewer = self.query_one("#file-view", Markdown)
        file_viewer.styles.display = "none"


@click.command()
@click.option("--notes-dir", default="notes", help="directory containing notes.")
def browse(notes_dir):
    """launches an interactive notes browser."""
    app = NotesBrowser(notes_dir)
    app.run()

if __name__ == "__main__":
    browse()
