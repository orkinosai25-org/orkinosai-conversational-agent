using Microsoft.EntityFrameworkCore;
using SiteChatCMS.Core.Entities.Conversations;
using SiteChatCMS.Core.Interfaces.Services;
using SiteChatCMS.Infrastructure.Data;
using SiteChatCMS.Infrastructure.Services.Issues;

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
        string? tenantId = null,
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

        var now = DateTime.UtcNow;
        var conversation = new Conversation
        {
            SessionId = sessionId,
            TenantId = tenantId,
            BotId = botId,
            SeatSlug = seatSlug,
            SourceUrl = sourceUrl,
            Language = language,
            VisitorName = visitorName,
            VisitorEmail = visitorEmail,
            Status = ConversationStatus.Active,
            LastActivityAtUtc = now,
            CreatedAt = now
        };

        _db.Conversations.Add(conversation);
        await _db.SaveChangesAsync();
        return conversation;
    }

    public async Task<Conversation?> GetBySessionIdAsync(string sessionId) =>
        await _db.Conversations
            .Include(c => c.Messages.OrderBy(m => m.SequenceNumber).ThenBy(m => m.Timestamp))
            .FirstOrDefaultAsync(c => c.SessionId == sessionId);

    public async Task<Conversation?> GetByIdAsync(int id) =>
        await _db.Conversations
            .Include(c => c.Messages.OrderBy(m => m.SequenceNumber).ThenBy(m => m.Timestamp))
            .FirstOrDefaultAsync(c => c.Id == id);

    // ── Message persistence ───────────────────────────────────────────────────

    public async Task<ConversationMessage> AddMessageAsync(
        string sessionId,
        string role,
        string content,
        string? botId = null,
        string? seatSlug = null,
        string? model = null,
        int? tokensInput = null,
        int? tokensOutput = null,
        double? confidence = null)
    {
        // Ensure the conversation exists
        var conversation = await _db.Conversations
            .FirstOrDefaultAsync(c => c.SessionId == sessionId);

        if (conversation == null)
        {
            conversation = await StartConversationAsync(
                sessionId, botId: botId, seatSlug: seatSlug);
        }

        // Determine the next sequence number for this conversation
        var nextSeq = await _db.ConversationMessages
            .Where(m => m.ConversationId == conversation.Id)
            .MaxAsync(m => (int?)m.SequenceNumber) ?? 0;
        nextSeq++;

        var now = DateTime.UtcNow;
        var message = new ConversationMessage
        {
            ConversationId = conversation.Id,
            SequenceNumber = nextSeq,
            Role = role,
            Content = content,
            Timestamp = now,
            Model = model,
            TokensInput = tokensInput,
            TokensOutput = tokensOutput,
            Confidence = confidence,
            CreatedAt = now
        };

        _db.ConversationMessages.Add(message);
        conversation.LastActivityAtUtc = now;
        conversation.UpdatedAt = now;
        await _db.SaveChangesAsync();
        return message;
    }

    public async Task<IEnumerable<ConversationMessage>> GetMessagesAsync(string sessionId) =>
        await _db.ConversationMessages
            .Where(m => m.Conversation!.SessionId == sessionId)
            .OrderBy(m => m.SequenceNumber)
            .ThenBy(m => m.Timestamp)
            .ToListAsync();

    // ── Outcome recording ─────────────────────────────────────────────────────

    public async Task<Conversation> SetOutcomeAsync(string sessionId, bool isResolved)
    {
        var conversation = await RequireConversationAsync(sessionId);
        conversation.IsResolved = isResolved;
        conversation.Status = isResolved ? ConversationStatus.Resolved : ConversationStatus.Unresolved;
        conversation.LastActivityAtUtc = DateTime.UtcNow;
        conversation.UpdatedAt = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return conversation;
    }

    public async Task<Conversation> EscalateConversationAsync(string sessionId)
    {
        var conversation = await RequireConversationAsync(sessionId);
        conversation.WasEscalated = true;
        conversation.Status = ConversationStatus.Escalated;
        conversation.LastActivityAtUtc = DateTime.UtcNow;
        conversation.UpdatedAt = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return conversation;
    }

    public async Task<Conversation> LinkTicketAsync(string sessionId, int ticketId)
    {
        var conversation = await RequireConversationAsync(sessionId);
        conversation.TicketId = ticketId;
        conversation.IsTicketCreated = true;
        conversation.LastActivityAtUtc = DateTime.UtcNow;
        conversation.UpdatedAt = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return conversation;
    }

    public async Task<Conversation> EndConversationAsync(string sessionId)
    {
        var conversation = await RequireConversationAsync(sessionId);
        var now = DateTime.UtcNow;
        conversation.EndedAt = now;
        conversation.LastActivityAtUtc = now;
        conversation.UpdatedAt = now;
        // Only move to Closed if not already in a terminal state
        if (conversation.Status == ConversationStatus.Active)
            conversation.Status = ConversationStatus.Closed;
        await _db.SaveChangesAsync();
        return conversation;
    }

    // ── Transcript builder ────────────────────────────────────────────────────

    public async Task<string> BuildTranscriptAsync(string sessionId)
    {
        var messages = await _db.ConversationMessages
            .Where(m => m.Conversation!.SessionId == sessionId)
            .OrderBy(m => m.SequenceNumber)
            .ThenBy(m => m.Timestamp)
            .ToListAsync();

        if (messages.Count == 0)
            return string.Empty;

        var lines = messages
            .Where(m => !string.IsNullOrWhiteSpace(m.Content))
            .Select(m =>
            {
                var label = m.Role.ToLowerInvariant() switch
                {
                    "user" => "User",
                    "assistant" => "Assistant",
                    _ => m.Role
                };
                return $"{label}: {m.Content.Trim()}";
            });

        return string.Join("\n", lines);
    }

    // ── Admin / analytics ─────────────────────────────────────────────────────

    public async Task<IEnumerable<Conversation>> GetAllAsync() =>
        await _db.Conversations
            .Include(c => c.Messages)
            .OrderByDescending(c => c.CreatedAt)
            .ToListAsync();

    public async Task<IEnumerable<Conversation>> GetBySeatSlugAsync(string seatSlug) =>
        await _db.Conversations
            .Include(c => c.Messages)
            .Where(c => c.SeatSlug == seatSlug)
            .OrderByDescending(c => c.CreatedAt)
            .ToListAsync();

    public async Task<IEnumerable<Conversation>> GetByTenantIdAsync(string tenantId) =>
        await _db.Conversations
            .Include(c => c.Messages)
            .Where(c => c.TenantId == tenantId)
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

    // ── Training metadata ─────────────────────────────────────────────────────

    public async Task<Conversation> AnalyseConversationAsync(string sessionId)
    {
        var conversation = await RequireConversationAsync(sessionId);
        var transcript = await BuildTranscriptAsync(sessionId);

        if (!string.IsNullOrWhiteSpace(transcript))
        {
            var (sentimentLabel, sentimentScore) = ConversationAnalyser.DetectSentiment(transcript);
            var summary = ConversationAnalyser.Summarise(transcript);
            var category = ConversationAnalyser.DetectType(transcript);

            conversation.Sentiment = sentimentLabel;
            conversation.SentimentScore = sentimentScore;
            conversation.Summary = summary.Length > 1000 ? summary[..997] + "…" : summary;
            conversation.Category = category;

            // Derive intent label from category and sentiment
            conversation.Intent = BuildIntentLabel(category, sentimentLabel);
        }

        conversation.UpdatedAt = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return conversation;
    }

    public async Task<Conversation> SetTrainingMetadataAsync(
        string sessionId,
        string? answerQuality = null,
        string? resolutionSource = null,
        string? escalationReason = null,
        string? intent = null)
    {
        var conversation = await RequireConversationAsync(sessionId);

        if (answerQuality != null)
            conversation.AnswerQuality = answerQuality;
        if (resolutionSource != null)
            conversation.ResolutionSource = resolutionSource;
        if (escalationReason != null)
            conversation.EscalationReason = escalationReason;
        if (intent != null)
            conversation.Intent = intent;

        conversation.UpdatedAt = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return conversation;
    }

    // ── Dataset export ────────────────────────────────────────────────────────

    public async Task<IEnumerable<Conversation>> GetAllForExportAsync() =>
        await _db.Conversations
            .Include(c => c.Messages.OrderBy(m => m.SequenceNumber).ThenBy(m => m.Timestamp))
            .Include(c => c.Ticket)
            .OrderBy(c => c.CreatedAt)
            .ToListAsync();

    // ── Private helpers ───────────────────────────────────────────────────────

    private static string BuildIntentLabel(string category, string sentiment) => category switch
    {
        "Bug" => "report_bug",
        "FeatureRequest" => "request_feature",
        "Question" => "ask_question",
        _ => sentiment == "Negative" ? "express_frustration" : "general_enquiry"
    };

}
