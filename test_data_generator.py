# Test data generator

import os

def main():
    """Test data generator"""
    PATH = os.path.join(os.path.dirname(__file__), 'test_data/data/snippets/ma1ex.Html/')

    for i in range(1, 50):
        data = f'''name=gen_test_{i}
id=gen_test_{i}
lex=HTML,HTML_,PHP
text=
<div class="generator">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</div>
'''
        file_name = PATH + 'snippet_gen_' + str(i) + '.synw-snippet'
        with open(file_name, 'w', encoding='utf-8') as test_snippet:
            test_snippet.write(data)


if __name__ == "__main__":
    main()