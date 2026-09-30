namespace SolidShowcase.Core;

public sealed class StringDataReader(string content, SolidTracer tracer) : IDataReader
{
    public string Read()
    {
        tracer.Add(
            "Імпорт даних",
            "Зчитування джерела",
            "StringDataReader.Read()",
            SolidPrinciple.L,
            "Liskov Substitution Principle",
            "ImportProcessor працює з IDataReader. Рядкове, файлове або мережеве джерело можна підставити без зміни алгоритму імпорту.",
            "public string Read()\n{\n    return _content;\n}",
            3);
        return content;
    }
}
