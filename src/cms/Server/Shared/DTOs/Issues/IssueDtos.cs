using System.ComponentModel.DataAnnotations;

namespace SiteChatCMS.Shared.DTOs.Issues;

/// <summary>
/// Full issue details returned to clients
/// </summary>
public class IssueDto
{
    public int Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string Type { get; set; } = string.Empty;
    public string Priority { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public string SubmitterName { get; set; } = string.Empty;
    public string? SubmitterEmail { get; set; }
    public string? AdminNotes { get; set; }
    public DateTime? ResolvedAt { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
}

/// <summary>
/// Payload for submitting a new issue
/// </summary>
public class CreateIssueDto
{
    [Required]
    [MaxLength(200)]
    public string Title { get; set; } = string.Empty;

    [Required]
    [MaxLength(5000)]
    public string Description { get; set; } = string.Empty;

    [MaxLength(50)]
    public string Type { get; set; } = string.Empty;

    [MaxLength(50)]
    public string Priority { get; set; } = string.Empty;

    [MaxLength(200)]
    public string SubmitterName { get; set; } = string.Empty;

    [Required]
    [MaxLength(254)]
    [EmailAddress]
    public string SubmitterEmail { get; set; } = string.Empty;
}

/// <summary>
/// Payload for admin edits to an existing issue
/// </summary>
public class UpdateIssueDto
{
    [Required]
    [MaxLength(200)]
    public string Title { get; set; } = string.Empty;

    [Required]
    [MaxLength(5000)]
    public string Description { get; set; } = string.Empty;

    [MaxLength(50)]
    public string Type { get; set; } = string.Empty;

    [MaxLength(50)]
    public string Priority { get; set; } = string.Empty;

    [MaxLength(50)]
    public string Status { get; set; } = string.Empty;

    [MaxLength(2000)]
    public string? AdminNotes { get; set; }
}

/// <summary>
/// Aggregate statistics for the admin issue dashboard
/// </summary>
public class IssueStatsDto
{
    public int TotalIssues { get; set; }
    public int OpenIssues { get; set; }
    public int InProgressIssues { get; set; }
    public int ResolvedIssues { get; set; }
    public int ClosedIssues { get; set; }
    public int CriticalIssues { get; set; }
}

/// <summary>
/// Payload for resolving an issue with optional admin notes
/// </summary>
public class ResolveIssueDto
{
    public string? AdminNotes { get; set; }
}

/// <summary>
/// Payload for auto-creating a support ticket from an AI chat conversation transcript
/// </summary>
public class ConversationToTicketDto
{
    /// <summary>Full conversation transcript (alternating user / agent turns)</summary>
    [Required]
    [MaxLength(50000)]
    public string Transcript { get; set; } = string.Empty;

    /// <summary>Website or channel where the conversation occurred</summary>
    [MaxLength(2048)]
    public string? SourceUrl { get; set; }

    /// <summary>Name of the user who started the conversation (optional)</summary>
    [MaxLength(200)]
    public string? SubmitterName { get; set; }

    /// <summary>Contact email of the user — required to route the ticket</summary>
    [Required]
    [MaxLength(254)]
    [EmailAddress]
    public string SubmitterEmail { get; set; } = string.Empty;
}

/// <summary>
/// Result returned when a ticket is auto-created from a conversation.
/// Includes the created ticket plus the AI analysis that drove its classification.
/// </summary>
public class ConversationTicketResult
{
    /// <summary>The support ticket that was created</summary>
    public IssueDto Ticket { get; set; } = new();

    /// <summary>Detected sentiment: Positive, Neutral, Negative, or Mixed</summary>
    public string Sentiment { get; set; } = "Neutral";

    /// <summary>Sentiment confidence score in the range 0.0 – 1.0</summary>
    public double SentimentScore { get; set; }

    /// <summary>Extractive summary of the conversation</summary>
    public string Summary { get; set; } = string.Empty;

    /// <summary>Auto-detected issue type (Bug / FeatureRequest / Question / Other)</summary>
    public string DetectedType { get; set; } = string.Empty;

    /// <summary>Auto-detected priority (Low / Medium / High / Critical)</summary>
    public string DetectedPriority { get; set; } = string.Empty;
}
