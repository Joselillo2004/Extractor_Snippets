from src.snippets.parser import parse_snippets, normalize_content

def test_parse_basic(tmp_path):
    content = (
        "# Title A\n"
        "print('a')\n\n"
        "# Title B\n"
        "x = 1\n"
    )
    p = tmp_path / 'ref.py'
    p.write_text(content, encoding='utf-8')

    snippets = parse_snippets(str(p), strict=True)
    assert len(snippets) == 2
    assert snippets[0].title == 'Title A'
    assert snippets[0].start_line == 1
    assert snippets[0].end_line == 2
    assert "print('a')" in snippets[0].content

    assert snippets[1].title == 'Title B'
    assert snippets[1].start_line == 4
    assert snippets[1].end_line == 5
    assert 'x = 1' in snippets[1].content


def test_normalize_content():
    # Test CRLF to LF conversion
    content_crlf = "print('hello')\r\nprint('world')\r\n"
    normalized = normalize_content(content_crlf)
    assert '\r' not in normalized
    assert normalized == "print('hello')\nprint('world')\n"
    
    # Test tab to spaces conversion
    content_tabs = "\tprint('indented')\n\t\tx = 1\n"
    normalized = normalize_content(content_tabs)
    assert '\t' not in normalized
    assert normalized == "    print('indented')\n        x = 1\n"
    
    # Test mixed problems
    content_mixed = "\tif True:\r\n\t\tprint('test')\r\n"
    normalized = normalize_content(content_mixed)
    assert '\t' not in normalized
    assert '\r' not in normalized
    assert normalized == "    if True:\n        print('test')\n"


def test_parse_with_problematic_formatting(tmp_path):
    """Test parsing file with tabs and CRLF like the real reference file"""
    content = (
        "# Test Snippet\r\n"
        "\r\n"
        "\tprint('hello')\r\n"
        "\tif True:\r\n"
        "\t\tprint('indented')\r\n"
    )
    p = tmp_path / 'ref_problematic.py'
    p.write_bytes(content.encode('utf-8'))
    
    snippets = parse_snippets(str(p), strict=True)
    assert len(snippets) == 1
    assert snippets[0].title == 'Test Snippet'
    
    # El contenido debe estar normalizado (tabs -> espacios, sin \r)
    content = snippets[0].content
    assert '\t' not in content
    assert '\r' not in content
    assert "    print('hello')" in content
    assert "        print('indented')" in content
