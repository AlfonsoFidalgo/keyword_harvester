ad_template = {
    'headline1': ['BRAND MODEL Gebrauchtwagen',
                   'MODEL Gebrauchtwagen',
                   'BRAND Gebrauchtwagen',
                   'Top Gebrauchtwagen auf heycar'],
    'headline2': ['BRAND MODEL mit Garantie',
                   'MODEL mit Garantie',
                   'BRAND mit Garantie',
                   'Alle Autos mit Garantie'],
    'descriptions': ['Große Auswahl an Gebrauchtwagen von Top Händlern - keine unseriösen Angebote.',
                     'Hochwertige Gebrauchtwagen von Händlern gründlich geprüft. Jetzt in Ihrer Nähe',
                     'Gebrauchte mit max. 150.000 KM und 8 Jahren Lauﬂeistung. Qualitäts-geprüft']
}

def get_hl(make, model, headline):
    """
    headline needs to be headline1 or headline2
    """
    for headline in ad_template[headline]:
        hl = headline.replace('BRAND', make)
        hl = hl.replace('MODEL', model)
        if len(hl) < 31:
            return hl

def get_path(word, path):
    if ((len(word) > 15) and (path == 'path1')):
        return 'Gebrauchtwagen'
    elif ((len(word) > 15) and (path == 'path2')):
        return 'Garantie'
    else:
        return word

def find_make_display_name(brand_model):
    for make in brand_model['make_display_name']:
        if (make['key'] == brand_model['make']):
            return make['displayName']


def find_model_display_name(brand_model):
    for model in brand_model['model_display_name']:
        if (model['key'] == brand_model['model']):
            return model['displayName']

def add_adcopy(client, adgroup_id, brand_model):
    ad_service = client.GetService('AdGroupAdService', version='v201809')

    make = find_make_display_name(brand_model)
    if (make == None):
        make = brand_model['make']

    model = find_model_display_name(brand_model)
    if (model == None):
        model = brand_model['model'].split(',')[0]


    operations = []
    for description in ad_template['descriptions']:

        ad = {
                'operator': 'ADD',
                'operand': {
                    'xsi_type': 'AdGroupAd',
                    'adGroupId': adgroup_id,
                    'ad': {
                        'xsi_type': 'ExpandedTextAd',
                        'headlinePart1': get_hl(make, model, 'headline1'),
                        'headlinePart2': get_hl(make, model, 'headline2'),
                        'description': description,
                        'finalUrls': 'https://hey.car',
                        'path1': get_path(make, 'path1'),
                        'path2': get_path(model, 'path2')
                    }
                }
            }
        operations.append(ad)


    ads = ad_service.mutate(operations)
    return ads
