from jupyterfair.core.client import *

class FourTuData(Client):
    '''
    '''
    TOKEN = config.FOURTU_TOKEN
    BASE_URL = 'https://api.figshare.com/v2/{endpoint}'

    def create_deposition(self, article_title):
        data = {
            'title': article_title  # You may add any other information about the article here as you wish.
        }
        response = self.issue_request('POST', 'account/articles', data=data)
        data = json.loads(response.content)
        print ('Created article:', data['location'], '\n')
        return response
    


    def list_articles(self):
        return self.issue_request('GET', 'account/articles')

    

