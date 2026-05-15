using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SiteChatCMS.Core.Interfaces.Services;
using SiteChatCMS.Infrastructure.Services.Issues;
using SiteChatCMS.Shared.DTOs.Conversations;
using SiteChatCMS.Shared.DTOs.Issues;

namespace SiteChatCMS.Controllers;

/// <summary>
/// REST API for persistent SiteChat conversation storage.
/// Public endpoints are used by the chat widget; admin endpoints require authentication.
/// </summary>
[ApiController]
[Route("api/[controller]")]
public class ConversationController : ControllerBase
{
    private readonly IConversationService _conversationService;
    private readonly IIssueService _issueService;
    private readonly ILogger<ConversationController> _logger;

    public ConversationController(
        IConversationService conversationService,
        IIssueService issueService,
        ILogger<ConversationController> logger)
    {
        _conversationService = conversationService;
        _issueService = issueService;
        _logger = logger;
    }

    // ── Public endpoints (used by the chat widget) ────────────────────────────

    /// <summary>
    /// Start a new conversation session, or return the existing one if the
    /// session ID is already known.
    /// </summary>
    [HttpPost("start")]
    [ProducesResponseType(typeof(ConversationDto), 201)]
    [ProducesResponseType(typeof(ConversationDto), 200)]
    [ProducesResponseType(400)]
    public async Task<IActionResult> Start([FromBody] StartConversationDto dto)
    {
        if (string.IsNullOrWhiteSpace(dto.SessionId))
            return BadRequest("SessionId is required.");

        try
        {
            var conversation = await _conversationService.StartConversationAsync(
                dto.SessionId,
                tenantId: dto.TenantId,
                botId: dto.BotId,
                seatSlug: dto.SeatSlug,
                sourceUrl: dto.SourceUrl,
                language: dto.Language,
                visitorName: dto.VisitorName,
                visitorEmail: dto.VisitorEmail);

            var result = MapConversation(conversation);

            // Return 200 if already existed, 201 if newly created
            var isNew = conversation.Messages.Count == 0 && conversation.UpdatedAt == null;
            return isNew
                ? CreatedAtAction(nameof(GetBySession), new { sessionId = conversation.SessionId }, result)
                : Ok(result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error starting conversation {SessionId}", SanitizeForLog(dto.SessionId));
            return StatusCode(500, "An error occurred while starting the conversation.");
        }
    }

    /// <summary>
    /// Append a message (user, assistant, or system) to an existing conversation.
    /// Creates the conversation record automatically if not yet started.
    /// </summary>
    [HttpPost("{sessionId}/messages")]
    [ProducesResponseType(typeof(ConversationMessageDto), 201)]
    [ProducesResponseType(400)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> AddMessage(
        string sessionId,
        [FromBody] AddMessageDto dto,
        [FromQuery] string? botId = null,
        [FromQuery] string? seatSlug = null)
    {
        if (string.IsNullOrWhiteSpace(dto.Role))
            return BadRequest("Role is required.");
        if (string.IsNullOrWhiteSpace(dto.Content))
            return BadRequest("Content is required.");

        var normalizedRole = dto.Role.ToLowerInvariant();
        if (normalizedRole is not ("user" or "assistant" or "system"))
            return BadRequest("Role must be 'user', 'assistant', or 'system'.");

        try
        {
            var message = await _conversationService.AddMessageAsync(
                sessionId, dto.Role, dto.Content,
                botId, seatSlug,
                dto.Model, dto.TokensInput, dto.TokensOutput, dto.Confidence);

            return CreatedAtAction(
                nameof(GetBySession),
                new { sessionId },
                MapMessage(message));
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error adding message to session {SessionId}", SanitizeForLog(sessionId));
            return StatusCode(500, "An error occurred while saving the message.");
        }
    }

    /// <summary>List all messages for a conversation in order.</summary>
    [HttpGet("{sessionId}/messages")]
    [ProducesResponseType(typeof(IEnumerable<ConversationMessageDto>), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> GetMessages(string sessionId)
    {
        var conversation = await _conversationService.GetBySessionIdAsync(sessionId);
        if (conversation == null) return NotFound();

        var messages = await _conversationService.GetMessagesAsync(sessionId);
        return Ok(messages.Select(MapMessage));
    }

    /// <summary>Get a conversation by its external session ID, including all messages.</summary>
    [HttpGet("{sessionId}")]
    [ProducesResponseType(typeof(ConversationDto), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> GetBySession(string sessionId)
    {
        var conversation = await _conversationService.GetBySessionIdAsync(sessionId);
        if (conversation == null) return NotFound();
        return Ok(MapConversation(conversation));
    }

    /// <summary>
    /// Return the plain-text transcript for a conversation.
    /// Useful for feeding into ticket creation or AI analysis.
    /// </summary>
    [HttpGet("{sessionId}/transcript")]
    [ProducesResponseType(typeof(ConversationTranscriptDto), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> GetTranscript(string sessionId)
    {
        var conversation = await _conversationService.GetBySessionIdAsync(sessionId);
        if (conversation == null) return NotFound();

        var transcript = await _conversationService.BuildTranscriptAsync(sessionId);
        return Ok(new ConversationTranscriptDto
        {
            SessionId = sessionId,
            Transcript = transcript
        });
    }

    /// <summary>Record whether the AI resolved the visitor's query.</summary>
    [HttpPost("{sessionId}/outcome")]
    [ProducesResponseType(typeof(ConversationDto), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> SetOutcome(string sessionId, [FromBody] SetOutcomeDto dto)
    {
        try
        {
            var conversation = await _conversationService.SetOutcomeAsync(sessionId, dto.IsResolved);
            return Ok(MapConversation(conversation));
        }
        catch (KeyNotFoundException)
        {
            return NotFound();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error setting outcome for session {SessionId}", SanitizeForLog(sessionId));
            return StatusCode(500, "An error occurred while recording the outcome.");
        }
    }

    /// <summary>Mark the conversation as escalated to human support.</summary>
    [HttpPost("{sessionId}/escalate")]
    [ProducesResponseType(typeof(ConversationDto), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> Escalate(string sessionId)
    {
        try
        {
            var conversation = await _conversationService.EscalateConversationAsync(sessionId);
            return Ok(MapConversation(conversation));
        }
        catch (KeyNotFoundException)
        {
            return NotFound();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error escalating session {SessionId}", SanitizeForLog(sessionId));
            return StatusCode(500, "An error occurred while escalating the conversation.");
        }
    }

    /// <summary>Mark the conversation session as ended.</summary>
    [HttpPost("{sessionId}/end")]
    [ProducesResponseType(typeof(ConversationDto), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> End(string sessionId)
    {
        try
        {
            var conversation = await _conversationService.EndConversationAsync(sessionId);
            return Ok(MapConversation(conversation));
        }
        catch (KeyNotFoundException)
        {
            return NotFound();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error ending session {SessionId}", SanitizeForLog(sessionId));
            return StatusCode(500, "An error occurred while ending the conversation.");
        }
    }

    /// <summary>Link a support ticket to the conversation.</summary>
    [HttpPost("{sessionId}/ticket")]
    [ProducesResponseType(typeof(ConversationDto), 200)]
    [ProducesResponseType(400)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> LinkTicket(string sessionId, [FromBody] LinkTicketDto dto)
    {
        try
        {
            var conversation = await _conversationService.LinkTicketAsync(sessionId, dto.TicketId);
            return Ok(MapConversation(conversation));
        }
        catch (KeyNotFoundException)
        {
            return NotFound();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error linking ticket to session {SessionId}", SanitizeForLog(sessionId));
            return StatusCode(500, "An error occurred while linking the ticket.");
        }
    }

    /// <summary>
    /// Analyse a conversation transcript using the rule-based analyser and store
    /// the derived training metadata (sentiment, summary, category, intent).
    /// If the conversation is unresolved and <paramref name="createTicket"/> is true,
    /// a support ticket is automatically created and linked.
    /// </summary>
    [HttpPost("{sessionId}/analyse")]
    [ProducesResponseType(typeof(ConversationAnalysisResultDto), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> Analyse(string sessionId, [FromQuery] bool createTicket = false)
    {
        var conversation = await _conversationService.GetBySessionIdAsync(sessionId);
        if (conversation == null) return NotFound();

        try
        {
            conversation = await _conversationService.AnalyseConversationAsync(sessionId);

            IssueTicketRef? ticketRef = null;

            if (createTicket && !conversation.IsTicketCreated && !conversation.IsResolved)
            {
                var transcript = await _conversationService.BuildTranscriptAsync(sessionId);

                if (!string.IsNullOrWhiteSpace(transcript))
                {
                    var (sentiment, sentimentScore) = ConversationAnalyser.DetectSentiment(transcript);
                    var summary = ConversationAnalyser.Summarise(transcript);
                    var detectedType = ConversationAnalyser.DetectType(transcript);
                    var detectedPriority = ConversationAnalyser.DetectPriority(transcript);

                    if (!Enum.TryParse<Core.Entities.Issues.IssueType>(detectedType, out var issueType))
                        issueType = Core.Entities.Issues.IssueType.Other;
                    if (!Enum.TryParse<Core.Entities.Issues.IssuePriority>(detectedPriority, out var issuePriority))
                        issuePriority = Core.Entities.Issues.IssuePriority.Medium;

                    var title = summary.Length > 100 ? summary[..97] + "…" : summary;
                    var adminNotes = $"{ConversationAnalyser.SummaryPrefix} {summary}\n{ConversationAnalyser.SentimentPrefix} {sentiment} ({sentimentScore:P0})";
                    if (!string.IsNullOrWhiteSpace(conversation.SourceUrl))
                        adminNotes += $"\n[Source] {conversation.SourceUrl}";

                    var issue = new Core.Entities.Issues.Issue
                    {
                        Title = title,
                        Description = transcript,
                        Type = issueType,
                        Priority = issuePriority,
                        SubmitterName = conversation.VisitorName ?? "SiteChat Visitor",
                        SubmitterEmail = conversation.VisitorEmail ?? "noreply@sitechat.ai",
                        AdminNotes = adminNotes
                    };

                    var created = await _issueService.CreateIssueAsync(issue);
                    await _conversationService.LinkTicketAsync(sessionId, created.Id);
                    await _conversationService.EscalateConversationAsync(sessionId);

                    conversation = await _conversationService.GetBySessionIdAsync(sessionId)
                                   ?? conversation;

                    ticketRef = new IssueTicketRef
                    {
                        Id = created.Id,
                        Title = created.Title,
                        Status = created.Status.ToString()
                    };
                }
            }

            var result = new ConversationAnalysisResultDto
            {
                Conversation = MapConversation(conversation),
                Sentiment = conversation.Sentiment ?? string.Empty,
                SentimentScore = conversation.SentimentScore ?? 0,
                Summary = conversation.Summary ?? string.Empty,
                Category = conversation.Category ?? string.Empty,
                Intent = conversation.Intent ?? string.Empty,
                CreatedTicket = ticketRef
            };

            return Ok(result);
        }
        catch (KeyNotFoundException)
        {
            return NotFound();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error analysing session {SessionId}", SanitizeForLog(sessionId));
            return StatusCode(500, "An error occurred while analysing the conversation.");
        }
    }

    /// <summary>
    /// Manually set training-review labels on a conversation.
    /// Used by human reviewers to rate answer quality, resolution source, etc.
    /// </summary>
    [HttpPost("{sessionId}/metadata")]
    [ProducesResponseType(typeof(ConversationDto), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> SetMetadata(string sessionId, [FromBody] SetTrainingMetadataDto dto)
    {
        try
        {
            var conversation = await _conversationService.SetTrainingMetadataAsync(
                sessionId,
                answerQuality: dto.AnswerQuality,
                resolutionSource: dto.ResolutionSource,
                escalationReason: dto.EscalationReason,
                intent: dto.Intent);
            return Ok(MapConversation(conversation));
        }
        catch (KeyNotFoundException)
        {
            return NotFound();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error setting metadata for session {SessionId}", SanitizeForLog(sessionId));
            return StatusCode(500, "An error occurred while setting the metadata.");
        }
    }

    // ── Admin endpoints ───────────────────────────────────────────────────────

    /// <summary>Admin: list all conversations (summaries, no messages).</summary>
    [Authorize]
    [HttpGet("admin/all")]
    [ProducesResponseType(typeof(IEnumerable<ConversationSummaryDto>), 200)]
    public async Task<IActionResult> GetAll()
    {
        var conversations = await _conversationService.GetAllAsync();
        return Ok(conversations.Select(MapSummary));
    }

    /// <summary>Admin: list conversations for a specific bot seat.</summary>
    [Authorize]
    [HttpGet("admin/seat/{seatSlug}")]
    [ProducesResponseType(typeof(IEnumerable<ConversationSummaryDto>), 200)]
    public async Task<IActionResult> GetBySeat(string seatSlug)
    {
        var conversations = await _conversationService.GetBySeatSlugAsync(seatSlug);
        return Ok(conversations.Select(MapSummary));
    }

    /// <summary>Admin: list conversations for a specific tenant (organisation).</summary>
    [Authorize]
    [HttpGet("admin/tenant/{tenantId}")]
    [ProducesResponseType(typeof(IEnumerable<ConversationSummaryDto>), 200)]
    public async Task<IActionResult> GetByTenant(string tenantId)
    {
        var conversations = await _conversationService.GetByTenantIdAsync(tenantId);
        return Ok(conversations.Select(MapSummary));
    }

    /// <summary>Admin: get full conversation details by primary key.</summary>
    [Authorize]
    [HttpGet("admin/{id:int}")]
    [ProducesResponseType(typeof(ConversationDto), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> GetById(int id)
    {
        var conversation = await _conversationService.GetByIdAsync(id);
        if (conversation == null) return NotFound();
        return Ok(MapConversation(conversation));
    }

    /// <summary>Admin: get transcript by conversation primary key.</summary>
    [Authorize]
    [HttpGet("admin/{id:int}/transcript")]
    [ProducesResponseType(typeof(ConversationTranscriptDto), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> GetTranscriptById(int id)
    {
        var conversation = await _conversationService.GetByIdAsync(id);
        if (conversation == null) return NotFound();

        var transcript = await _conversationService.BuildTranscriptAsync(conversation.SessionId);
        return Ok(new ConversationTranscriptDto
        {
            SessionId = conversation.SessionId,
            Transcript = transcript
        });
    }

    /// <summary>
    /// Admin: export all conversations as a dataset suitable for training / analytics.
    /// Returns full transcripts, training labels, and linked ticket data.
    /// </summary>
    [Authorize]
    [HttpGet("admin/export")]
    [ProducesResponseType(typeof(IEnumerable<ConversationExportDto>), 200)]
    public async Task<IActionResult> Export()
    {
        var conversations = await _conversationService.GetAllForExportAsync();
        var result = new List<ConversationExportDto>();

        foreach (var c in conversations)
        {
            var transcript = await _conversationService.BuildTranscriptAsync(c.SessionId);
            result.Add(MapExport(c, transcript));
        }

        return Ok(result);
    }

    // ── Mappers ───────────────────────────────────────────────────────────────

    /// <summary>
    /// Strips newline and carriage-return characters from a user-provided value
    /// so that it cannot inject extra lines into structured log output (log forging).
    /// </summary>
    private static string SanitizeForLog(string? value) =>
        value?.Replace('\n', ' ').Replace('\r', ' ') ?? string.Empty;

    private static ConversationDto MapConversation(Core.Entities.Conversations.Conversation c) => new()
    {
        Id = c.Id,
        SessionId = c.SessionId,
        TenantId = c.TenantId,
        BotId = c.BotId,
        SeatSlug = c.SeatSlug,
        SourceUrl = c.SourceUrl,
        Language = c.Language,
        VisitorName = c.VisitorName,
        VisitorEmail = c.VisitorEmail,
        Status = c.Status.ToString(),
        IsResolved = c.IsResolved,
        WasEscalated = c.WasEscalated,
        IsTicketCreated = c.IsTicketCreated,
        TicketId = c.TicketId,
        CreatedAt = c.CreatedAt,
        LastActivityAtUtc = c.LastActivityAtUtc,
        UpdatedAt = c.UpdatedAt,
        EndedAt = c.EndedAt,
        Messages = c.Messages.Select(MapMessage).ToList()
    };

    private static ConversationSummaryDto MapSummary(Core.Entities.Conversations.Conversation c) => new()
    {
        Id = c.Id,
        SessionId = c.SessionId,
        TenantId = c.TenantId,
        BotId = c.BotId,
        SeatSlug = c.SeatSlug,
        SourceUrl = c.SourceUrl,
        Language = c.Language,
        VisitorName = c.VisitorName,
        VisitorEmail = c.VisitorEmail,
        Status = c.Status.ToString(),
        IsResolved = c.IsResolved,
        WasEscalated = c.WasEscalated,
        IsTicketCreated = c.IsTicketCreated,
        TicketId = c.TicketId,
        MessageCount = c.Messages.Count,
        CreatedAt = c.CreatedAt,
        LastActivityAtUtc = c.LastActivityAtUtc,
        UpdatedAt = c.UpdatedAt,
        EndedAt = c.EndedAt,
        Summary = c.Summary,
        Sentiment = c.Sentiment,
        SentimentScore = c.SentimentScore,
        Category = c.Category,
        AnswerQuality = c.AnswerQuality,
        ResolutionSource = c.ResolutionSource
    };

    private static ConversationMessageDto MapMessage(Core.Entities.Conversations.ConversationMessage m) => new()
    {
        Id = m.Id,
        SequenceNumber = m.SequenceNumber,
        Role = m.Role,
        Content = m.Content,
        Timestamp = m.Timestamp,
        Model = m.Model,
        TokensInput = m.TokensInput,
        TokensOutput = m.TokensOutput,
        Confidence = m.Confidence
    };

    private static ConversationExportDto MapExport(
        Core.Entities.Conversations.Conversation c,
        string transcript) => new()
    {
        Id = c.Id,
        SessionId = c.SessionId,
        TenantId = c.TenantId,
        BotId = c.BotId,
        SeatSlug = c.SeatSlug,
        SourceUrl = c.SourceUrl,
        Language = c.Language,
        VisitorName = c.VisitorName,
        Status = c.Status.ToString(),
        CreatedAt = c.CreatedAt,
        EndedAt = c.EndedAt,
        MessageCount = c.Messages.Count,
        IsResolved = c.IsResolved,
        WasEscalated = c.WasEscalated,
        IsTicketCreated = c.IsTicketCreated,
        TicketId = c.TicketId,
        Summary = c.Summary,
        Intent = c.Intent,
        Sentiment = c.Sentiment,
        SentimentScore = c.SentimentScore,
        Category = c.Category,
        EscalationReason = c.EscalationReason,
        AnswerQuality = c.AnswerQuality,
        ResolutionSource = c.ResolutionSource,
        Transcript = transcript,
        Ticket = c.Ticket == null ? null : new ExportedTicketDto
        {
            Id = c.Ticket.Id,
            Title = c.Ticket.Title,
            Type = c.Ticket.Type.ToString(),
            Priority = c.Ticket.Priority.ToString(),
            Status = c.Ticket.Status.ToString(),
            AdminNotes = c.Ticket.AdminNotes,
            ResolvedAt = c.Ticket.ResolvedAt,
            CreatedAt = c.Ticket.CreatedAt
        }
    };
}
