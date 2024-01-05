import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def delete_entry(title):
    """
    Deletes an encyclopedia entry by its title. If no such
    entry exists, nothing happens.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)



def edit_entry(title, new_content):
    """
    Edits an encyclopedia entry with the given title, replacing the content.
    """
    filename = f"entries/{title}.md"
    try:
        with default_storage.open(filename, 'w') as f:
            f.write(new_content)
    except Exception as e:
        # Handle exceptions (e.g., file not found, permissions error, etc.)
        print(f"Error editing entry: {e}")


def search_entry(title):
    """
    Searches for an encyclopedia entry by title. Returns the content of the entry
    if found, otherwise returns None.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        try:
            f = default_storage.open(filename)
            return f.read().decode("utf-8")
        except FileNotFoundError:
            return None
    else:
        return None