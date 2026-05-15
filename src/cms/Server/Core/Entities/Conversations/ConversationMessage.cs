using SiteChatCMS.Core.Common;

namespace SiteChatCMS.Core.Entities.Conversations;

/// <summary>
/// A single message within a <see cref="Conversation"/>.
/// Role is "user", "assistant", or "system".
/// </summary>
public class ConversationMessage : BaseEntity
{
    /// <summary>FK to the owning conversation.</summary>
    public int ConversationId { get; set; }

    /// <summary>
    /// 1-based position of this message within the conversation.
    /// Used with <see cref="CreatedAt"/> to ensure deterministic ordering.
    /// </summary>
    public int SequenceNumber { get; set; }

    /// <summary>Who sent the message: "user", "assistant", or "system".</summary>
    public string Role { get; set; } = string.Empty;

    /// <summary>Full text content of the message.</summary>
    public string Content { get; set; } = string.Empty;

    /// <summary>UTC timestamp when the message was recorded.</summary>
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;

    // ── Optional AI metadata ──────────────────────────────────────────────────

    /// <summary>Model identifier used to generate this message (e.g. "gpt-4o").</summary>
    public string? Model { get; set; }

    /// <summary>Number of input/prompt tokens consumed (assistant messages only).</summary>
    public int? TokensInput { get; set; }

    /// <summary>Number of output/completion tokens generated (assistant messages only).</summary>
    public int? TokensOutput { get; set; }

    /// <summary>Confidence score in the range 0.0 – 1.0, if available from the model.</summary>
    public double? Confidence { get; set; }

    /// <summary>Optional JSON bag for extra message-level metadata.</summary>
    public string? MessageMetadataJson { get; set; }

    // ── Navigation ────────────────────────────────────────────────────────────

    /// <summary>The conversation this message belongs to.</summary>
    public virtual Conversation? Conversation { get; set; }
}
