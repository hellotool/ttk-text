from ttk_text._utils import parse_padding


class TestParsePadding:
    def test_parse_tuple_left(self):
        result = parse_padding(5)
        assert result is not None
        assert result.to_padx() == (5, 5)
        assert result.to_pady() == (5, 5)

    def test_parse_tuple_left_top(self):
        result = parse_padding((5, 10))
        assert result is not None
        assert result.to_padx() == (5, 5)
        assert result.to_pady() == (10, 10)

    def test_parse_tuple_left_top_right_bottom(self):
        result = parse_padding((1, 2, 3, 4))
        assert result is not None
        assert result.to_padx() == (1, 3)
        assert result.to_pady() == (2, 4)

    def test_parse_string_left(self):
        result5p = parse_padding("5p")
        assert result5p is not None
        assert result5p.to_padx() == ("5p", "5p")
        assert result5p.to_pady() == ("5p", "5p")

    def test_parse_string_left_top(self):
        result5p10p = parse_padding("5p 10p")
        assert result5p10p is not None
        assert result5p10p.to_padx() == ("5p", "5p")
        assert result5p10p.to_pady() == ("10p", "10p")

    def test_parse_string_left_top_right(self):
        result5p10p15p10p = parse_padding("5p 10p 15p")
        assert result5p10p15p10p is not None
        assert result5p10p15p10p.to_padx() == ("5p", "15p")
        assert result5p10p15p10p.to_pady() == ("10p", "10p")

    def test_parse_string_left_top_right_bottom(self):
        result5p10p15p20p = parse_padding("5p 10p 15p 20p")
        assert result5p10p15p20p is not None
        assert result5p10p15p20p.to_padx() == ("5p", "15p")
        assert result5p10p15p20p.to_pady() == ("10p", "20p")

    def test_parse_none(self):
        result = parse_padding(None)
        assert result is None
