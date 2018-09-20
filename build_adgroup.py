def add_adgroup(client, campaign_id, adgroup_name):
    adgroup_service = client.GetService('AdGroupService', version='v201806')

    operations = [{
        'operator': 'ADD',
        'operand': {
            'campaignId': campaign_id,
            'name': adgroup_name,
            'status': 'PAUSED',  #'ENABLED'
            'trackingUrlTemplate': '{lpurl}?gLocationId={loc_physical_ms}&cid={campaignid}&adid={creative}&agid={adgroupid}&kw={keyword}&mt={matchtype}',
            'biddingStrategyConfiguration': {
                'bids': [
                    {
                        'xsi_type': 'CpcBid',
                        'bid': {
                            'microAmount': '500000'
                        }
                    }
                ]
            },
            'settings': [
                {
                    'xsi_type': 'TargetingSetting',
                    'details': [
                        {
                            'xsi_type': 'TargetingSettingDetail',
                            'criterionTypeGroup': 'USER_INTEREST_AND_LIST',
                            'targetAll': 'true' #true= bid only(observation)
                        }
                        ]
                }
            ]
        }
    }]

    new_adgroup_id = adgroup_service.mutate(operations)['value'][0]['id']
    return new_adgroup_id
