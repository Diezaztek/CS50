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
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


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
    page_rank = dict()
    pages = list(corpus.keys())
    total_pages = len(pages)
    initial_probability = (1 - damping_factor) / total_pages
    
    for page in pages:
        page_rank[page] = initial_probability
        
    has_converged = False
    previous_rank = page_rank.copy()
    
    while not has_converged:
        for page in corpus:
            #Calculate new range for each page
            pages_with_link_to_curr_page = list()
            for i_page, links in corpus.items():
                if page in links:
                    pages_with_link_to_curr_page.append(i_page)
            
            inner_summatory = 0
            for page_link in pages_with_link_to_curr_page:
                inner_summatory += (previous_rank[page_link] / len(corpus[page_link]))
            page_rank[page] = initial_probability + (inner_summatory * damping_factor)
        
        has_converged = True
        for page in corpus:
            #Verify if the range has converged for every page
            if abs(previous_rank[page] - page_rank[page]) > 0.001:
                has_converged = False
                previous_rank = page_rank.copy()
                break
    
    return page_rank


if __name__ == "__main__":
    main()
