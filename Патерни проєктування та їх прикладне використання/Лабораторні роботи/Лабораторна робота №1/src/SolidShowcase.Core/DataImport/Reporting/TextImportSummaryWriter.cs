namespace SolidShowcase.Core;

public sealed class TextImportSummaryWriter : IImportSummaryWriter
{
    public string WriteSummary(ImportResult result) =>
        $"Оброблено: {result.Total}; імпортовано: {result.Imported}; відхилено: {result.Rejected}; сума: {result.TotalAmount:0.00}";
}
