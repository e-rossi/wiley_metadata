from time import sleep
from pandas import json_normalize

from crossref.restful import Works


def create_book_metadata_obejct(line):
    title, isbn = line.split('_')
    return {
        'title': title,
        'isbn': isbn,
        'authors': [],
        'access_link': None
    }


def main(list_):
    books = []
    crossref_works = Works()

    with open(list_) as f:
        lines = [line.rstrip() for line in f]
        for line in lines:
            book_object = create_book_metadata_obejct(line)
            books.append(book_object)

    for book in books:
        for result in crossref_works.filter(isbn=book['isbn'])\
                                    .sample(100)\
                                    .select('title', 'ISBN', 'link', 'author'):
            try:
                if book['isbn'] in result['ISBN']\
                    and book['title'] in result['title']:

                    if result.get('author'):
                        for author in result['author']:
                            name = f"{author['given']} {author['family']}"
                            book['authors'].append(name)

                    if result.get('link'):
                        for link in result['link']:
                            book['access_link'] = link['URL']

            except KeyError as err:
                print(err)
                pass

        sleep(0.5)

    normalised_json = json_normalize(books, sep=',')
    normalised_json.to_excel(
        f'results_{list_}.xlsx',
        verbose=True,
        sheet_name='books',
        encoding='utf-8'
    )


if __name__ == '__main__':
    main('books')
