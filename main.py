import get_search_terms as get_terms
import pandas as pd
import find_adgroup as fa

def main():
    df = get_terms.get_terms()
    campaigns = df['dest_campaign'].unique()

    for campaign in campaigns:
        #LOCATE CAMPAIGN/ADGROUP AND GET IDs
        #we also need to get the make and model in case the adgroup doesn't exist: we will need to build ad copy
        brand = list(terms[terms['dest_campaign'] == 'Models_SkodaCitigo_EM'][['make']].values)[0][0]
        model = list(terms[terms['dest_campaign'] == 'Models_SkodaCitigo_EM'][['model']].values)[0][0]
        brand_model = {'make': brand, 'model': model}
        adgroup_id = fa.get_adgroup_id(campaign, brand_model)
        #GET TERMS TO BE ADDED
        terms = df[df['dest_campaign'] == campaign][['Query','Url']]
        keywords = list(terms[['Query']]['Query'].values)

        #Add keywords


if __name__ == '__main__':
    main()
