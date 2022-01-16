import csv as csv
from urllib.parse import urlparse
import requests

# MAJOR OVERALL NOTE
# This solution is NOT FAST and per the instructions is NOT OPTIMIZED for speed.
# My next step would be to optimize so it runs faster.

class Transformer:
    # this is a simple url parser that determines if the URL
    # provided is valid, then uses the requests library to return
    # the actual domain
    def url_parser(self, content_url):
        # some of the links provided are to content servers or files
        # these links are not valid and cannot be parsed as URLs
        # the first if statement looks for a valid url that contains http
        # this condition also applies to https
        if 'http' not in content_url:
            return ['Invalid URL', 'Invalid URL']
        else:
            # occasionally the link provided is a valid URL but there is no
            # response from the site. This try/except block handles requests
            # that time out.
            try:
                r = requests.get(content_url)
                return [urlparse(content_url).netloc, urlparse(r.url).netloc]
            except:
                return [urlparse(content_url).netloc, 'Network request failed']

    # test case for direct url
    def standard_url_test(self):
        contenturl = 'https://www.nytimes.com/2019/06/07/business/economy/age-discrimination-jobs-hiring.html'

        if self.url_parser(contenturl)[0] == 'www.nytimes.com' and self.url_parser(contenturl)[1] == 'www.nytimes.com' :
            print('standard_url_test PASS')
        else:
            print('standard_url_test FAIL')
        return

    # test case for a url that redirects to another domain
    def redirect_url_test(self):
        contenturl = 'https://youtu.be/hq8UQvjXnRk'

        if self.url_parser(contenturl)[1] == 'www.youtube.com' and self.url_parser(contenturl)[0] == 'youtu.be':
            print('redirect_url_test PASS')
        else:
            print('redirect_url_test FAIL')
        return

    # test case for a URL that is invalid
    def invalid_url_test(self):
        contenturl = 'degreed://useruploadedvideo-d1ebec1b-4044-40e8-9b5f-7c816e777856'

        if self.url_parser(contenturl)[1] == 'Invalid URL':
            print('invalid_url_test PASS')
        else:
            print('invalid_url_test FAIL')
        return

    def transform_content_hostname(self, input_file, output_file):
        #datafile = 'Degreed_ExampleCompletions.csv'
        # result list to hold final array
        result = []

        # test call block
        self.standard_url_test()
        self.redirect_url_test()
        self.invalid_url_test()

        with open(input_file, newline='') as f:
            # read data into list object
            reader = csv.reader(f)
            # skip header line
            next(reader)

            for line in reader:
                userid, contentid, contenturl = line
                # to get the domain, call the url_parser function which will
                # determine the top level or redirected domain if the url is valid
                return_values = self.url_parser(contenturl)

                # add results to a list object
                result.append([userid, contentid, contenturl, return_values[0], return_values[1]])
                # since this script is not optimized for performance, it takes a while to run,
                # so I printed the output to see if it was still going or not
                print(userid, contentid, contenturl, return_values[0], return_values[1])

        # output result array to csv
        with open(output_file, 'w', newline='') as of:
            mywriter = csv.writer(of, delimiter=',')
            mywriter.writerows(result)