import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    """ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")"""


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability = dict()
    
    pages = corpus.keys()
    total_pages = len(pages)
    
    direct_links = corpus[page]
    total_direct_links = len(direct_links)
    
    for page in pages:
        if page in direct_links:
            probability[page] = (damping_factor * (1 / total_direct_links)) + ((1 - damping_factor)/total_pages)
        else:
            probability[page] = (1 - damping_factor)/total_pages
    
    return probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict()
    
    pages= list(corpus.keys())
    total_pages = len(pages)
    for page in pages:
        page_rank[page] = 0
        
    initial_page = random.randrange(total_pages)
    next_probability = transition_model(corpus, pages[initial_page], damping_factor)
    
    for i in range(n):
        weights = list(next_probability.values())
        population = list(next_probability.keys())
        next_page = random.choices(population, weights)
        page_rank[next_page[0]] += 1
        
        next_probability = transition_model(corpus, next_page[0], damping_factor)
        
    for page in page_rank:
        page_rank[page] /= n
    
    return page_rank
    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    return corpus


if __name__ == "__main__":
    main()
