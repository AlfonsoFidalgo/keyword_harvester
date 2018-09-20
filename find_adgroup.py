from googleads import adwords
import pandas as pd
import build_adgroup as ba
import build_adcopy as adcopy
import requests
client = adwords.AdWordsClient.LoadFromStorage('../adwords_api/googleads.yaml')
client.client_customer_id = '5744449309' #Models

def get_campaign_id(campaign_name):
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
        print('No campaign found with that name')
        return


def get_adgroup_id(campaign_name, brand_model):
    """
    gets the ad group to insert keywords to. If it doesn't exist, it should create it
    """
    campaign_id = get_campaign_id(campaign_name)

    if(not campaign_id):
        #If campaign doesn't exist, ignore for now. campaign_builder.py should handle this
        print('Campaign doesnt exist')
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

    try:
        adgroup_id = page['entries'][0]['id']
        return adgroup_id
    except:
        adgroup_id = ba.add_adgroup(client, campaign_id, adgroup_name)

        #Need to add display name information
        suggestions_url = 'https://api.hey.car/search/count?q={}%20{}'.format(brand_model['make'], brand_model['model'])
        response = requests.get(suggestions_url).json()
        brand_model['make_display_name'] = response['aggregations']['make']
        brand_model['model_display_name'] = response['aggregations']['model']

        adcopy.add_adcopy(client, adgroup_id, brand_model)
        ##NEED TO PASS Brand/Model INFO TO BUILD ADS
        return adgroup_id
