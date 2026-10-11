const databaseName = "nosql_lab1_variant5";
const marker = "nosql-lab1-v5";

db = db.getSiblingDB(databaseName);

const populatedCollections = db.getCollectionNames().filter(
  (name) => db.getCollection(name).countDocuments({ labMarker: marker }) > 0
);
if (populatedCollections.length > 0) {
  throw new Error(`Навчальні дані вже існують у колекціях: ${populatedCollections.join(", ")}`);
}

db.students.insertOne({
  _id: "student-01",
  labMarker: marker,
  fullName: "Левченко Д. В.",
  group: "КН-24-1",
  semester: 5,
  portfolio: { repository: "dirana21/5_Semestr", owner: true },
  skills: ["Python", "C#", "MongoDB", "Git"]
});

db.students.insertMany(
  Array.from({ length: 9 }, (_, index) => {
    const number = String(index + 2).padStart(2, "0");
    return {
      _id: `student-${number}`,
      labMarker: marker,
      fullName: `Студент навчального набору ${number}`,
      group: "КН-24-1",
      semester: 5,
      portfolio: { repository: null, owner: false },
      skills: ["основи програмування", "робота з даними"],
      synthetic: true
    };
  })
);

db.teachers.insertMany([
  { _id: "teacher-01", labMarker: marker, fullName: "Андреєв П. І.", role: "викладач", department: "кафедра автоматизації та інформаційних систем", disciplines: ["course-01", "course-02", "course-03"] },
  { _id: "teacher-02", labMarker: marker, fullName: "Рилова Н. В.", role: "доцент", department: "кафедра автоматизації та інформаційних систем", disciplines: ["course-04"] },
  ...Array.from({ length: 8 }, (_, index) => {
    const number = String(index + 3).padStart(2, "0");
    return { _id: `teacher-${number}`, labMarker: marker, fullName: `Викладач кафедри ${number}`, role: "викладач", department: "кафедра автоматизації та інформаційних систем", disciplines: [`course-${String(index + 5).padStart(2, "0")}`], synthetic: true };
  })
]);

db.laboratory_works.insertMany([
  { _id: "lab-01", labMarker: marker, courseId: "course-01", number: 1, variant: 5, title: "Створення документної бази даних MongoDB", tools: ["MongoDB", "Compass", "mongoimport"], status: "виконується" },
  { _id: "lab-02", labMarker: marker, courseId: "course-02", number: 1, variant: 1, title: "Консольний калькулятор", tools: ["Python", "pytest", "PyCharm"], status: "завершено" },
  { _id: "lab-03", labMarker: marker, courseId: "course-02", number: 2, variant: 1, title: "Декоратори функцій", tools: ["Python", "pytest", "PyCharm"], status: "завершено" },
  { _id: "lab-04", labMarker: marker, courseId: "course-03", number: 1, variant: 12, title: "Шифрування методами перестановки", tools: ["Python", "pytest"], status: "завершено" },
  { _id: "lab-05", labMarker: marker, courseId: "course-03", number: 2, variant: 12, title: "Шифр Плейфейра", tools: ["Python", "pytest"], status: "завершено" },
  { _id: "lab-06", labMarker: marker, courseId: "course-04", number: 1, variant: 12, title: "Формування множини Парето", tools: ["C#", ".NET", "xUnit"], status: "завершено" },
  { _id: "lab-07", labMarker: marker, courseId: "course-05", number: 1, variant: 12, title: "Графічний метод лінійного програмування", tools: ["Python", "Matplotlib"], status: "завершено" },
  { _id: "lab-08", labMarker: marker, courseId: "course-06", number: 1, variant: 5, title: "Практичне застосування принципів SOLID", tools: ["C#", "WPF", "xUnit"], status: "завершено" },
  { _id: "lab-09", labMarker: marker, courseId: "course-07", number: 1, variant: 5, title: "Побудова логічної моделі даних", tools: ["ER-модель", "SQL"], status: "заплановано" },
  { _id: "lab-10", labMarker: marker, courseId: "course-10", number: 1, variant: 5, title: "Організація репозиторію та CI", tools: ["Git", "GitHub Actions"], status: "заплановано" }
]);

db.assignments.insertMany(
  Array.from({ length: 10 }, (_, index) => {
    const number = String(index + 1).padStart(2, "0");
    return {
      _id: `assignment-${number}`,
      labMarker: marker,
      labId: `lab-${number}`,
      requirements: index === 0
        ? { minCollections: 7, minDocumentsPerCollection: 10, requiredMethods: ["mongoimport", "insertOne", "insertMany"] }
        : { report: true, sourceCode: true, screenshotsFromApplication: true },
      deliverables: ["README.md", "Звіт", "screenshots"],
      dueState: index < 8 ? "виконано" : "заплановано"
    };
  })
);

db.submissions.insertMany(
  Array.from({ length: 10 }, (_, index) => {
    const number = String(index + 1).padStart(2, "0");
    return {
      _id: `submission-${number}`,
      labMarker: marker,
      assignmentId: `assignment-${number}`,
      studentId: "student-01",
      repository: { owner: "dirana21", name: "5_Semestr", path: index === 0 ? "NoSQL бази даних/Лабораторні роботи/Лабораторна робота №1" : `portfolio/lab-${number}` },
      files: ["README.md", "Звіт", "screenshots"],
      submittedAt: new Date(Date.UTC(2026, 8, index + 1, 12, 0, 0)),
      status: index === 0 ? "готово до перевірки" : "архівовано"
    };
  })
);

db.grades.insertMany(
  Array.from({ length: 10 }, (_, index) => {
    const number = String(index + 1).padStart(2, "0");
    return {
      _id: `grade-${number}`,
      labMarker: marker,
      submissionId: `submission-${number}`,
      reviewerId: index < 5 ? "teacher-01" : "teacher-02",
      rubric: { completeness: null, correctness: null, presentation: null },
      score: null,
      status: "очікує перевірки",
      feedback: []
    };
  })
);

db.students.createIndex({ group: 1 });
db.disciplines.createIndex({ code: 1 }, { unique: true });
db.laboratory_works.createIndex({ courseId: 1, number: 1 });
db.assignments.createIndex({ labId: 1 }, { unique: true });
db.submissions.createIndex({ studentId: 1, submittedAt: -1 });
db.grades.createIndex({ submissionId: 1 }, { unique: true });

printjson({
  database: databaseName,
  collections: db.getCollectionNames().sort(),
  counts: Object.fromEntries(
    db.getCollectionNames().sort().map((name) => [name, db.getCollection(name).countDocuments({})])
  )
});
