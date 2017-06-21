
Example query for notes/note service:

Queries:

{
  notes(name: "NewLabBook") {
    name
    username
    entries {
      id,
      message,
      tags,
      timestamp
    }
  }
}



{
  note(name: "NewLabBook", id: "7") {
    freetext
    kvobjects
    summary {
      message,
      loglevel
    }
  }
}
