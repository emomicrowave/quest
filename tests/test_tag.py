from context import kobold
from kobold.tag import Tag, parse_tag


class TestTagParse:
    def test_parse_utag(self):
        tag = parse_tag("due:tomorrow")
        assert tag == Tag("due", "tomorrow")
        assert str(tag) == "due:tomorrow"

    def test_parse_ctag(self):
        tag_text = "@home"
        tag = parse_tag(tag_text)
        assert tag == Tag("context", "home")
        assert str(tag) == tag_text

    def test_parse_ptag(self):
        tag_text = "+kobold"
        tag = parse_tag(tag_text)
        assert tag == Tag("project", "kobold")
        assert str(tag) == tag_text

    def test_parse_notag(self):
        tag_text = "not_a_tag"
        tag = parse_tag(tag_text)
        assert tag == Tag("word", "not_a_tag")
        assert str(tag) == tag_text

    def test_parse_with_default(self):
        tag = parse_tag("not_a_tag", "none")
        assert tag == "none"
