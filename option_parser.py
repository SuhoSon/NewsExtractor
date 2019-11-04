from optparse import OptionParser

option_pages = {'name': ('-p', '--pages'),
                'help': "The number of pages to analyze. If no option, all pages are analyzed.",
                'action': 'store'
                }

option_start = {'name': ('-s', '--start'),
                'help': "The start date for analyze. If no option, analyze from a year ago.",
                'action': 'store'
                }

option_end = {'name': ('-e', '--end'),
              'help': "The end date for analyze. If no option, It is analyzed to today.",
              'action': 'store'
              }

option_saved_crawler = {'name': ('-c', '--crawler'),
                        'help': "The saved file for crawling. If no option, make new file.",
                        'action': 'store'
                        }

option_saved_counter = {'name': ('-t', '--counter'),
                        'help': "The saved file for counting. If no option, make new file.",
                        'action': 'store'
                        }

class Option_Parser:
    def __init__(self):
        self.parser = OptionParser()

    def start(self):
        options = [option_pages, option_start, option_end, option_saved_crawler, option_saved_counter]

        for option in options:
            param = option['name']
            del option['name']
            self.parser.add_option(*param, **option)

        options, arguments = self.parser.parse_args()

        options = vars(options)
        for key, value in options.items():
            if value is None:
                continue
            if (key is not 'c' or not 't') and (key is not 'crawler' or not 'counter'):
                options[key] = int(value.strip().replace(".", "").replace("-", ""))

        return options
