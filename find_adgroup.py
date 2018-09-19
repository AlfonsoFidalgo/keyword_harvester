from googleads import adwords
import pandas as pd
client = adwords.AdWordsClient.LoadFromStorage('../adwords_api/googleads.yaml')

def get_campaign_id(campaign_name):
    campaign_service = client.GetService('CampaignService', version='v201806')
    client.client_customer_id = '5744449309' #Models

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
        print('No campaign found with that name')

def get_adgroup_id(campaign_name):
    """
    gets the ad group to insert keywords to. If it doesn't exist, it should create it
    """
    campaign_id = get_campaign_id(campaign_name)

    if(not campaign_id):
        #If campaign doesn't exist, ignore for now. campaign_builder.py should handle this
        print('Campaign doesnt exist')
        return

    adgroup_service = client.GetService('AdGroupService', version='v201806')
    client.client_customer_id = '5744449309' #Models

    selector = {
        'fields': ['Id', 'Name'],
        'predicates': [{
            'field': 'Name',
            'operator': 'EQUALS',
            'values': 'Models_KeywordHarvester_EM_' + str(campaign_id)
        }]
    }
    page = adgroup_service.get(selector)

    try:
        return page['entries'][0]['id']
    except:
        print('will create ad group')
        # adgroup_id = build_adgroup(campaign_id)
        # return adgroup_id
