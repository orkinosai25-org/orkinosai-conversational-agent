using SiteChatCMS.Core.Entities.Conversations;

namespace SiteChatCMS.Core.Interfaces.Services;

/// <summary>
/// Persistent storage and retrieval of SiteChat conversation sessions and their messages.
/// Implementations must be scoped (they depend on a scoped DbContext).
/// </summary>
public interface IConversationService
{
    // ── Session management ────────────────────────────────────────────────────

    /// <summary>
    /// Creates a new conversation record and returns it.
    /// If a conversation with the same <paramref name="sessionId"/> already exists,
    /// that existing record is returned instead (idempotent).
    /// </summary>
    Task<Conversation> StartConversationAsync(
        string sessionId,
        string? tenantId = null,
        string? botId = null,
        string? seatSlug = null,
        string? sourceUrl = null,
        string? language = null,
        string? visitorName = null,
        string? visitorEmail = null);

    /// <summary>Retrieves a conversation by its external session ID, including messages ordered by SequenceNumber.</summary>
    Task<Conversation?> GetBySessionIdAsync(string sessionId);

    /// <summary>Retrieves a conversation by its primary key, including messages ordered by SequenceNumber.</summary>
    Task<Conversation?> GetByIdAsync(int id);

    // ── Message persistence ───────────────────────────────────────────────────

    /// <summary>
    /// Appends a message to the conversation identified by <paramref name="sessionId"/>.
    /// Creates the conversation record first if it does not exist yet.
    /// SequenceNumber is assigned automatically (max + 1 within the conversation).
    /// </summary>
    Task<ConversationMessage> AddMessageAsync(
        string sessionId,
        string role,
        string content,
        string? botId = null,
        string? seatSlug = null,
        string? model = null,
        int? tokensInput = null,
        int? tokensOutput = null,
        double? confidence = null);

    /// <summary>Returns all messages for a conversation, ordered by SequenceNumber then Timestamp.</summary>
    Task<IEnumerable<ConversationMessage>> GetMessagesAsync(string sessionId);

    // ── Outcome recording ─────────────────────────────────────────────────────

    /// <summary>Marks a conversation as resolved or unresolved and updates its Status accordingly.</summary>
    Task<Conversation> SetOutcomeAsync(string sessionId, bool isResolved);

    /// <summary>Marks the conversation as escalated (e.g. to human support) and sets WasEscalated = true.</summary>
    Task<Conversation> EscalateConversationAsync(string sessionId);

    /// <summary>Links a support ticket to the conversation and marks IsTicketCreated = true.</summary>
    Task<Conversation> LinkTicketAsync(string sessionId, int ticketId);

    /// <summary>Marks the conversation session as ended and sets Status to Closed.</summary>
    Task<Conversation> EndConversationAsync(string sessionId);

    // ── Transcript builder ────────────────────────────────────────────────────

    /// <summary>
    /// Builds a clean, human-readable transcript from all messages in the conversation,
    /// ordered by SequenceNumber then Timestamp. Empty messages are skipped.
    /// Format: "User: message\nAssistant: reply\n…"
    /// </summary>
    Task<string> BuildTranscriptAsync(string sessionId);

    // ── Admin / analytics ─────────────────────────────────────────────────────

    /// <summary>Returns all conversations, newest first.</summary>
    Task<IEnumerable<Conversation>> GetAllAsync();

    /// <summary>Returns conversations for a specific bot seat, newest first.</summary>
    Task<IEnumerable<Conversation>> GetBySeatSlugAsync(string seatSlug);

    /// <summary>Returns conversations for a specific tenant (organisation), newest first.</summary>
    Task<IEnumerable<Conversation>> GetByTenantIdAsync(string tenantId);

    // ── Training metadata ─────────────────────────────────────────────────────

    /// <summary>
    /// Runs the <see cref="SiteChatCMS.Infrastructure.Services.Issues.ConversationAnalyser"/>
    /// against the conversation transcript and persists the derived training metadata
    /// (summary, intent, sentiment, category) back to the conversation record.
    /// </summary>
    Task<Conversation> AnalyseConversationAsync(string sessionId);

    /// <summary>
    /// Manually overrides training metadata on a conversation.
    /// Any non-null parameter value replaces the existing column value.
    /// </summary>
    Task<Conversation> SetTrainingMetadataAsync(
        string sessionId,
        string? answerQuality = null,
        string? resolutionSource = null,
        string? escalationReason = null,
        string? intent = null);

    // ── Dataset export ────────────────────────────────────────────────────────

    /// <summary>
    /// Returns all conversations as export-ready records containing the conversation
    /// metadata, training labels, transcript, and linked ticket information.
    /// Ordered by creation date ascending (oldest first) for stable export batches.
    /// </summary>
    Task<IEnumerable<Conversation>> GetAllForExportAsync();
}
