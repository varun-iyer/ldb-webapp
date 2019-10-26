# LDB Minimum Viable Project
## Installation
You can install it locally by cloning + pip install -r requirements.txt

You can also get it through pip but this is useless as you want to run it with flask, not python.

Run with flask run while you’re in the tld.



Forget your directories full of random arXiv-numbered PDFs or
cryptically-labeled court documents.
A librarian for research literature. Search, preview, and download articles.
Grep through, annotate, and cite your locally saved documents.
Working title, librarian-database, LaDdBrarian (after one of my teachers), also
a convenient, unused three-character bin command.
## Purpose
Serves as an online repository client and local db which allows users to
find and manage their literature.
## UI
### LDB
`ldb`: universal prefix for all following subcomands, like git.
Alone, it prints a help text. Each subcommand can also be used with a short
letter command
### Search
`(s)earch [OPTS] [TERM]`: starts the online repository client
Searches online repository(ies) for a particular
search term. Options allow selection of repository and  advanced search
for authors, year published, etc. Displays list of articles in curses/tui
interface
#### Opts
* `-a` author
* `-t` title
* `-b` before date
* `-d` after date
#### Interface
* `k` move up on  the article list
* `j` move down on  the article list
* `C-u` move 5 items up
* `C-d` move 5 items down
* `G` move to bottom of list
* `gg` move to top of list
* `1-9` jump to a specific article in the list
* `l` or `Enter` display abstract of selected article in pager
* `f` view full article in pager or pdf viewer
* `s` save article
* `q` quits interactive client
### List
`(l)ist [SORT]`
* `-r` reverse whatever sorting option is chosen
* `(au)thor`: sort alpha by author
* `(ac)cessed`: sort by date accessed/stored
* `(cr)eated`: sort by date article was created
### Grep
`(g)rep [OPTS] [REGEXP]` Prints list of articles whose text match regexp
* Search through text [REGEXP] and metadata
* Opts to specify search field similar to above
* Maybe sorting like above?
### Open
`(o)pen [OPTS] [SEARCH]`
* Similar to grep, but opens the file in a viewer if there is one match
* If more than one match, opens a TUI list with a similar interface as the one
described above
* Maybe multiple selections?
### Cite
`(c)ite [FORMAT] [OPTS] [SEARCH]`
* Prints citations of all literature which matches search queries
* Uses the given format for citations, possible candidates: APA, MLA, BlueBook,
Ap J, IEEE
### Help
`(h)elp [SUBCOMMAND]`
* Prints a help for `ldb` or a help for the given subcommand
## Implementation
* `tui.py`
```python
class TUIItem(ABC):
	"""
	Abstract class for objects displayed on a text user interface.
	"""

	def __init__(self):
		super().__init__()
	
	@abstractmethod
	def title(self):
		"""
		Return a title string of <72 characters
		"""

	@abstractmethod
	def text(self):	
		"""
		Return brief text for the item, 72 chars * 3 lines
		"""


def display(itemlist):
	"""
	Accepts a list of TUIItems and genrates a TUI to navigate between them.
	Implements basic vim-like movement commands. When a non-navigation
	command i received, it does Item.__call__(<key pressed>)
	Arguments:
		itemlist -- list of Item objects to display
	Returns:
		Nothing. Usually the last thing called in in the program
	"""
```
* `ldb.py`
```python
def init(path):
	"""
	creates a new .ldb directory and database in the specified path
	"""
```
* `db.py`
```python
```
* `document.py`
```python
class Document:
	"""
	Stores information about the document
	"""
```
