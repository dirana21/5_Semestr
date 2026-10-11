db = db.getSiblingDB("nosql_lab1_variant5");

const requiredCollections = [
  "assignments",
  "disciplines",
  "grades",
  "laboratory_works",
  "students",
  "submissions",
  "teachers"
];

const counts = Object.fromEntries(
  requiredCollections.map((name) => [name, db.getCollection(name).countDocuments({})])
);

const invalid = Object.entries(counts).filter(([, count]) => count < 10);
if (invalid.length > 0) {
  throw new Error(`Недостатньо документів: ${tojson(invalid)}`);
}

printjson({
  ok: true,
  database: db.getName(),
  collectionCount: requiredCollections.length,
  counts,
  example: db.laboratory_works.findOne({ _id: "lab-01" })
});
