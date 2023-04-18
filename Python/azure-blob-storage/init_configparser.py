import configparser
config = configparser.ConfigParser()
config['azure-storage'] = {'storage_key': 'storagekey',
                        'storage_url': 'https://<account>.blob.core.windows.net',
                        'container_name': 'my-container'}

with open('example.ini', 'w') as configfile:
  config.write(configfile)