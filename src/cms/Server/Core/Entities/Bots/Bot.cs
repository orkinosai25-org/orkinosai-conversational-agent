namespace PapaganCMS.Core.Entities.Identity;

/// <summary>
/// Bot entity representing a trained chatbot instance
/// </summary>
public class Bot
{
    public string Id { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? UpdatedAt { get; set; }
    
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public string UserId { get; set; } = string.Empty;
    public string? OrganizationId { get; set; }
    public string? AvatarUrl { get; set; }
    public string? SystemPrompt { get; set; }
    public double Temperature { get; set; } = 0.7;
    public int MaxTokens { get; set; } = 1000;
    public bool IsActive { get; set; } = true;
    public bool IsPublic { get; set; } = false;
    
    // Training status
    public int TrainedDocumentsCount { get; set; } = 0;
    public int TrainedUrlsCount { get; set; } = 0;
    public DateTime? LastTrainedAt { get; set; }
    
    // Widget settings
    public string? WidgetColor { get; set; }
    public string? WidgetPosition { get; set; }
    public string? EmbedCode { get; set; }
    
    // Navigation
    public virtual ApplicationUser? User { get; set; }
    public virtual Organization? Organization { get; set; }
    public virtual ICollection<TrainingDocument> TrainingDocuments { get; set; } = new List<TrainingDocument>();
    public virtual ICollection<TrainingUrl> TrainingUrls { get; set; } = new List<TrainingUrl>();
}

/// <summary>
/// Training document uploaded by user
/// </summary>
public class TrainingDocument
{
    public string Id { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? UpdatedAt { get; set; }
    
    public string BotId { get; set; } = string.Empty;
    public string FileName { get; set; } = string.Empty;
    public string? FileUrl { get; set; }
    public long FileSize { get; set; }
    public string ContentType { get; set; } = string.Empty;
    public string? ProcessingStatus { get; set; }
    public DateTime UploadedAt { get; set; } = DateTime.UtcNow;
    
    // Navigation
    public virtual Bot? Bot { get; set; }
}

/// <summary>
/// URL used for training the bot
/// </summary>
public class TrainingUrl
{
    public string Id { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? UpdatedAt { get; set; }
    
    public string BotId { get; set; } = string.Empty;
    public string Url { get; set; } = string.Empty;
    public string? Title { get; set; }
    public string? ProcessingStatus { get; set; }
    public DateTime AddedAt { get; set; } = DateTime.UtcNow;
    public DateTime? LastCrawledAt { get; set; }
    
    // Navigation
    public virtual Bot? Bot { get; set; }
}
