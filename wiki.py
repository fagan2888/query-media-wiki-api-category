import requests

class WikiClient():
    """A wrapper around MediaWiki's API

    Exposes methods to request data from MediaWiki's API:
        
        - get_backlinked_pages()
        - get_page_data()

    Attributes:
        endpoint_url (str) - url of a MediaWiki API backend
                             Defaults to 'https://www.wikidata.org/w/api.php'
    """

    def __init__(self, url=False):
        if url:
            self.endpoint_url = url
        else:    
            self.endpoint_url = 'https://www.wikidata.org/w/api.php'            


    def get_backlinked_pages(self, title, limit=False):
        """Finds all pages that backlink to the `title` page

        Args:
            title (str): The title of the page that is backlinked to
                         TODO *** provide little explaination what a title is***                
            
            limit (int, optional): The total number of pages to return.
                Use False to return all pages. Defaults to False.

        Returns:
            list(str): The titles of pages that backlink to `title`
        """
        if not isinstance(limit, int) or limit < 1:
            raise ValueError(limit)
        # EP: at this point limit is int type and likely has value 5000  
        
        # QUESTION: is limit a batch size or an overall limit on page_ids?
        #           can we retrive more than 500 page_ids?

        page_ids = list()
        params = {
                'action':'query',
                'format':'json',
                'list':'backlinks',
                'bltitle':title,
                'bllimit':limit
                }


        must_continue = True        
        while must_continue:
            r = requests.get(self.endpoint_url, params=params)
            data = r.json()
            for backlink in data['query']['backlinks']:
                page_ids.append(backlink['title'])
                # QUESTION: this function can also be an iterator:
                #           yield backlink['title']               

            # Check if we need to continue making requests
            
            if len(page_ids) >= limit:
                must_continue = False
            elif 'continue' not in data:
                must_continue = False
            else:
                params['continue'] = data['continue']['continue']
                params['blcontinue'] = data['continue']['blcontinue']

        return page_ids

    def get_page_data(self, title):
        """Returns the full text of the requested page

        Args:
            title (str): The title of the page to return
                         TODO *** provide little explaination what a title is***                

        Returns:
            str: The `str` representation of the requested page's JSON
        """

        params = {
                'action':'wbgetentities',
                'format':'json',
                'ids':title,
                'languages':'en'
                }

        r = requests.get(self.endpoint_url, params=params)
        data = r.json()

        return data
    
if "__main__" == __name__:    

    d = WikiClient().get_page_data(title = "P569")
    
    e = WikiClient().get_backlinked_pages("Q5")    
    assert len(e) == 500    
    
    # any pagination available? something like a pointer to next 500 entries? 
    # somehow it gets linked here 
    # https://www.wikidata.org/w/index.php?title=Special:WhatLinksHere/Q5&limit=500&from=10643&back=7545
    
