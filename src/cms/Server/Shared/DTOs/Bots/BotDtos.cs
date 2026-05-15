namespace SiteChatCMS.Shared.DTOs.Bots;

public class BotDto
{
    public string Id { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public string? SiteUrl { get; set; }
    public string SeatSlug { get; set; } = string.Empty;
    public string ChatPageUrl => $"/c/{SeatSlug}";
    public string? AvatarUrl { get; set; }
    public string? SystemPrompt { get; set; }
    public double Temperature { get; set; }
    public int MaxTokens { get; set; }
    public bool IsActive { get; set; }
    public bool IsPublic { get; set; }
    public int TrainedDocumentsCount { get; set; }
    public int TrainedUrlsCount { get; set; }
    public DateTime? LastTrainedAt { get; set; }
    public string? WidgetColor { get; set; }
    public string? WidgetPosition { get; set; }
    public string? EmbedCode { get; set; }
    public string PrimaryModel { get; set; } = BotModelCatalog.DefaultPrimaryModel;
    public string FallbackModel { get; set; } = BotModelCatalog.DefaultFallbackModel;
    public string RoutingMode { get; set; } = BotRoutingCatalog.DefaultMode;
    public DateTime CreatedAt { get; set; }
}

public class CreateBotDto
{
    public string Name { get; set; } = string.Empty;
    public string? SiteUrl { get; set; }
    public string? Description { get; set; }
    public string? SystemPrompt { get; set; }
    public double Temperature { get; set; } = 0.7;
    public int MaxTokens { get; set; } = 1000;
    public string PrimaryModel { get; set; } = BotModelCatalog.DefaultPrimaryModel;
    public string FallbackModel { get; set; } = BotModelCatalog.DefaultFallbackModel;
    public string RoutingMode { get; set; } = BotRoutingCatalog.DefaultMode;
}

public class UpdateBotDto
{
    public string? Name { get; set; }
    public string? Description { get; set; }
    public string? AvatarUrl { get; set; }
    public string? SystemPrompt { get; set; }
    public double? Temperature { get; set; }
    public int? MaxTokens { get; set; }
    public bool? IsActive { get; set; }
    public bool? IsPublic { get; set; }
    public string? WidgetColor { get; set; }
    public string? WidgetPosition { get; set; }
    public string? PrimaryModel { get; set; }
    public string? FallbackModel { get; set; }
    public string? RoutingMode { get; set; }
}

public class TrainingDocumentDto
{
    public string Id { get; set; } = string.Empty;
    public string FileName { get; set; } = string.Empty;
    public string? FileUrl { get; set; }
    public long FileSize { get; set; }
    public string ContentType { get; set; } = string.Empty;
    public string? ProcessingStatus { get; set; }
    public DateTime UploadedAt { get; set; }
}

public class TrainingUrlDto
{
    public string Id { get; set; } = string.Empty;
    public string Url { get; set; } = string.Empty;
    public string? Title { get; set; }
    public string? ProcessingStatus { get; set; }
    public DateTime AddedAt { get; set; }
    public DateTime? LastCrawledAt { get; set; }
}

public class AddTrainingUrlDto
{
    public string Url { get; set; } = string.Empty;
}

public class BotModelOptionDto
{
    public string Id { get; init; } = string.Empty;
    public string DisplayName { get; init; } = string.Empty;
    public string Route { get; init; } = string.Empty;
    public string Speed { get; init; } = string.Empty;
    public string Quality { get; init; } = string.Empty;
    public string CostLabel { get; init; } = string.Empty;
    public string Description { get; init; } = string.Empty;
}

public class BotRoutingModeOptionDto
{
    public string Id { get; init; } = string.Empty;
    public string DisplayName { get; init; } = string.Empty;
    public string Description { get; init; } = string.Empty;
}

public static class BotModelCatalog
{
    public const string DefaultPrimaryModel = "gpt-4";
    public const string DefaultFallbackModel = "sumotx";

    public static IReadOnlyList<BotModelOptionDto> All { get; } =
    [
        new BotModelOptionDto
        {
            Id = "small",
            DisplayName = "Small",
            Route = "cheap",
            Speed = "fast",
            Quality = "good",
            CostLabel = "£",
            Description = "Best for FAQs and low-complexity support requests."
        },
        new BotModelOptionDto
        {
            Id = "sumotx",
            DisplayName = "SUMOTX",
            Route = "balanced",
            Speed = "balanced",
            Quality = "strong",
            CostLabel = "££",
            Description = "Balanced model for product questions and guided support."
        },
        new BotModelOptionDto
        {
            Id = "gpt-4",
            DisplayName = "GPT-4",
            Route = "premium",
            Speed = "thoughtful",
            Quality = "best",
            CostLabel = "£££",
            Description = "Premium reasoning for technical, sensitive, or escalated conversations."
        }
    ];

    public static bool IsValid(string? modelId) =>
        !string.IsNullOrWhiteSpace(modelId) &&
        All.Any(option => option.Id.Equals(modelId, StringComparison.OrdinalIgnoreCase));

    public static string Normalize(string? modelId, string fallback) =>
        IsValid(modelId)
            ? All.First(option => option.Id.Equals(modelId, StringComparison.OrdinalIgnoreCase)).Id
            : fallback;

    public static BotModelOptionDto Get(string? modelId) =>
        All.First(option => option.Id.Equals(Normalize(modelId, DefaultPrimaryModel), StringComparison.OrdinalIgnoreCase));
}

public static class BotRoutingCatalog
{
    public const string DefaultMode = "auto";

    public static IReadOnlyList<BotRoutingModeOptionDto> All { get; } =
    [
        new BotRoutingModeOptionDto
        {
            Id = "auto",
            DisplayName = "Auto",
            Description = "Classify each message and choose the lowest-cost model that can handle it."
        },
        new BotRoutingModeOptionDto
        {
            Id = "cheap",
            DisplayName = "Cheap",
            Description = "Prefer the low-cost small model whenever possible."
        },
        new BotRoutingModeOptionDto
        {
            Id = "balanced",
            DisplayName = "Balanced",
            Description = "Default to SUMOTX for a balance of quality and cost."
        },
        new BotRoutingModeOptionDto
        {
            Id = "premium",
            DisplayName = "Premium",
            Description = "Always prefer the premium reasoning model."
        }
    ];

    public static bool IsValid(string? routingMode) =>
        !string.IsNullOrWhiteSpace(routingMode) &&
        All.Any(option => option.Id.Equals(routingMode, StringComparison.OrdinalIgnoreCase));

    public static string Normalize(string? routingMode) =>
        IsValid(routingMode)
            ? All.First(option => option.Id.Equals(routingMode, StringComparison.OrdinalIgnoreCase)).Id
            : DefaultMode;

    public static BotRoutingModeOptionDto Get(string? routingMode) =>
        All.First(option => option.Id.Equals(Normalize(routingMode), StringComparison.OrdinalIgnoreCase));
}
