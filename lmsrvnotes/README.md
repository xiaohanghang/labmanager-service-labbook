
Example query for notes/note service:

Create a Labbook:

mutation myMutation {
    createLabbook(name: "NotesLB", description: "Labbook to store notes")
    {labbook{name,id,username,description}}
}


Add notes:

mutation myMutation {
  createNote (lbname:"NotesLB", message:"First user defined note.", level: USER_MAJOR, linkedcommit: "123abcf", tags: ["user","major"]) {
    note {
      commit
      linkedcommit
      timestamp
      tags
      message
      lbname
      level
      freetext
      kvobjects
    }
  }
}

mutation myMutation {
  createNote (lbname:"NotesLB", message:"Second user defined note.", level: USER_MAJOR, linkedcommit: "123abcf", tags: ["user","major"]) {
    note {
      commit
      linkedcommit
      timestamp
      tags
      message
      lbname
      level
      freetext
      kvobjects
    }
  }
}


Query notes:

{
  notes(lbname: "NotesLB") {
    entries {
      commit
      linkedcommit
      level
      message
      tags
      timestamp
    }
    username
  }
}


Query Individual Note

{
  note(lbname: "NotesLB", id: "0f0c3df68eaad873402518e2f7186d9a2ed8ccad") {
    commit
    linkedcommit
    lbname
    message
    level
    timestamp
    freetext
    kvobjects
  }
}
