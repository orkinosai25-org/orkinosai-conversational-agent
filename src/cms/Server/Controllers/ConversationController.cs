using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SiteChatCMS.Core.Interfaces.Services;
using SiteChatCMS.Shared.DTOs.Conversations;

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
    private readonly ILogger<ConversationController> _logger;

    public ConversationController(
        IConversationService conversationService,
        ILogger<ConversationController> logger)
    {
        _conversationService = conversationService;
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
                dto.BotId,
                dto.SeatSlug,
                dto.SourceUrl,
                dto.Language,
                dto.VisitorName,
                dto.VisitorEmail);

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
    /// Append a message (user or assistant) to an existing conversation.
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
        if (!dto.Role.Equals("user", StringComparison.OrdinalIgnoreCase) &&
            !dto.Role.Equals("assistant", StringComparison.OrdinalIgnoreCase))
            return BadRequest("Role must be 'user' or 'assistant'.");

        try
        {
            var message = await _conversationService.AddMessageAsync(
                sessionId, dto.Role, dto.Content, botId, seatSlug);

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
        BotId = c.BotId,
        SeatSlug = c.SeatSlug,
        SourceUrl = c.SourceUrl,
        Language = c.Language,
        VisitorName = c.VisitorName,
        VisitorEmail = c.VisitorEmail,
        IsResolved = c.IsResolved,
        IsTicketCreated = c.IsTicketCreated,
        TicketId = c.TicketId,
        CreatedAt = c.CreatedAt,
        UpdatedAt = c.UpdatedAt,
        EndedAt = c.EndedAt,
        Messages = c.Messages.Select(MapMessage).ToList()
    };

    private static ConversationSummaryDto MapSummary(Core.Entities.Conversations.Conversation c) => new()
    {
        Id = c.Id,
        SessionId = c.SessionId,
        BotId = c.BotId,
        SeatSlug = c.SeatSlug,
        SourceUrl = c.SourceUrl,
        Language = c.Language,
        VisitorName = c.VisitorName,
        IsResolved = c.IsResolved,
        IsTicketCreated = c.IsTicketCreated,
        TicketId = c.TicketId,
        MessageCount = c.Messages.Count,
        CreatedAt = c.CreatedAt,
        UpdatedAt = c.UpdatedAt,
        EndedAt = c.EndedAt
    };

    private static ConversationMessageDto MapMessage(Core.Entities.Conversations.ConversationMessage m) => new()
    {
        Id = m.Id,
        Role = m.Role,
        Content = m.Content,
        Timestamp = m.Timestamp
    };
}
