
### Example query for notes/note service:

Create a Labbook:

```
mutation myMutation {
  createLabbook(name: "notes-test", description: "Labbook to store notes") {
    labbook {
      name
      id
      description
    }
  }
}

```

Add note:

```
mutation CreateNote {
  createNote(labbookName: "notes-test",
    message: "8th user defined note.",
    level: USER_MINOR,
    linkedCommit: "123abcf",
    tags: ["user", "minor"],
    freeText: "Lots of text here more and more text (8).",
    objects: [{key: "objectkey1", objectType: "PNG", value: "2new0x7FABC374FX"}]) {
    note {
      labbookName
      commit
      linkedCommit
      author
      message
      level
      tags
      timestamp
      freeText
      objects {
        key
        objectType
        value
      }
    }
  }
}

```

Query note summaries:

```
{
  noteSummaries(labbookName: "notes-test") {
    entries {
      labbookName
      commit
      linkedCommit
      author
      level
      message
      tags
      timestamp
    }
  }
}
```


Query Individual Note

```
{
  note(labbookName: "notes-test", commit: "44fb8351e50c94fce248b9b0051cbf0ecd412727") {
    labbookName
    commit
    linkedCommit
    author
    message
    level
    tags
    timestamp
    freeText
    objects {
      key
      objectType
      value
    }
  }
}
```

