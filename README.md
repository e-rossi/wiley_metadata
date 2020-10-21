# wiley_metadata
A short script made for getting books' metadata from Wiley Online Library.

## Problem ##

I had an excel sheet containing a lot of books, with title and isbn, but I also needed to get the author's name and the book's access link.

## Solution ##

Instead of going to Wiley Online Library and manually searching each book, this automation gets it all via their API, here wrapped in a Python library.

## Step-by-step ##

### File formating ###
There is an example file in this directory already, but just to be explicit, I didn't have the time to learn how to work with xlsx files in Python right now, so I copied the lines and pasted them on a file, replacing the space between cells with an underscore, which is parsed in the script. The lines follow a `title_isbn` structure:
```
Book title_123456789
```

### Lines 1 through 4: Imports ###
Importing is using an existing package to do something in your code. Four packages were needed here:
#### sleep function from the time module ####
Wiley's API requires delay between requests, since it is an open API and anyone could flood the server. The sleep function blocks the program from running for the set time, because without it this script would be sending A LOT of requests per second and I would propably get banned from using the API at all.

#### json_normalize from the pandas library ####
The pandas library is a poweful resource for manipulating data and it has great methods for formatting and converting data structures, in this case from JSON to XLSX.

#### Works class from the crossref restful implementation of the wiley API ####
This is crossref's interface for their available works, through it, it's possible to query their database using a filter, setting a sample size and selecting which fields we'd like to get.

### Lines 7 through 14: Book object creation function ###
This function takes a line in the `title_isbn` format and returns a dictionary with the organized information.

### Lines 17 through 56: Main function ###
It starts by opening the file with the books and creating a list of lines, each line is then passed to the previously defined function and the resulting object is appended to the books list.

Now, for each book in the books list, a search is made on the crossref Works API with a sample size of 100 and if the result matches the search object's parameters, the logic for getting the author and access link is run.

If any errors in the dict manipulations occur, it is simply ignored and the next one is run. At the end of the iteration, the process waits for .5 second to do another search.

After every book is processed, the list is normalized into a proper json and it is converted to xlsx and saved to the root directory.

NOTE: As there is no HTTP Session handling, after some time it expires and the whole process is cancelled, so the file shouldn't be large as it risks not outputting anything.

### Lines 59 and 60: Script executor ##
Standard python module runner for standalone scripts
