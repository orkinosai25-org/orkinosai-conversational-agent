using Microsoft.EntityFrameworkCore;
using SiteChatCMS.Core.Entities.Conversations;
using SiteChatCMS.Core.Interfaces.Services;
using SiteChatCMS.Infrastructure.Data;

namespace SiteChatCMS.Infrastructure.Services.Conversations;

/// <summary>
/// EF Core-backed implementation of <see cref="IConversationService"/>.
/// Persists conversations and messages to Azure SQL via <see cref="ApplicationDbContext"/>.
/// </summary>
public class ConversationService : IConversationService
{
    private readonly ApplicationDbContext _db;

    public ConversationService(ApplicationDbContext db)
    {
        _db = db;
    }

    // ── Session management ────────────────────────────────────────────────────

    public async Task<Conversation> StartConversationAsync(
        string sessionId,
        string? botId = null,
        string? seatSlug = null,
        string? sourceUrl = null,
        string? language = null,
        string? visitorName = null,
        string? visitorEmail = null)
    {
        var existing = await _db.Conversations
            .FirstOrDefaultAsync(c => c.SessionId == sessionId);

        if (existing != null)
            return existing;

        var conversation = new Conversation
        {
            SessionId = sessionId,
            BotId = botId,
            SeatSlug = seatSlug,
            SourceUrl = sourceUrl,
            Language = language,
            VisitorName = visitorName,
            VisitorEmail = visitorEmail,
            CreatedAt = DateTime.UtcNow
        };

        _db.Conversations.Add(conversation);
        await _db.SaveChangesAsync();
        return conversation;
    }

    public async Task<Conversation?> GetBySessionIdAsync(string sessionId) =>
        await _db.Conversations
            .Include(c => c.Messages.OrderBy(m => m.Timestamp))
            .FirstOrDefaultAsync(c => c.SessionId == sessionId);

    public async Task<Conversation?> GetByIdAsync(int id) =>
        await _db.Conversations
            .Include(c => c.Messages.OrderBy(m => m.Timestamp))
            .FirstOrDefaultAsync(c => c.Id == id);

    // ── Message persistence ───────────────────────────────────────────────────

    public async Task<ConversationMessage> AddMessageAsync(
        string sessionId,
        string role,
        string content,
        string? botId = null,
        string? seatSlug = null)
    {
        // Ensure the conversation exists
        var conversation = await _db.Conversations
            .FirstOrDefaultAsync(c => c.SessionId == sessionId);

        if (conversation == null)
        {
            conversation = await StartConversationAsync(
                sessionId, botId, seatSlug);
        }

        var message = new ConversationMessage
        {
            ConversationId = conversation.Id,
            Role = role,
            Content = content,
            Timestamp = DateTime.UtcNow,
            CreatedAt = DateTime.UtcNow
        };

        _db.ConversationMessages.Add(message);
        conversation.UpdatedAt = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return message;
    }

    // ── Outcome recording ─────────────────────────────────────────────────────

    public async Task<Conversation> SetOutcomeAsync(string sessionId, bool isResolved)
    {
        var conversation = await RequireConversationAsync(sessionId);
        conversation.IsResolved = isResolved;
        conversation.UpdatedAt = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return conversation;
    }

    public async Task<Conversation> LinkTicketAsync(string sessionId, int ticketId)
    {
        var conversation = await RequireConversationAsync(sessionId);
        conversation.TicketId = ticketId;
        conversation.IsTicketCreated = true;
        conversation.UpdatedAt = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return conversation;
    }

    public async Task<Conversation> EndConversationAsync(string sessionId)
    {
        var conversation = await RequireConversationAsync(sessionId);
        conversation.EndedAt = DateTime.UtcNow;
        conversation.UpdatedAt = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return conversation;
    }

    // ── Transcript builder ────────────────────────────────────────────────────

    public async Task<string> BuildTranscriptAsync(string sessionId)
    {
        var messages = await _db.ConversationMessages
            .Where(m => m.Conversation!.SessionId == sessionId)
            .OrderBy(m => m.Timestamp)
            .ToListAsync();

        if (messages.Count == 0)
            return string.Empty;

        var lines = messages.Select(m =>
        {
            var label = m.Role.Equals("user", StringComparison.OrdinalIgnoreCase)
                ? "User"
                : "Assistant";
            return $"[{label}] {m.Content}";
        });

        return string.Join("\n", lines);
    }

    // ── Admin / analytics ─────────────────────────────────────────────────────

    public async Task<IEnumerable<Conversation>> GetAllAsync() =>
        await _db.Conversations
            .OrderByDescending(c => c.CreatedAt)
            .ToListAsync();

    public async Task<IEnumerable<Conversation>> GetBySeatSlugAsync(string seatSlug) =>
        await _db.Conversations
            .Where(c => c.SeatSlug == seatSlug)
            .OrderByDescending(c => c.CreatedAt)
            .ToListAsync();

    // ── Helpers ───────────────────────────────────────────────────────────────

    private async Task<Conversation> RequireConversationAsync(string sessionId)
    {
        return await _db.Conversations
            .FirstOrDefaultAsync(c => c.SessionId == sessionId)
            ?? throw new KeyNotFoundException(
                $"Conversation with session ID '{sessionId}' was not found.");
    }
}
