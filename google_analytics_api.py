"""Python script fixing Ecommerce banks using Google Analytics API."""

import argparse
import sys

import ga # Python script in charge of filling the referral exclusion list

from apiclient.discovery import build
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from bs4 import BeautifulSoup
import json


def get_service(api_name, api_version, scope, client_secrets_path):
  """Get a service that communicates to a Google API.

  Args:
    api_name: string The name of the api to connect to.
    api_version: string The api version to connect to.
    scope: A list of strings representing the auth scopes to authorize for the
      connection.
    client_secrets_path: string A path to a valid client secrets file.

  Returns:
    A service that is connected to the specified API.
  """
  # Parse command-line arguments.
  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      parents=[tools.argparser])
  flags = parser.parse_args([])

  # Set up a Flow object to be used if we need to authenticate.
  flow = client.flow_from_clientsecrets(
      client_secrets_path, scope=scope,
      message=tools.message_if_missing(client_secrets_path))

  # Prepare credentials, and authorize HTTP object with them.
  # If the credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # credentials will get written back to a file.
  storage = file.Storage(api_name + '.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(flow, storage, flags)
  http = credentials.authorize(http=httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service


def get_url_analytics_referral_exclusion(service, id):
  # Use the Analytics service object to get the url analytics referral exclusion.

  # # Get a list of all Google Analytics accounts for the authorized user.
  # accounts = service.management().accounts().list().execute()

  views = service.management().profiles().list(accountId=id, webPropertyId='~all').execute()
  for item in views.get('items'):
      if item.get('starred') == True:
            url = 'https://analytics.google.com/analytics/web/?authuser=1#/'
            # Following line is different for each client
            url += 'a' + id + 'w' + item.get('internalWebPropertyId') + 'p' + item.get('id')
            url += '/admin/trackingreferral-exclusion-list/'
            # print(url)
            return url
  # print("Client name : starred, accountId, internalWebPropertyId, viewId")
  # print("%s : %s, %s, %s, %s" %(item.get('name'), item.get('starred'), id, item.get('internalWebPropertyId'), item.get('id')))

  return None

def fix_ecommerce_banks():
  # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/analytics.readonly']

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, 'client_secrets.json')
  if len(sys.argv) == 1:
      print('No accountId given')
      exit(0)
  for arg in sys.argv[1:]:
    print(type(arg))
    url = get_url_analytics_referral_exclusion(service, arg)
    ga.fill_referral_exclusion(url)

if __name__ == '__main__':
  fix_ecommerce_banks()
