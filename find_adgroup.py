import pandas as pd
import build_adgroup as ba
import build_adcopy as adcopy
import requests
import add_keywords as ak

def get_campaign_id(client, campaign_name):
    campaign_service = client.GetService('CampaignService', version='v201806')

    selector = {
        'fields': ['Id', 'Name'],
        'predicates': [{
            'field': 'Name',
            'operator': 'EQUALS',
            'values': campaign_name
        }]
    }

    page = campaign_service.get(selector)
    try:
        return page['entries'][0]['id']
    except:
        #if there is no campaign, the other script should handle it
        return


def get_adgroup_id(client, campaign_name, brand_model, keywords):
    """
    gets the ad group to insert keywords to. If it doesn't exist, it should create it
    """
    campaign_id = get_campaign_id(client, campaign_name)

    if(not campaign_id):
        #If campaign doesn't exist, ignore for now. campaign_builder.py should handle this
        #print('Campaign doesnt exist')
        return

    adgroup_service = client.GetService('AdGroupService', version='v201806')

    adgroup_name = 'Models_KeywordHarvester_EM_' + str(campaign_id)
    selector = {
        'fields': ['Id', 'Name'],
        'predicates': [{
            'field': 'Name',
            'operator': 'EQUALS',
            'values': adgroup_name
        }]
    }
    page = adgroup_service.get(selector)

    #Need to add display name information from our API
    suggestions_url = 'https://api.hey.car/search/count?q={}%20{}'.format(brand_model['make'], brand_model['model'])
    response = requests.get(suggestions_url).json()
    brand_model['make_display_name'] = response['aggregations']['make']
    brand_model['model_display_name'] = response['aggregations']['model']

    try:
        #the harvester adgroup already esist
        adgroup_id = page['entries'][0]['id']
        ak.add_keyword(client, adgroup_id, keywords, 'EXACT', brand_model)
        print(str(len(keywords)) + ' keywords added for ' + brand_model['make'] + ' ' + brand_model['model'])
    except:
        #harvester adgroup needs to be created for that brand/model
        adgroup_id = ba.add_adgroup(client, campaign_id, adgroup_name)
        adcopy.add_adcopy(client, adgroup_id, brand_model)
        ak.add_keyword(client, adgroup_id, keywords, 'EXACT', brand_model)
        print(str(len(keywords)) + ' keywords added for ' + brand_model['make'] + ' ' + brand_model['model'])
