from googleads import adwords
import pandas as pd

def get_accounts(client):
    managed_customer_service = client.GetService('ManagedCustomerService', version='v201809')
    selector = {
                'fields': ['Name','CustomerId'],
                'predicates': [
                    {
                        'field': 'Name',
                        'operator': 'CONTAINS',
                        'values': 'DSA'
                    }
                ]
    }
    accounts = managed_customer_service.get(selector)
    return accounts

columns = ['AccountDescriptiveName', 'CampaignName','AdGroupName', 'Query', 'CategoryPaths','Url' , 'Impressions', 'Clicks', 'Conversions', 'Cost']
def get_data(client):
    accounts = get_accounts(client)
    report_downloader = client.GetReportDownloader(version='v201809')
    try:
        with open('sqr_dsa_raw.csv','wb') as a:
            for entry in accounts['links']:
                client.client_customer_id= entry['clientCustomerId']
                report = {
                      'reportName': 'KEYWORDLESS_QUERY_REPORT',
                      'dateRangeType': 'LAST_7_DAYS',
                      'reportType': 'KEYWORDLESS_QUERY_REPORT',
                      'downloadFormat': 'CSV',
                      'selector': {
                          'fields': columns,
                          'predicates': [
                              {
                                  'field': 'Impressions',
                                  'operator': 'GREATER_THAN',
                                  'values': '10'
                              },
                              {
                                  'field': 'Conversions',
                                  'operator': 'GREATER_THAN',
                                  'values': '0'
                              }
                          ]
                       },

                }
                report_downloader.DownloadReport(report,a)

    except Exception:
        print('error getting report')


def remove_row (r):
    try:
        if r in ('Total', 'Account'):
            return 'yes'
        elif 'SEARCH_QUERY_' in r:
            return 'yes'
        else:
            return 'no'
    except Exception:
        print(r)
        print('error removing row')

def clean_file():
    df = pd.read_csv('sqr_dsa_raw.csv')
    df.reset_index(inplace=True)
    df.columns = columns
    df['remove'] = df['AccountDescriptiveName'].apply(lambda x: remove_row(x))
    #removed unnecessary rows
    df.drop(df[df['remove'] == 'yes'].index, inplace=True)
    df['Cost'] = df['Cost'].apply(lambda x: float(x)/1000000)
    df['Impressions'] = df['Impressions'].apply(lambda x: float(x))
    df['Clicks'] = df['Clicks'].apply(lambda x: float(x))
    df.drop(['remove'], axis=1, inplace=True)
    df.to_csv('sqr_dsa_clean.csv')

def make(url):
    word = url.split('/')[-2]
    if (word == 'gebrauchtwagen'):
        return url.split('/')[-1]
    else:
        return word

def model(url):
    return url.split('/')[-1]

def get_account(make, model):
    if (make == model):
        return 'Makes'
    elif (model == ''):
        return 'Unknown'
    else:
        return 'Models'

def cap_all(word):
    spl = word.split(' ')
    cap = [w.capitalize() for w in spl]
    output = ''
    for a in cap:
        output += a
    return output

def get_campaign(account, make, model):
    make_clean = make.title().replace(' ', '').replace('-', ' ')
    model_clean = model.title().replace(' ', '').replace('-', ' ')

    if (account == 'Models'):
        return 'Models_' + cap_all(make_clean) + cap_all(model_clean) + '_EM'
    elif (account == 'Makes'):
        return 'Makes_' + cap_all(make_clean) + '_EM'
    else:
        return 'Unknown'

def get_terms():
    adwords_client = adwords.AdWordsClient.LoadFromStorage('../adwords_api/googleads.yaml')
    get_data(adwords_client)
    clean_file()
    df = pd.read_csv('sqr_dsa_clean.csv')
    df['make'] = df['Url'].apply(lambda x: make(x))
    df['model'] = df['Url'].apply(lambda x: model(x))
    df['dest_account'] = df.apply(lambda row: get_account(row['make'], row['model']), axis=1)
    df['dest_campaign'] = df.apply(lambda row: get_campaign(row['dest_account'], row['make'], row['model']), axis=1)
    df['dest_adgroup'] = 'DSA_Harvesting'
    converting_terms = df[['Query', 'make', 'model', 'Impressions', 'Conversions', 'dest_account', 'dest_campaign', 'Url']][df['Conversions'] > 0].groupby(['Query', 'make', 'model', 'dest_account', 'dest_campaign', 'Url']).sum().reset_index()
    return converting_terms[(converting_terms['dest_account'] == 'Models') & (converting_terms['Impressions'] > 10)].sort_values('Conversions', ascending=False)

if __name__ == '__main__':
    get_terms()
