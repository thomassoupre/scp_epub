import unittest
from parameterized import parameterized
import bs4

import process.process_page
from constants import constants

class TestProcessPage(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def create_soup(self, html):
        return bs4.BeautifulSoup(html, "html.parser")

    @parameterized.expand([
        [
            'simple page content',
            '<html><head/><body>outside<div id="page-content">inside</div></body>',
            '<div id="page-content">inside</div>'
        ],
        [
            'not found',
            '<html><head/><body>outside</body>',
            'None'
        ],
    ])
    def test_get_page_content(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_page_content_id = 'page-content'

        # Act
        actual_output = process.process_page.get_page_content(expected_html_string, page_content_id=expected_page_content_id)

        # Assert
        self.assertEqual(expected_output_string, str(actual_output))


class TestProcessContentFunctions(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def create_soup(self, html):
        return bs4.BeautifulSoup(html, "html.parser")

    @parameterized.expand([
        [
            'nothing to remove',
            '<div class="qux">asdf</div>',
            '<div class="qux">asdf</div>'
        ],
        [
            'complete removal',
            '<div class="foo">asdf</div>',
            ''
        ],
        [
            'nested',
            'outside<div class="foo">qwq<div class="bar">asdf</div>qwrq</div>outside',
            'outsideoutside'
        ],
        [
            'reverse nested',
            'outside<div class="bar">qwq<div class="foo">asdf</div>qwrq</div>outside',
            'outsideoutside'
        ],
    ])
    def test_remove_by_class(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_classses_to_remove = [
            'foo',
            'bar'
        ]

        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.remove_classes(expected_content, classes_to_remove=expected_classses_to_remove)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

    @parameterized.expand([
        [
            'nothing to remove',
            '<a href="foobar">asdf</a>',
            '<a href="foobar">asdf</a>'
        ],
        [
            'complete removal',
            '<img></img>',
            ''
        ],
        [
            'simple removal',
            'outside<img src="foo.png" class="bar"></img>outside',
            'outsideoutside'
        ],
        [
            'singletag',
            'outside<img src="foo.png" class="bar"/>outside',
            'outsideoutside'
        ],
    ])
    def test_remove_by_tags(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_tags_to_remove = [
            'img'
        ]

        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.remove_tags(expected_content, tags_to_remove=expected_tags_to_remove)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

    @parameterized.expand([
        [
            'scp-047',
            '''outside<div class="collapsible-block"><div class="collapsible-block-folded"><a class="collapsible-block-link" href="javascript:;">&gt; Show details</a></div><div class="collapsible-block-unfolded" style="display:none"><div class="collapsible-block-unfolded-link"><a class="collapsible-block-link" href="javascript:;">&lt; Hide details</a></div><div class="collapsible-block-content"><ul><li><strong>Pathogenicity:</strong> Severe skin colonisation around sebaceous glands. Modification of skin pH to levels that become toxic to skin cells. Massive inflammation and immune cell infiltration. Eventual breakdown of skin structure leading to sepsis.</li><li><strong>Transmission:</strong> Transmitted by skin-to-skin contact. Can remain active on inorganic surfaces for up to five hours.</li><li><strong>Lethality:</strong> Approximately 40% mortality rate. Runs its course in 2-6 weeks. Very visible symptoms within 5-10 hours; contagious within 2-5 hours.</li><li><strong>Handling:</strong> As soon as visible symptoms form, victims must be quarantined. Deceased victims should be incinerated.</li></ul></div></div></div>''',
            '''outside<div class="collapsible"><p class="collapsible-title">&gt; Show details</p><ul><li><strong>Pathogenicity:</strong> Severe skin colonisation around sebaceous glands. Modification of skin pH to levels that become toxic to skin cells. Massive inflammation and immune cell infiltration. Eventual breakdown of skin structure leading to sepsis.</li><li><strong>Transmission:</strong> Transmitted by skin-to-skin contact. Can remain active on inorganic surfaces for up to five hours.</li><li><strong>Lethality:</strong> Approximately 40% mortality rate. Runs its course in 2-6 weeks. Very visible symptoms within 5-10 hours; contagious within 2-5 hours.</li><li><strong>Handling:</strong> As soon as visible symptoms form, victims must be quarantined. Deceased victims should be incinerated.</li></ul></div>'''
        ],
    ])
    def test_unwrap_collapsible_blocks(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.unwrap_collapsible_blocks(expected_content)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

    @parameterized.expand([
        [
            'simple',
            '''outside<blockquote><p>I love peace. I'd kill to preserve it</p></blockquote>''',
            '''outside<div class="quote"><p>I love peace. I'd kill to preserve it</p></div>'''
        ],
    ])
    def test_divify_blockquotes(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.divify_blockquotes(expected_content)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

    @parameterized.expand([
        [
            'two with nested div',
            '''<div id="wiki-tabview-03edd57ee60acc9ffdcd1050bfe0a7c2" class="yui-navset"><ul class="yui-nav"><li class="selected"><a href="javascript:;"><em>Effect 1509-1</em></a></li><li><a href="javascript:;"><em>Effect 1509-2</em></a></li></ul><div class="yui-content"><div id="wiki-tab-0-0"><div class="inner-div" style="width:300px;"><p>A specimen.</p></div><p>Effect 1509-1 typically.</p></div><div id="wiki-tab-0-1" style="display:none"><p>Effect SCP-1509-2 occurs.</p></div></div></div>''',
            '''<div class="tabview"><div class="tabview-tab"><p class="tab-title">Effect 1509-1</p><div class="inner-div" style="width:300px;"><p>A specimen.</p></div><p>Effect 1509-1 typically.</p></div><div class="tabview-tab"><p class="tab-title">Effect 1509-2</p><p>Effect SCP-1509-2 occurs.</p></div></div>'''
        ],
    ])
    def test_unwrap_navset(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.unwrap_yui_navset(expected_content)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

    @parameterized.expand([
        [
            'no links',
            '''asdf''',
            '''asdf'''
        ],
        [
            'non-href anchors',
            '''asdf<a>asdf</a>asdf<a name="asdf">asdf</a>''',
            '''asdf<a>asdf</a>asdf<a name="asdf">asdf</a>'''
        ],
        [
            'expanded internal link',
            '''<p>This is by <a href="http://scp-wiki.net/scp-3281">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>''',
            '''<p>This is by <a href="scp-3281.xhtml">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>'''
        ],
        [
            'other internal link',
            '''<p>This is by <a href="http://scp-wiki.net/scp-1234">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>''',
            '''<p>This is by <a href="scp-1234.xhtml">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>'''
        ],
        [
            'implicit internal link',
            '''<p>This is by <a href="/scp-3281">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>''',
            '''<p>This is by <a href="scp-3281.xhtml">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>'''
        ],
        [
            'external link',
            '''<p>This is by <a href="http://wikipedia.org/scp-3281">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>''',
            '''<p>This is by Autonomic (AARS821) RAISA. <strong>AAR</strong></p>'''
        ],
        [
            'multiple links',
            '''<p>This is by <a href="/scp-3281">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>asdf<p>This is by <a href="http://scp-wiki.net/scp-3281">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p><p>This is by <a href="http://wikipedia.org/scp-3281">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>''',
            '''<p>This is by <a href="scp-3281.xhtml">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p>asdf<p>This is by <a href="scp-3281.xhtml">Autonomic (AARS821)</a> RAISA. <strong>AAR</strong></p><p>This is by Autonomic (AARS821) RAISA. <strong>AAR</strong></p>'''
        ],
        [
            'not in book',
            '''<a href="http://scp-wiki.net/scp-11111">asdf</a>''',
            '''asdf'''
        ],
        [
            'not in book, implicit',
            '''<a href="/scp-11111">asdf</a>''',
            '''asdf'''
        ],
    ])
    def test_fix_links(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_url_allow_list = ['scp-3281', 'scp-1234']

        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.fix_links(expected_content, url_allow_list=expected_url_allow_list)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

    @parameterized.expand([
        [
            'no links',
            '''asdf''',
            '''asdf'''
        ],
        [
            'non-href anchors',
            '''asdf<a>asdf</a>asdf<a name="asdf">asdf</a>''',
            '''asdf<a>asdf</a>asdf<a name="asdf">asdf</a>'''
        ],
        [
            'not in book, implicit',
            '''<a href="/scp-11111">asdf</a>''',
            '''<a href="scp-11111.xhtml">asdf</a>'''
        ],
    ])
    def test_fix_links_no_whitelist(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_url_allow_list = None

        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.fix_links(expected_content, url_allow_list=expected_url_allow_list)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

    @parameterized.expand([
        [
            'simple add title',
            '''asdf''',
            '''<p class="page-title">Hi there!</p>asdf'''
        ],
        [
            'some other tags',
            '''<div class="foo">asdf</div>''',
            '''<p class="page-title">Hi there!</p><div class="foo">asdf</div>'''
        ]
    ])
    def test_add_title(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_title = 'Hi there!'

        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.add_title(expected_content, expected_title)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)

    @parameterized.expand([
        [
            'just the noteref',
            '''<sup class="footnoteref"><a id="footnoteref-1"href="javascript:;" class="footnoteref"onclick="WIKIDOT.page.utils.scrollToReference('footnote-1')">1</a></sup>''',
            '''<sup class="footnoteref"><a epub:type="noteref" href="#footnote-1" id="footnoteref-1">1</a></sup>'''
        ],
        [
            'just the footnote',
            '''<div class="footnote-footer" id="footnote-1"><a href="javascript:;"onclick="WIKIDOT.page.utils.scrollToReference('footnoteref-1')">1</a>. Even Grandma!</div>''',
            '''<div class="footnote-footer" epub:type="footnote" id="footnote-1"><a href="#footnoteref-1">1</a>. Even Grandma!</div>'''
        ],
        [
            'noterefs and footnotes',
            '''<p><strong>Special Containment Procedures:</strong> SCP-1-800-J can be easily and safely stored anywhere in your home! SCP-1-800-J can be used safely by any member of the family<sup class="footnoteref"><a id="footnoteref-1" href="javascript:;" class="footnoteref" onclick="WIKIDOT.page.utils.scrollToReference('footnote-1')">1</a></sup>! No stains! No mess! No permanent physical or mental trauma!</p> <p>Companies like Marshall, Carter, and Dark Ltd. and Dr. Wondertainment would charge you FORTUNES for similar products. But SCP-1-800-J is only $19.99! That's right! SCP-1-800-J is only $19.99<sup class="footnoteref"><a id="footnoteref-2" href="javascript:;" class="footnoteref" onclick="WIKIDOT.page.utils.scrollToReference('footnote-2')">2</a></sup>!</p> <div class="footnotes-footer"> <div class="title">Footnotes</div> <div class="footnote-footer" id="footnote-1"><a href="javascript:;" onclick="WIKIDOT.page.utils.scrollToReference('footnoteref-1')">1</a>. Even Grandma!</div> <div class="footnote-footer" id="footnote-2"><a href="javascript:;" onclick="WIKIDOT.page.utils.scrollToReference('footnoteref-2')">2</a>. Plus shipping and handling</div> </div>''',
            '''<p><strong>Special Containment Procedures:</strong> SCP-1-800-J can be easily and safely stored anywhere in your home! SCP-1-800-J can be used safely by any member of the family<sup class="footnoteref"><a epub:type="noteref" href="#footnote-1" id="footnoteref-1">1</a></sup>! No stains! No mess! No permanent physical or mental trauma!</p> <p>Companies like Marshall, Carter, and Dark Ltd. and Dr. Wondertainment would charge you FORTUNES for similar products. But SCP-1-800-J is only $19.99! That's right! SCP-1-800-J is only $19.99<sup class="footnoteref"><a epub:type="noteref" href="#footnote-2" id="footnoteref-2">2</a></sup>!</p> <div class="footnotes-footer"> <div class="title">Footnotes</div> <div class="footnote-footer" epub:type="footnote" id="footnote-1"><a href="#footnoteref-1">1</a>. Even Grandma!</div> <div class="footnote-footer" epub:type="footnote" id="footnote-2"><a href="#footnoteref-2">2</a>. Plus shipping and handling</div> </div>'''
        ],
    ])
    def test_fix_footnotes(self, reason, expected_html_string, expected_output_string):
        # Arrange
        expected_content = self.create_soup(expected_html_string)
        expected_output = None

        # Act
        actual_output = process.process_page.fix_footnotes(expected_content)

        # Assert
        self.assertEqual(expected_output_string, str(expected_content))
        self.assertEqual(expected_output, actual_output)