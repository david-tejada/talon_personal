code.language: javascriptreact
code.language: typescriptreact
-
use state <user.text>:
    user.insert_snippet("const [{user.camel(text)}, set{user.pascal(text)}] = useState($0)")

use effect: user.insert_snippet_by_name("reactUseState")