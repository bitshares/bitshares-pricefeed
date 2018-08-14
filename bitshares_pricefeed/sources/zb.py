import requests
from . import FeedSource, _request_headers


class Zb(FeedSource):
    def _fetch(self):
        feed = {}
        url = "http://api.zb.com/data/v1/ticker?market={quote}_{base}"
        try:
            for base in self.bases:
                for quote in self.quotes:
                    if base == quote:
                        continue
                    response = requests.get(
                        url=url.format(base=base, quote=quote),
                        headers=_request_headers,
                        timeout=self.timeout)
                    result = response.json()
                    if "ticker" in result and \
                       "last" in result["ticker"] and \
                       "vol" in result["ticker"]:
                        self.add_rate(feed, base, quote, float(result["ticker"]["last"]), float(result["ticker"]["vol"]))
                    else:
                        print("\nFetched data from {0} is empty!".format(type(self).__name__))
                        continue
        except Exception as e:
            raise Exception("\nError fetching results from {1}! ({0})".format(str(e), type(self).__name__))
        return feed
