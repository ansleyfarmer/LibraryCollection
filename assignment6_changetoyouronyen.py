__author__ = 'Ansley Farmer, afar@unc.edu, Onyen = afar'


# Loads data for both books and movies, returning a dictionary with two keys, 'books' and 'movies', one for
# each subset of the collection.
def load_collections():
    # Load the two collections.
    book_collection, max_book_id = load_collection("books.csv")
    movie_collection, max_movie_id = load_collection("movies.csv")

    # Check for error.
    if book_collection is None or movie_collection is None:
        return None, None

    # Return the composite dictionary.
    return {"books": book_collection, "movies": movie_collection}, max(max_book_id, max_movie_id)


# Loads a single collection and returns the data as a dictionary.  Upon error, None is returned.
def load_collection(file_name):
    max_id = -1
    try:
        # Create an empty collection.
        collection = {}

        # Open the file and read the field names
        collection_file = open(file_name, "r")
        field_names = collection_file.readline().rstrip().split(",")

        # Read the remaining lines, splitting on commas, and creating dictionaries (one for each item)
        for item in collection_file:
            field_values = item.rstrip().split(",")
            collection_item = {}
            for index in range(len(field_values)):
                if (field_names[index] == "Available") or (field_names[index] == "Copies") or (field_names[index] == "ID"):
                    collection_item[field_names[index]] = int(field_values[index])
                else:
                    collection_item[field_names[index]] = field_values[index]
            # Add the full item to the collection.
            collection[collection_item["ID"]] = collection_item
            # Update the max ID value
            max_id = max(max_id, collection_item["ID"])

        # Close the file now that we are done reading all of the lines.
        collection_file.close()

    # Catch IO Errors, with the File Not Found error the primary possible problem to detect.
    except FileNotFoundError:
        print("File not found when attempting to read", file_name)
        return None
    except IOError:
        print("Error in data file when reading", file_name)
        return None

    # Return the collection.
    return collection, max_id


# Display the menu of commands and get user's selection.  Returns a string with  the user's reauexted command.
# No validation is performed.
def prompt_user_with_menu():
    print("\n\n********** Welcome to the Collection Manager. **********")
    print("COMMAND    FUNCTION")
    print("  ci         Check in an item")
    print("  co         Check out an item")
    print("  ab         Add a new book")
    print("  am         Add a new movie")
    print("  db         Display books")
    print("  dm         Display movies")
    print("  qb         Query for books")
    print("  qm         Query for movies")
    print("  x          Exit")
    return input("Please enter a command to proceed: ")


# This is the main program function.  It runs the main loop which prompts the user and performs the requested actions.
def main():
    # Load the collections, and check for an error.
    library_collections, max_existing_id = load_collections()

    if library_collections is None:
        print("The collections could not be loaded. Exiting.")
        return
    print("The collections have loaded successfully.")

    # Display the error and get the operation code entered by the user.  We perform this continuously until the
    # user enters "x" to exit the program.  Calls the appropriate function that corresponds to the requested operation.
    operation = prompt_user_with_menu()
    while operation != "x":
        ###############################################################################################################
        ###############################################################################################################
        # HINTS HINTS HINTS!!! READ THE FOLLOWING SECTION OF COMMENTS!
        ###############################################################################################################
        ###############################################################################################################
        #
        # The commented-out code below gives you a some good hints about how to structure your code.
        #
        # FOR BASIC REQUIREMENTS:
        #
        # Notice that each operation is supported by a function.  That is good design, and you should use this approach.
        # Moreover, you will want to define even MORE functions to help break down these top-level user operations into
        # even smaller chunks that are easier to code.
        #
        # FOR ADVANCED REQUIREMENTS:
        #
        # Notice the "max_existing_id" variable?  When adding a new book or movie to the collection, you'll need to
        # assign the new item a unique ID number.  This variable is included to make that easier for you to achieve.
        # Remember, if you assign a new ID to a new item, be sure to keep "max_existing_id" up to date!
        #
        # Have questions? Ask on Piazza!
        #
        ###############################################################################################################
        ###############################################################################################################
        if operation == "ci":
            check_in(library_collections)

        elif operation == "co":
            check_out(library_collections)

        elif operation == "ab":
            max_existing_id = add_book(library_collections["books"], max_existing_id)
            library_collections["books"] = max_existing_id

        elif operation == "am":
            max_existing_id = add_movie(library_collections["movies"], max_existing_id)
            library_collections["movies"] = max_existing_id

        elif operation == "db":
            display_collection(library_collections["books"])

        elif operation == "dm":
            display_collection(library_collections["movies"])

        elif operation == "qb":
            query_collection(library_collections["books"], "book")

        elif operation == "qm":
            query_collection(library_collections["movies"], "movie")
        else:
            print("Unknown command.  Please try again.")

        operation = prompt_user_with_menu()


def search(collection, attribute, query):
    # list to keep track of matching query from attribute
    matches = []
    for book_info in collection.values():
        # print(book_info[attribute])
        if query in book_info[attribute]:
            matches.append(book_info)
    return matches


# sends
def query_collection(collection, type):
    # list to keep track of all matching query
    matches = []
    query = input("Enter a query string to use for the search:")
    if type == "book":
        matches.append(search(collection, "Title", query))
        matches.append(search(collection, "Author", query))
        matches.append(search(collection, "Publisher", query))

    if type == "movie":
        matches.append(search(collection, "Title", query))
        matches.append(search(collection, "Director", query))
        matches.append(search(collection, "Genre", query))
    print(matches)
    return matches


def display_collection(collection):
    count = 0
    for id in collection:
        if count < 10:
            print(collection[id])
        count = count + 1
        if count == 10:
            more = input("Press enter to show more items, or type 'm' to return to the menu: ")
            count = 0
            if more == "m":
                return None
    return None


def add_book(collection, id):
    id = id + 1

    title = input("Enter the title of the new book: ")
    author = input("Enter the author of the new book: ")
    publisher = input("Enter the publisher of the new book: ")
    pages = input("Enter the number of pages of the new book: ")
    year = input("Enter the publication year of the new book: ")
    copies = input("Enter the number of copies of the new book: ")
    available = input("Enter the number of available copies of the new book: ")

    new_book = {
        "Title": title,
        "Author": author,
        "Publisher": publisher,
        "Pages": pages,
        "Year": year,
        "Copies": int(copies),
        "Available": int(available),
        "ID": id
    }
    print("You have entered the following data: ")
    print(new_book)
    add = input("Press enter to add this item to the collection. Enter 'x' to cancel.")

    if add == "x":
        return None

    # should return just the book part then need to add the books to the whole collection in the first part
    return collection


def add_movie(collection, id):
    id = id + 1
    title = input("Enter the title of the new movie: ")
    director = input("Enter the director of the new movie: ")
    length = input("Enter the length of the new movie: ")
    genre = input("Enter the genre of the new movie: ")
    year = input("Enter the release year of the new movie: ")
    copies = input("Enter the number of copies of the new movie: ")
    available = input("Enter the number of available copies of the new movie: ")

    new_movie = {
        "Title": title,
        "Director": director,
        "Length": length,
        "Genre": genre,
        "Year": year,
        "Copies": int(copies),
        "Available": int(available),
        "ID": id
    }

    print("You have entered the following data: ")
    print(new_movie)
    add = input("Press enter to add this item to the collection. Enter 'x' to cancel.")

    if add == "x":
        return None
    collection[id] = new_movie
    # should return just the book part then need to add the books to the whole collection in the first part
    return collection


# Sees if ID is related to book or movie
def find_by_id(library_collections, item_id):
    item_type = "unknown"
    # Search through books
    books = library_collections["books"]
    for collection_id in books:
        if int(collection_id) == int(item_id):
            item_type = "books"

    # Search through movies
    movies = library_collections["movies"]
    for collection_id in movies:
        if int(collection_id) == int(item_id):
            item_type = "movies"

    if item_type == "unknown":
        print("Error, ID not found, please retry.")
        return None
    else:
        return item_type


def check_in(library_collections):
    item_id = input("Enter the ID for the item you wish to check in: ")
    collection_type = find_by_id(library_collections,item_id)

    amt_available = library_collections[collection_type][int(item_id)]['Available']

    library_collections[collection_type][int(item_id)]['Available'] = int(amt_available) + 1

    print("Your check in has succeeded.")
    print(library_collections)
    return library_collections


def check_out(library_collections):
    item_id = input("Enter the ID for the item you wish to check in: ")
    collection_type = find_by_id(library_collections, item_id)

    amt_available = library_collections[collection_type][int(item_id)]['Available']

    if amt_available <= 0:
        print("Sorry, book is not available at the moment.")
        return library_collections

    library_collections[collection_type][int(item_id)]['Available'] = int(amt_available) - 1

    print("Your check in has succeeded.")
    print(library_collections)
    return library_collections


# Kick off the execution of the program.
main()


