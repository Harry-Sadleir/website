import unittest
import urllib.error
from unittest import mock

from woof_site import github_activity, helpers

FEED = b"""<?xml version="1.0"?>
<rss version="2.0"><channel><title>t</title>
<item><title>How random is random?</title><link>https://example.com/p/1</link>
<description><![CDATA[<p><img src="https://example.com/a.png">Some text</p>]]></description></item>
</channel></rss>"""


class CacheTests(unittest.TestCase):
    def setUp(self):
        github_activity._cache.update(ts=0, items=[])
        helpers._cache.update(ts=0.0, posts=[])

    def test_empty_github_result_is_cached(self):
        with mock.patch.object(github_activity, "_request", return_value=[]) as call:
            github_activity.get_github_activity()
            github_activity.get_github_activity()
        self.assertEqual(call.call_count, 1)

    def test_github_error_is_not_retried_on_every_request(self):
        with mock.patch.object(github_activity, "_request", side_effect=urllib.error.URLError("down")) as call:
            self.assertEqual(github_activity.get_github_activity(), [])
            self.assertEqual(github_activity.get_github_activity(), [])
        self.assertEqual(call.call_count, 1)

    def test_substack_failure_is_not_retried_on_every_request(self):
        with mock.patch.object(helpers.requests, "get", side_effect=helpers.requests.Timeout) as call:
            self.assertEqual(helpers.fetch_recent_from_substack(), [])
            self.assertEqual(helpers.fetch_recent_from_substack(), [])
        self.assertEqual(call.call_count, 1)

    def test_substack_feed_is_parsed_and_cached(self):
        response = mock.Mock(content=FEED)
        with mock.patch.object(helpers.requests, "get", return_value=response) as call:
            posts = helpers.fetch_recent_from_substack()
            helpers.fetch_recent_from_substack()
        self.assertEqual(call.call_count, 1)
        self.assertEqual(posts[0]["title"], "How random is random?")
        self.assertEqual(posts[0]["image"], "https://example.com/a.png")
        self.assertEqual(posts[0]["desc"], "Some text")


if __name__ == "__main__":
    unittest.main()
