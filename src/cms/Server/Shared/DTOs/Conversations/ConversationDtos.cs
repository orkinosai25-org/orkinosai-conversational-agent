using System.ComponentModel.DataAnnotations;

namespace SiteChatCMS.Shared.DTOs.Conversations;

// ── Request DTOs ─────────────────────────────────────────────────────────────

/// <summary>Payload to start (or retrieve) a conversation session.</summary>
public class StartConversationDto
{
    /// <summary>Unique client-generated session ID (UUID recommended).</summary>
    [Required]
    [MaxLength(200)]
    public string SessionId { get; set; } = string.Empty;

    /// <summary>Tenant/organisation identifier for multi-tenant scoping.</summary>
    [MaxLength(450)]
    public string? TenantId { get; set; }

    /// <summary>ID of the Bot (seat) handling the conversation.</summary>
    [MaxLength(450)]
    public string? BotId { get; set; }

    /// <summary>SeatSlug of the bot — used for tenant/site association.</summary>
    [MaxLength(200)]
    public string? SeatSlug { get; set; }

    /// <summary>URL of the page where the chat was initiated.</summary>
    [MaxLength(2000)]
    public string? SourceUrl { get; set; }

    /// <summary>Language code (e.g. "en", "es").</summary>
    [MaxLength(20)]
    public string? Language { get; set; }

    /// <summary>Visitor display name (optional).</summary>
    [MaxLength(200)]
    public string? VisitorName { get; set; }

    /// <summary>Visitor email (optional).</summary>
    [MaxLength(254)]
    [EmailAddress]
    public string? VisitorEmail { get; set; }
}

/// <summary>Payload to append a message to an existing conversation.</summary>
public class AddMessageDto
{
    /// <summary>Who sent the message: "user", "assistant", or "system".</summary>
    [Required]
    [MaxLength(50)]
    public string Role { get; set; } = string.Empty;

    /// <summary>Text content of the message.</summary>
    [Required]
    [MaxLength(50000)]
    public string Content { get; set; } = string.Empty;

    /// <summary>AI model identifier (e.g. "gpt-4o") — assistant messages only.</summary>
    [MaxLength(100)]
    public string? Model { get; set; }

    /// <summary>Number of input/prompt tokens consumed — assistant messages only.</summary>
    public int? TokensInput { get; set; }

    /// <summary>Number of output/completion tokens generated — assistant messages only.</summary>
    public int? TokensOutput { get; set; }

    /// <summary>Model confidence score in the range 0.0 – 1.0.</summary>
    public double? Confidence { get; set; }
}

/// <summary>Payload to record the outcome of a conversation.</summary>
public class SetOutcomeDto
{
    /// <summary>Whether the AI resolved the visitor's query.</summary>
    public bool IsResolved { get; set; }
}

/// <summary>Payload to link a support ticket to a conversation.</summary>
public class LinkTicketDto
{
    /// <summary>Primary key of the Issue / support ticket to link.</summary>
    [Required]
    public int TicketId { get; set; }
}

// ── Response DTOs ─────────────────────────────────────────────────────────────

/// <summary>Single message within a conversation.</summary>
public class ConversationMessageDto
{
    public int Id { get; set; }
    public int SequenceNumber { get; set; }
    public string Role { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;

    /// <summary>UTC time when this message was sent in the conversation.</summary>
    public DateTime Timestamp { get; set; }

    /// <summary>AI model used to generate this message (assistant messages only).</summary>
    public string? Model { get; set; }

    /// <summary>Input token count (assistant messages only).</summary>
    public int? TokensInput { get; set; }

    /// <summary>Output token count (assistant messages only).</summary>
    public int? TokensOutput { get; set; }

    /// <summary>Confidence score 0.0 – 1.0 (if available).</summary>
    public double? Confidence { get; set; }
}

/// <summary>Full conversation details including all messages.</summary>
public class ConversationDto
{
    public int Id { get; set; }
    public string SessionId { get; set; } = string.Empty;
    public string? TenantId { get; set; }
    public string? BotId { get; set; }
    public string? SeatSlug { get; set; }
    public string? SourceUrl { get; set; }
    public string? Language { get; set; }
    public string? VisitorName { get; set; }
    public string? VisitorEmail { get; set; }
    public string Status { get; set; } = string.Empty;
    public bool IsResolved { get; set; }
    public bool WasEscalated { get; set; }
    public bool IsTicketCreated { get; set; }
    public int? TicketId { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime LastActivityAtUtc { get; set; }
    public DateTime? UpdatedAt { get; set; }
    public DateTime? EndedAt { get; set; }
    public List<ConversationMessageDto> Messages { get; set; } = new();
}

/// <summary>Summary view of a conversation — no messages included.</summary>
public class ConversationSummaryDto
{
    public int Id { get; set; }
    public string SessionId { get; set; } = string.Empty;
    public string? TenantId { get; set; }
    public string? BotId { get; set; }
    public string? SeatSlug { get; set; }
    public string? SourceUrl { get; set; }
    public string? Language { get; set; }
    public string? VisitorName { get; set; }
    public string Status { get; set; } = string.Empty;
    public bool IsResolved { get; set; }
    public bool WasEscalated { get; set; }
    public bool IsTicketCreated { get; set; }
    public int? TicketId { get; set; }
    public int MessageCount { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime LastActivityAtUtc { get; set; }
    public DateTime? UpdatedAt { get; set; }
    public DateTime? EndedAt { get; set; }
}

/// <summary>Plain-text transcript of a conversation.</summary>
public class ConversationTranscriptDto
{
    public string SessionId { get; set; } = string.Empty;
    public string Transcript { get; set; } = string.Empty;
}
