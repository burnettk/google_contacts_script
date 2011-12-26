#!/usr/bin/python
#
# Copyright (C) 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
# NOTE: This code has been modified by Kevin Burnett, December, 2011.


__author__ = 'api.jscudder (Jeffrey Scudder)'


import sys
import getopt
import getpass
import atom
import gdata.contacts.data
import gdata.contacts.client


class ContactsSample(object):
  """ContactsSample object demonstrates operations with the Contacts feed."""

  def __init__(self, email, password):
    """Constructor for the ContactsSample object.
    
    Takes an email and password corresponding to a gmail account to
    demonstrate the functionality of the Contacts feed.
    
    Args:
      email: [string] The e-mail address of the account to use for the sample.
      password: [string] The password corresponding to the account specified by
          the email parameter.
    
    Yields:
      A ContactsSample object used to run the sample demonstrating the
      functionality of the Contacts feed.
    """
    self.gd_client = gdata.contacts.client.ContactsClient(source='GoogleInc-ContactsPythonSample-1')
    self.gd_client.ClientLogin(email, password, self.gd_client.source)

  def PrintPaginatedFeed(self, feed, print_method):
    """ Print all pages of a paginated feed.
    
    This will iterate through a paginated feed, requesting each page and
    printing the entries contained therein.
    
    Args:
      feed: A gdata.contacts.ContactsFeed instance.
      print_method: The method which will be used to print each page of the
          feed. Must accept these two named arguments:
              feed: A gdata.contacts.ContactsFeed instance.
              ctr: [int] The number of entries in this feed previously
                  printed. This allows continuous entry numbers when paging
                  through a feed.
    """
    ctr = 0
    while feed:
      # Print contents of current feed
      ctr = print_method(feed=feed, ctr=ctr)
      # Prepare for next feed iteration
      next = feed.GetNextLink()
      feed = None
      if next:
        feed = self.gd_client.GetContacts(uri=next.href)

  def ListAllContacts(self, username):
    """Retrieves a list of contacts and displays name and primary email."""
    query = gdata.contacts.client.ContactsQuery()
    query.group = 'http://www.google.com/m8/feeds/groups/' + username + '%40gmail.com/base/6'
    query.max_results = 5000
    """feed = self.gd_client.GetContacts()"""
    feed = self.gd_client.GetContacts(q=query)
    self.PrintPaginatedFeed(feed, self.PrintContactsFeed)

  def PrintContactsFeed(self, feed, ctr):
    if not feed.entry:
      print '\nNo contacts in feed.\n'
      return 0
    entries = feed.entry
    entries = sorted(entries, key=lambda entry: entry.name.full_name.text)
    for i, entry in enumerate(entries):
      if not entry.name is None:
        full_name = entry.name.full_name is None and " " or entry.name.full_name.text
        """given_name = entry.name.given_name is None and " " or entry.name.given_name.text"""
        sys.stdout.write('\n' + full_name + ": ")
      else:
        print '\n%s %s (title)' % (ctr+i+1, entry.title.text)

      for phone in entry.phone_number:
        #if "mobile" in entry.phone_number[0].rel:
        #print phone.text + " "
        sys.stdout.write(phone.text + " ")

    return len(feed.entry) + ctr

  def Run(self, username):
    """Prompts the user to choose funtionality to be demonstrated."""
    self.ListAllContacts(username)
    return

def main():
  """Demonstrates use of the Contacts extension using the ContactsSample object."""
  # Parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['user=', 'pw='])
  except getopt.error, msg:
    print 'python contacts_example.py --user [username] --pw [password]'
    sys.exit(2)

  user = ''
  pw = ''
  # Process options
  for option, arg in opts:
    if option == '--user':
      user = arg
    elif option == '--pw':
      pw = arg

  while not user:
    print 'NOTE: Please run these tests only with a test account.'
    user = raw_input('Please enter your username: ')
  while not pw:
    pw = getpass.getpass()
    if not pw:
      print 'Password cannot be blank.'


  try:
    sample = ContactsSample(user, pw)
  except gdata.client.BadAuthentication:
    print 'Invalid user credentials given.'
    return

  sample.Run(user)


if __name__ == '__main__':
  main()
