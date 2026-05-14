using SiteChatCMS.Core.Common;

namespace SiteChatCMS.Core.Entities.Conversations;

/// <summary>
/// A single message within a <see cref="Conversation"/>.
/// Role is "user" or "assistant".
/// </summary>
public class ConversationMessage : BaseEntity
{
    /// <summary>FK to the owning conversation.</summary>
    public int ConversationId { get; set; }

    /// <summary>Who sent the message: "user" or "assistant".</summary>
    public string Role { get; set; } = string.Empty;

    /// <summary>Full text content of the message.</summary>
    public string Content { get; set; } = string.Empty;

    /// <summary>UTC timestamp when the message was recorded.</summary>
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;

    // ── Navigation ────────────────────────────────────────────────────────────

    /// <summary>The conversation this message belongs to.</summary>
    public virtual Conversation? Conversation { get; set; }
}
