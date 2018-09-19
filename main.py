import get_search_terms as get_terms
import pandas as pd
import find_adgroup as fa

if __name__ == '__main__':
    df = get_terms.get_terms()
    campaigns = df['dest_campaign'].unique()

    for campaign in campaigns:
        #LOCATE CAMPAIGN/ADGROUP AND GET IDs
        adgroup_id = fa.find_adgroup(campaign)
        #IF CAMPAIGN DOESNT EXIST, JUST IGNORE IT
        #IF ADGROUP DOESNT EXIST, CREATE IT

        #GET TERMS TO BE ADDED
        # terms = df[df['dest_campaign'] == campaign][['Query','Url']]
        # keywords = list(terms[['Query']]['Query'].values)
        # add_keywords
