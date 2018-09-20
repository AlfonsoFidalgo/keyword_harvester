import get_search_terms as get_terms
import pandas as pd
import find_adgroup as fa
from googleads import adwords

client = adwords.AdWordsClient.LoadFromStorage('../adwords_api/googleads.yaml')
client.client_customer_id = '6503001352'# 'Test account' #Models '5744449309'

def main():
    df = get_terms.get_terms()
    campaigns = df['dest_campaign'].unique()

    for campaign in campaigns:
        #GET TERMS TO BE ADDED
        terms = df[df['dest_campaign'] == campaign][['Query','Url', 'make', 'model', 'dest_campaign']]
        keywords = list(terms[['Query']]['Query'].values)

        #LOCATE CAMPAIGN/ADGROUP AND GET IDs
        #we also need to get the make and model in case the adgroup doesn't exist: we will need to build ad copy
        brand = list(terms[terms['dest_campaign'] == campaign][['make']].values)[0][0]
        model = list(terms[terms['dest_campaign'] == campaign][['model']].values)[0][0]
        brand_model = {'make': brand, 'model': model}
        fa.get_adgroup_id(client, campaign, brand_model, keywords)


if __name__ == '__main__':
    main()
