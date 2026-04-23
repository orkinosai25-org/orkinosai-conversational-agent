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
