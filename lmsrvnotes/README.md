
Example query for notes/note service:

Create a Labbook:

mutation myMutation {
    createLabbook(name: "NotesLB", description: "Labbook to store notes")
    {labbook{name,id,username,description}}
}


Add notes:

mutation myMutation {
  createNote(lbname: "NotesLB", message: "8th user defined note.", 
                level: USER_MINOR, linkedcommit: "123abcf", tags: ["user", "minor"], 
                freetext: "Lots of text here more and more text (8).", 
                objects: [{key: "objectkey1", objecttype: "PNG", value: "2new0x7FABC374FX"}, 
                            {key: "objectkey2", objecttype: "CSV", value: "a,b,c"}]) {
    note {
      lbname
      commit
      linkedcommit
      author
      message
      level
      tags
      timestamp
      freetext
      objects {
        key
        objecttype
        value
      }
    }
  }
}


Query notes:

{
  notes(lbname: "NotesLB") {
    entries {
      lbname
      commit
      linkedcommit
      author
      level
      message
      tags
      timestamp
    }
  }
}



Query Individual Note

{
  note(lbname: "NotesLB", commit: "37579de691c3589ca939eec9700dbd41fbf21f4c") {
    lbname
    commit
    linkedcommit
    author
    message
    level
    tags
    timestamp
    freetext
    objects {
      key
      objecttype
      value
    }
  }
}


