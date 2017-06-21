
Example query for notes/note service:

Queries:


Notes
{
  notes(name: "NewLabBook") {
    entries {
      id
      loglevel
      message
      tags
      timestamp
    }
    username
  }
}


Note

{
  note(lbname: "NewLabBook", id: "7") {
    id
    lbname
    kvobjects
    message
    loglevel
    timestamp
    freetext
    
  }
}


