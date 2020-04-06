from context import kobold
from kobold.tag import Tag, parse_tag


class TestTagParse:
    def test_parse_utag(self):
        tag = parse_tag("due:tomorrow")
        assert tag == Tag("due", "tomorrow")
        assert str(tag) == "due:tomorrow"

    def test_parse_ctag(self):
        tag = parse_tag("@home")
        assert tag == Tag("context", "home")

    def test_parse_ptag(self):
        tag = parse_tag("+kobold")
        assert tag == Tag("project", "kobold")

    def test_parse_notag(self):
        tag = parse_tag("not_a_tag")
        assert tag == Tag("word", "not_a_tag")

    def test_parse_with_default(self):
        tag = parse_tag("not_a_tag", "none")
        assert tag == "none"
