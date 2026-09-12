code.language: javascript
code.language: typescript
code.language: javascriptreact
code.language: typescriptreact
-

make const: "const "
const <user.text>: "const {user.camel(text)} = "
make let: "let "
let <user.text>: user.insert_snippet("let {user.camel(text)} = ")

is instance of: " instanceof "
type of <user.text> is <user.text>: "typeof {user.camel(text_1)} === \"{text_2}\""

is null else: " ?? "
is undefined: user.insert_snippet(" === undefined")
is not undefined: user.insert_snippet(" !== undefined")

dolly var: user.insert_snippet("${{$0}}")

console log: user.insert_snippet("console.log($0)")
console error: user.insert_snippet("console.error($0)")
console warn: user.insert_snippet("console.warn($0)")
console debug: "console.debug()"
console trace: "console.trace()"
console time: "console.time()"
console time end: "console.timeEnd()"

make new <user.text>: user.insert_snippet("new {user.pascal(text)}($0)")
throw new [<user.text>] error:
  user.insert_snippet("throw new {user.pascal(text or '')}Error(\"$0\")")

blocker:
  edit.line_end()
  user.insert_snippet(" {{$0}}")
  key(enter)

make async: "async "

make await: "await "
await <user.text>: user.insert_snippet("await {user.camel(text)}($0)")

make export: "export "

block lambda: user.insert_snippet("($1) => {{$0}}")

function <user.text>:
  user.insert_snippet_by_name_with_phrase("functionDeclaration", text)

async function <user.text>:
  user.insert_snippet_by_name_with_phrase("asyncFunctionDeclaration", text)

for <user.text> of <user.text>:
  user.insert_snippet("for (const {user.camel(text_1)} of {user.camel(text_2)}) {{\n\t$0\n}}")

for <user.text> in <user.text>:
  user.insert_snippet("for (const {user.camel(text_1)} in {user.camel(text_2)}) {{\n\t$0\n}}")

for loop:
  user.insert_snippet("for (let i = 0; i < $1; i++) {{\n\t$0\n}}")

j s dock:
  "/**"
  sleep(100ms)
  key(tab)

# React. I place this here instead of in javascriptreact.talon because I want
# them active for hook files which are not jsx.
use state <user.text>:
  user.insert_snippet("const [{user.camel(text)}, set{user.pascal(text)}] = useState($0)")

use effect: user.insert_snippet_by_name("reactUseEffect")
