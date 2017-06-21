
Example query for notes service:

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

