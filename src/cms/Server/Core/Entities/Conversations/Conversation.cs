using SiteChatCMS.Core.Common;
using SiteChatCMS.Core.Entities.Issues;

namespace SiteChatCMS.Core.Entities.Conversations;

/// <summary>
/// Represents a persistent SiteChat conversation session.
/// Stores who chatted, on which site/bot, and what the outcome was.
/// Every message is stored in <see cref="ConversationMessage"/>.
/// </summary>
public class Conversation : BaseEntity
{
    // ── Tenant / site association ─────────────────────────────────────────────

    /// <summary>
    /// Organisation/tenant identifier — mirrors <c>Organization.Id</c> for fast
    /// multi-tenant filtering without an extra join.
    /// </summary>
    public string? TenantId { get; set; }

    /// <summary>ID of the Bot (seat) that handled the conversation.</summary>
    public string? BotId { get; set; }

    /// <summary>Slug of the Bot seat — mirrors Bot.SeatSlug for fast querying.</summary>
    public string? SeatSlug { get; set; }

    // ── Session identification ────────────────────────────────────────────────

    /// <summary>External session ID supplied by the chat client (UUID).</summary>
    public string SessionId { get; set; } = string.Empty;

    /// <summary>Source page or URL where the conversation started.</summary>
    public string? SourceUrl { get; set; }

    /// <summary>Language code of the conversation (e.g. "en", "es").</summary>
    public string? Language { get; set; }

    /// <summary>Visitor's display name (optional, provided by the site).</summary>
    public string? VisitorName { get; set; }

    /// <summary>Visitor's email address (optional).</summary>
    public string? VisitorEmail { get; set; }

    // ── Lifecycle ─────────────────────────────────────────────────────────────

    /// <summary>
    /// Current lifecycle state of the conversation.
    /// <see cref="ConversationStatus.Active"/> while in progress.
    /// </summary>
    public ConversationStatus Status { get; set; } = ConversationStatus.Active;

    /// <summary>UTC timestamp of the most recent message or state change.</summary>
    public DateTime LastActivityAtUtc { get; set; } = DateTime.UtcNow;

    /// <summary>When the conversation session ended (null if still active).</summary>
    public DateTime? EndedAt { get; set; }

    // ── Outcome fields ────────────────────────────────────────────────────────

    /// <summary>Whether the AI successfully resolved the visitor's query.</summary>
    public bool IsResolved { get; set; }

    /// <summary>Whether the conversation was escalated (to a human / ticket).</summary>
    public bool WasEscalated { get; set; }

    /// <summary>Whether a support ticket was created for this conversation.</summary>
    public bool IsTicketCreated { get; set; }

    /// <summary>FK to the Issue (support ticket) created from this conversation.</summary>
    public int? TicketId { get; set; }

    // ── Training-ready metadata ───────────────────────────────────────────────

    /// <summary>Extractive AI summary of the conversation (set by analyser).</summary>
    public string? Summary { get; set; }

    /// <summary>Detected user intent (e.g. "billing question", "bug report").</summary>
    public string? Intent { get; set; }

    /// <summary>Detected sentiment label: Positive, Negative, Mixed, or Neutral.</summary>
    public string? Sentiment { get; set; }

    /// <summary>Sentiment confidence score 0.0 – 1.0 (1.0 = fully positive).</summary>
    public double? SentimentScore { get; set; }

    /// <summary>Classified issue category: Bug, FeatureRequest, Question, or Other.</summary>
    public string? Category { get; set; }

    /// <summary>Reason the conversation was escalated (if WasEscalated is true).</summary>
    public string? EscalationReason { get; set; }

    /// <summary>
    /// Quality label for the AI's final answer: Good, Bad, Partial, or Unknown.
    /// Set by human review or automated heuristics.
    /// </summary>
    public string? AnswerQuality { get; set; }

    /// <summary>
    /// How the conversation was ultimately resolved: AI, Human, Unresolved, or Pending.
    /// </summary>
    public string? ResolutionSource { get; set; }

    // ── Extensibility ─────────────────────────────────────────────────────────

    /// <summary>
    /// Optional JSON bag for future extensibility (e.g. UTM params, custom fields).
    /// </summary>
    public string? MetadataJson { get; set; }

    // ── Navigation ────────────────────────────────────────────────────────────

    /// <summary>All messages that belong to this conversation.</summary>
    public virtual ICollection<ConversationMessage> Messages { get; set; } = new List<ConversationMessage>();

    /// <summary>The support ticket linked to this conversation (if any).</summary>
    public virtual Issue? Ticket { get; set; }
}
