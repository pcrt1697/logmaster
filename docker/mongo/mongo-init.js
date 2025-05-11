conn = new Mongo();
db = conn.getDB("logmaster");
db.createCollection('messages');
db.messages.dropIndexes();
db.messages.createIndex(
    {
      "message": "text",
      "timestamp": -1,
      "id_app": 1,
      "level": 1
   },
   {
      "name": "messages-0001"
   }
);
db.messages.createIndex(
    {
      "timestamp": -1,
      "id_app": 1,
      "level": 1
   },
   {
      "name": "messages-0002"
   }
);
