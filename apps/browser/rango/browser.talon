tag: browser
-

storage sync get: 
  user.insert_snippet("await browser.storage.sync.get($0)")

storage sync set:
  user.insert_snippet("await browser.storage.sync.set($0)")

storage sync clear: "await browser.storage.sync.clear()"

storage sync get bytes in use:
  user.insert_snippet("await browser.storage.sync.getBytesInUse($0)")