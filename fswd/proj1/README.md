# Project 1: Movie Trailer Website

Create a static web page with box art imagery and trailer URLs to allow visitors
to browse movies and watch the trailers.

## How it does it

It searches the [Open Movie Database][1] (OMDB) for the title of a movie. If the
movie is found, the response may include other details of the movie, including a
URL to a movie poster. If the response contains the poster URL, then it searches
[YouTube][2] for the URL of the movie trailer, and all of the information is
stored in a database to avoid having to search for the information again.

## How to use it

The driver of the program is *ecenter.py*, and it is designed to be used via the
command line. Below are a few examples of how the program can be used.

#### Getting a help message

```
$ ./ecenter.py --help
usage: ecenter.py [-h] [--dbfile DBFILE] [-f FILE] [-l LIST] [-s SEPARATOR]
                  [-x]

Create Fresh Tomatoes Web Page

optional arguments:
  -h, --help            show this help message and exit
  --dbfile DBFILE       The database for the movie trailers (default:
                        movie_trailer_db)
  -f FILE, --file FILE  Input file to get movie titles from, with one title
                        per line (default: None)
  -l LIST, --list LIST  List of movies separated by separator (default: None)
  -s SEPARATOR, --separator SEPARATOR
                        The separator used if a list of movies is provided
                        (default: ,)
  -x, --exclude         Exclude the default titles. List or file must be
                        specified. (default: False)
```

#### Simplest use case

```{bash}
$ ./ecenter.py
```

Searches for default movies, which are hard coded.

#### A list of movies

```
$ ./ecenter.py -l "braveheart, inception"
```

Specify the separator to avoid splitting the title, if including one with an
embedded comma.

```
$ ./ecenter.py -l "the good, the bad and the ugly" -s "|"
```

#### A file with a list of movies

Assuming *movies.txt* contains the following content

```
ocean's eleven
pretty woman
blade runner
the big short
her
```

then the titles can be processed by specifying the name of the file

```
$ ./ecenter.py -f movies.txt
```

#### Exclude default titles

```
$ ./ecenter.py -l "braveheart, inception" -x
```

This will only include a search for the two movies in the list, and default
movies will be ignored. Excluding default movies requires that some movies
be specified via at least a list or file.

## Details

* If the movie is not found in the database, which will always be the case
  the first time the program is run, then it is necessary to query the OMDB
  and YouTube. OMDB is not big and cannot handle many request at a time, and
  YouTube is not accessed via an API meant for bots; therefore, there is a delay
  of 1 second added after such a search in order to avoid a hangup. Subsequent
  searches should be faster, assuming the same database file is used.
* Error messages are directed to standard error, and logging is directed to
  standard output.
* There is one default movie which is found, but does not have a URL for a
  poster and results in an error message. The movie is there as an example
  of how an error is treated. 

[1]: http://www.omdbapi.com/
[2]: https://www.youtube.com/
