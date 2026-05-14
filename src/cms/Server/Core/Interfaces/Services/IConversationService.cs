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
        string? botId = null,
        string? seatSlug = null,
        string? sourceUrl = null,
        string? language = null,
        string? visitorName = null,
        string? visitorEmail = null);

    /// <summary>Retrieves a conversation by its external session ID, including messages.</summary>
    Task<Conversation?> GetBySessionIdAsync(string sessionId);

    /// <summary>Retrieves a conversation by its primary key, including messages.</summary>
    Task<Conversation?> GetByIdAsync(int id);

    // ── Message persistence ───────────────────────────────────────────────────

    /// <summary>
    /// Appends a message to the conversation identified by <paramref name="sessionId"/>.
    /// Creates the conversation record first if it does not exist yet.
    /// </summary>
    Task<ConversationMessage> AddMessageAsync(
        string sessionId,
        string role,
        string content,
        string? botId = null,
        string? seatSlug = null);

    // ── Outcome recording ─────────────────────────────────────────────────────

    /// <summary>Marks a conversation as resolved or unresolved.</summary>
    Task<Conversation> SetOutcomeAsync(string sessionId, bool isResolved);

    /// <summary>Links a support ticket to the conversation and marks IsTicketCreated = true.</summary>
    Task<Conversation> LinkTicketAsync(string sessionId, int ticketId);

    /// <summary>Marks the conversation session as ended.</summary>
    Task<Conversation> EndConversationAsync(string sessionId);

    // ── Transcript builder ────────────────────────────────────────────────────

    /// <summary>
    /// Builds a clean, human-readable transcript from all messages in the conversation.
    /// Format: "[User] message\n[Assistant] reply\n…"
    /// </summary>
    Task<string> BuildTranscriptAsync(string sessionId);

    // ── Admin / analytics ─────────────────────────────────────────────────────

    /// <summary>Returns all conversations, newest first.</summary>
    Task<IEnumerable<Conversation>> GetAllAsync();

    /// <summary>Returns conversations for a specific bot seat, newest first.</summary>
    Task<IEnumerable<Conversation>> GetBySeatSlugAsync(string seatSlug);
}
