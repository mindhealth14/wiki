from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from . import util
import markdown2
import random
from .forms import EncyclopediaEntryForm, EditPageForm
from django.contrib import messages





def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# CREATING Detail Page for the Entries that already exist

def detail_page(request, title):
    # Use the provided 'title' parameter, not a string "title"
    entry_content = util.get_entry(title)
    if entry_content:
        # Convert Markdown to HTML
        html_content = markdown2.markdown(entry_content)

        return render(request, 'encyclopedia/entry_page.html', {
            "title": title,
            "entry_content": html_content,  # Pass the HTML content
        })
    else:
        return( HttpResponseRedirect(reverse("error_page")))
    
    
    
def create_entry(request):
    if request.method == 'POST':
        form = EncyclopediaEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            # Check if an entry with the same title exists
            if util.get_entry(title):
                # Display error message if entry already exists
                messages.error(request, f"An entry with the title '{title}' already exists.")
            else:
                # Save the entry only if it doesn't exist
                util.save_entry(title, content)
                return redirect('title', title=title)  # Update the URL name here
    else:
        form = EncyclopediaEntryForm()

    return render(request, 'encyclopedia/create_entry.html', {'form': form})






def random_page(request):
    entries = util.list_entries()
    if entries:
        random_entry = random.choice(entries)
        return redirect('title', title=random_entry)
    else:
        raise Http404("No encyclopedia entries found")
    
    
def edit_page(request, title):
    # Retrieve the existing content of the page
    existing_content = util.get_entry(title)

    if request.method == 'POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            edited_title = form.cleaned_data['title']
            edited_content = form.cleaned_data['content']
            
            # Create a new entry with the updated title and content
            util.save_entry(edited_title, edited_content)
            
            # Delete the old entry (if needed)
            if edited_title != title:
                util.delete_entry(title)
                
            return redirect('title', title=edited_title)
    else:
        # Populate the form with the existing title and content
        form = EditPageForm(initial={'title': title, 'content': existing_content})

    return render(request, 'encyclopedia/edit_page.html', {'form': form})



def delete_entry(request, title):
    # Call the delete_entry function and pass the title as an argument
    util.delete_entry(title)
    return HttpResponseRedirect(reverse('index'))  # Redirect to the index page or any other appropriate page


def page_not_found(request):
    return render(request, 'encyclopedia/error_404.html', status=404)



def search_v(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    # Call the search_entry function to search for the entry by title
    entry_content = util.search_entry(query)

    if entry_content:
        # Entry found, display the content
        return render(request, 'encyclopedia/search_results.html', {
            "title": query,
            "entry_content": entry_content,
        })
    else:
        # Entry not found, raise Http404
        return render(request, 'encyclopedia/error_404.html', {
            "query": query 
        })
     
     
    