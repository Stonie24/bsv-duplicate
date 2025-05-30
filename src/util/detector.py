from src.util.parser import parse, Article

def detect_duplicates(data: str) -> list[str]:
    """Detect duplcate article entries in a raw text file containing bibliographic references in BibTeX format. 
    Two articles are considered duplicates if they have the same key (in case either or both articles miss a DOI) or if they have the same key or DOI.

    parameters:
        data: the raw text file representing a bibliography in BibTeX format

    returns: a list of duplicate articles

    throws: 
        ValueError: if the input data contains less than two articles
    """
    articles: list[str] = parse(data)
    
    if len(articles) < 1:
        raise ValueError("The input data does not contain enough articles to detect duplicates.")

    duplicates: list[Article] = []

    for i in range(len(articles)):
        for j in range(i + 1, len(articles)):
            if articles[i].doi!=None and articles[j].doi!=None:
                if articles[i].key == articles[j].key and articles[i].doi == articles[j].doi:
                    duplicates.append(articles[j])
            else:
                if articles[i].key == articles[j].key:
                    duplicates.append(articles[j])

    return duplicates
