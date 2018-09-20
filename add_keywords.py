def add_keyword(client, adgroup_id, keywords, match_type, brand_model):
    keyword_service = client.GetService('AdGroupCriterionService', version='v201806')

    keywords_upload = []
    for keyword in keywords:
        new_keyword = {
            'xsi_type': 'BiddableAdGroupCriterion',
            'adGroupId': adgroup_id,
            'criterion': {
                'xsi_type': 'Keyword',
                'matchType': match_type,
                'text': keyword
            },
            'finalUrls': {
                'urls': ['https://hey.car/gebrauchtwagen/{}/{}'.format(brand_model['make'], brand_model['model'])]
            }
        }
        keywords_upload.append(new_keyword)

    operations = []

    for i in keywords_upload:
        operations.append(
            {
                'operator': 'ADD',
                'operand': i
            }
        )

    keyword_service.mutate(operations)
