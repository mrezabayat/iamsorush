---
title: "Connect to Microsoft Access database with C# .Net core "
date: 2020-10-22T18:34:21+01:00
image: /images/bridge.jpg
thumbnail: /images/doorlock_tn.webp
tags: [".Net Core", "C Sharp", "Database"]
categories: "⋅Net"
summary: "I want to connect to an MS Access database with C# in .Net core. Therefore, I will be able to create, read, update, and delete (CRUD) records."
---

## Goal

I want to connect to an MS Access database with C# in .Net core. Therefore, I will be able to write queries to create, read, update, and delete (CRUD) records.

## OS driver

From experience, I would recommend run the web app on Windows rather than Linux. On Windows, the only driver needed to be installed is [MS Access Database Engine 2010](https://www.microsoft.com/en-gb/download/details.aspx?id=13255) or [MS Access Database Engine 2016](https://www.microsoft.com/en-us/download/details.aspx?id=54920). But for Linux, I couldn't find a free driver.

## Install Odbc connection

In visual studio, while your project is open, go to NuGet package manager:

*Tools ->  NuGet Package Manager -> Manage NuGet Packages for Solution*

Search for and install *System.Data.Odbc* package by Microsoft. My version is 4.7.

## Connection string 

Define the connection string as

```c#
ConnectionString = "Driver={Microsoft Access Driver (*.mdb, *.accdb)}; Dbq=C:\\Users\\sorush\\Documents\\nameOfDatabase.accdb; Uid = Admin; Pwd =; ",
```
Change my database address to yours. Leave the rest as it is.

## Write a query

The easiest way to write a query is to use the MS Access *Query Design* tool. Copy the query and
edit the variables in C# like:

```c#
public string GetBookDeleteQuery(int id)
{
  var query = $@"DELETE FROM Books WHERE BookID={id};";
  return query;
}
```

## Non-return query

The method below can be used for queries that no data is pulled like create, update, and delete.

```c#
public void RunQuery(string query)
{
    OdbcCommand command = new OdbcCommand(query);

    using (OdbcConnection connection = new OdbcConnection(ConnectionString))
    {
        command.Connection = connection;
        connection.Open();
        var reader = command.ExecuteReader();
    }
}
```

## Data return query

The sample below can be used when multiple rows of a table are pulled from the MS Access database.

```c#
public List<Person> GetPeople(string query)
{
  var people = new List<Person>();
  OdbcCommand command = new OdbcCommand(query);

  using (OdbcConnection connection = new OdbcConnection(ConnectionString))
  {
      command.Connection = connection;
      connection.Open();
      using (var reader = command.ExecuteReader())
      {
          while (reader.Read())
          {
              var person = new Person();
              person.Name = reader.SafeGetString(0);
              person.Height = reader.SafeGetDouble(1);
              person.IsEmployed = reader.SafeGetBool(2);
              people.Add(person);
          }
      };
  }
  return people;
}
```
## Safe get 

The pulled records can be `null`.  Create the extension class below. Therefore, Instead of using `GetString`, `GetDouble`, etc. of `OdbcDataReader`, we use the below methods to handle `null` records. See the usage of methods in the example of the previous section.

```c#

public static class SafeGetMethods
{
  public static string SafeGetString(this OdbcDataReader reader, int colIndex)
  {
      if (!reader.IsDBNull(colIndex))
          return reader.GetString(colIndex);
      return string.Empty;
  }
  public static int SafeGetInt(this OdbcDataReader reader, int colIndex)
  {
      if (!reader.IsDBNull(colIndex))
          return reader.GetInt32(colIndex);
      return 0;
  }
  public static double SafeGetDouble(this OdbcDataReader reader, int colIndex)
  {
      if (!reader.IsDBNull(colIndex))
          return reader.GetDouble(colIndex);
      return 0;
  }
  public static DateTime SafeGetDate(this OdbcDataReader reader, int colIndex)
  {
      if (!reader.IsDBNull(colIndex))
          return reader.GetDateTime(colIndex);
      return new DateTime();
  }
  public static bool SafeGetBool(this OdbcDataReader reader, int colIndex)
  {
      if (!reader.IsDBNull(colIndex))
          return reader.GetBoolean(colIndex);
      return false;
      
  }
}
```