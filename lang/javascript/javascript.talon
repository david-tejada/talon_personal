code.language: javascript
code.language: typescript
code.language: javascriptreact
code.language: typescriptreact
-

make const: "const "
const <user.text>: user.insert_snippet("const {user.camel(text)} = $0;")
make let: "let "
let <user.text>: user.insert_snippet("let {user.camel(text)} = $0;")

is instance of: " instanceof "
type of <user.text> is <user.text>: "typeof {user.camel(text_1)} === \"{text_2}\""

is null else: " ?? "

dolly var: user.insert_snippet("${{$0}}")

console log: user.insert_snippet("console.log($0)")
console error: user.insert_snippet("console.error($0)")
console warn: user.insert_snippet("console.warn($0)")
console debug: "console.debug()"
console trace: "console.trace()"
console time: "console.time()"
console time end: "console.timeEnd()"

make new <user.text>: user.insert_snippet("new {user.camel(text)}($0)")
throw new error: user.insert_snippet("throw new Error(\"$0\")")

blocker:
  edit.line_end()
  " "
  user.code_block()

make await: "await "
make async: "async "
make export: "export "

make block lambda: user.insert_snippet("() => {{$0}}")

function <user.text>:
  user.insert_snippet_by_name_with_phrase("functionDeclaration", text)

async function <user.text>:
  user.insert_snippet_by_name_with_phrase("asyncFunctionDeclaration", text)

for <user.text> of <user.text>:
  user.insert_snippet("for (const {user.camel(text_1)} of {user.camel(text_2)}) {{\n\t$body\n}}")

j s dock:
    "/**"
    sleep(100ms)
    key(tab)