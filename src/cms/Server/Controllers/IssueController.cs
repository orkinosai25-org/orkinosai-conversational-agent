using Microsoft.AspNetCore.Mvc;
using SiteChatCMS.Core.Entities.Issues;
using SiteChatCMS.Core.Interfaces.Services;
using SiteChatCMS.Infrastructure.Services.Issues;
using SiteChatCMS.Shared.DTOs.Issues;

namespace SiteChatCMS.Controllers;

/// <summary>
/// API controller for support issue management.
/// Admin endpoints are prefixed with /api/issue/admin.
/// Public endpoints are prefixed with /api/issue.
/// </summary>
[ApiController]
[Route("api/[controller]")]
public class IssueController : ControllerBase
{
    private readonly IIssueService _issueService;
    private readonly ILogger<IssueController> _logger;

    public IssueController(IIssueService issueService, ILogger<IssueController> logger)
    {
        _issueService = issueService;
        _logger = logger;
    }

    // ── Public endpoints ─────────────────────────────────────────────────────

    /// <summary>Submit a new support issue</summary>
    [HttpPost]
    [ProducesResponseType(typeof(IssueDto), 201)]
    [ProducesResponseType(400)]
    public async Task<IActionResult> CreateIssue([FromBody] CreateIssueDto dto)
    {
        try
        {
            if (string.IsNullOrWhiteSpace(dto.Title))
                return BadRequest("Title is required.");
            if (string.IsNullOrWhiteSpace(dto.Description))
                return BadRequest("Description is required.");
            if (string.IsNullOrWhiteSpace(dto.SubmitterEmail))
                return BadRequest("Email is required.");

            if (!Enum.TryParse<IssueType>(dto.Type, out var type))
                type = IssueType.Other;

            if (!Enum.TryParse<IssuePriority>(dto.Priority, out var priority))
                priority = IssuePriority.Medium;

            var issue = new Issue
            {
                Title = dto.Title,
                Description = dto.Description,
                Type = type,
                Priority = priority,
                SubmitterName = dto.SubmitterName,
                SubmitterEmail = dto.SubmitterEmail
            };

            var created = await _issueService.CreateIssueAsync(issue);
            return CreatedAtAction(nameof(GetIssue), new { id = created.Id }, MapIssue(created));
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating issue");
            return StatusCode(500, "An error occurred while submitting the issue.");
        }
    }

    /// <summary>
    /// Auto-create a support ticket from a SiteChat conversation transcript.
    /// The transcript is analysed for sentiment, summarised, and classified by
    /// type and priority — no external AI service is required.
    /// </summary>
    [HttpPost("from-conversation")]
    [ProducesResponseType(typeof(ConversationTicketResult), 201)]
    [ProducesResponseType(400)]
    public async Task<IActionResult> CreateFromConversation([FromBody] ConversationToTicketDto dto)
    {
        if (string.IsNullOrWhiteSpace(dto.Transcript))
            return BadRequest("Conversation transcript is required.");
        if (string.IsNullOrWhiteSpace(dto.SubmitterEmail))
            return BadRequest("Submitter email is required.");

        try
        {
            // ── AI analysis ────────────────────────────────────────────────────
            var (sentiment, sentimentScore) = ConversationAnalyser.DetectSentiment(dto.Transcript);
            var summary = ConversationAnalyser.Summarise(dto.Transcript);
            var detectedType = ConversationAnalyser.DetectType(dto.Transcript);
            var detectedPriority = ConversationAnalyser.DetectPriority(dto.Transcript);

            if (!Enum.TryParse<IssueType>(detectedType, out var issueType))
                issueType = IssueType.Other;
            if (!Enum.TryParse<IssuePriority>(detectedPriority, out var issuePriority))
                issuePriority = IssuePriority.Medium;

            // Use the summary as the ticket title (capped at 100 chars)
            var title = summary.Length > 100 ? summary[..97] + "…" : summary;

            // Persist AI analysis in AdminNotes so admins see it immediately
            var adminNotes = $"{ConversationAnalyser.SummaryPrefix} {summary}\n{ConversationAnalyser.SentimentPrefix} {sentiment} ({sentimentScore:P0})";
            if (!string.IsNullOrWhiteSpace(dto.SourceUrl))
                adminNotes += $"\n[Source] {dto.SourceUrl}";

            var issue = new Issue
            {
                Title = title,
                Description = dto.Transcript,
                Type = issueType,
                Priority = issuePriority,
                SubmitterName = dto.SubmitterName ?? "SiteChat Visitor",
                SubmitterEmail = dto.SubmitterEmail,
                AdminNotes = adminNotes
            };

            var created = await _issueService.CreateIssueAsync(issue);

            var result = new ConversationTicketResult
            {
                Ticket = MapIssue(created),
                Sentiment = sentiment,
                SentimentScore = sentimentScore,
                Summary = summary,
                DetectedType = detectedType,
                DetectedPriority = detectedPriority
            };

            return CreatedAtAction(nameof(GetIssue), new { id = created.Id }, result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating ticket from conversation");
            return StatusCode(500, "An error occurred while processing the conversation.");
        }
    }

    /// <summary>Get a single issue by ID</summary>
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(IssueDto), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> GetIssue(int id)
    {
        var issue = await _issueService.GetIssueByIdAsync(id);
        if (issue == null) return NotFound();
        return Ok(MapIssue(issue));
    }

    // ── Admin endpoints ──────────────────────────────────────────────────────

    /// <summary>Admin: get all issues</summary>
    [HttpGet("admin/all")]
    [ProducesResponseType(typeof(IEnumerable<IssueDto>), 200)]
    public async Task<IActionResult> GetAllIssues()
    {
        var issues = await _issueService.GetAllIssuesAsync();
        return Ok(issues.Select(MapIssue));
    }

    /// <summary>Admin: get issues filtered by status</summary>
    [HttpGet("admin/status/{status}")]
    [ProducesResponseType(typeof(IEnumerable<IssueDto>), 200)]
    [ProducesResponseType(400)]
    public async Task<IActionResult> GetIssuesByStatus(string status)
    {
        if (!Enum.TryParse<IssueStatus>(status, true, out var statusEnum))
            return BadRequest("Invalid status value.");

        var issues = await _issueService.GetIssuesByStatusAsync(statusEnum);
        return Ok(issues.Select(MapIssue));
    }

    /// <summary>Admin: get dashboard statistics</summary>
    [HttpGet("admin/stats")]
    [ProducesResponseType(typeof(IssueStatsDto), 200)]
    public async Task<IActionResult> GetStats()
    {
        var issues = (await _issueService.GetAllIssuesAsync()).ToList();
        var stats = new IssueStatsDto
        {
            TotalIssues = issues.Count,
            OpenIssues = issues.Count(i => i.Status == IssueStatus.Open),
            InProgressIssues = issues.Count(i => i.Status == IssueStatus.InProgress),
            ResolvedIssues = issues.Count(i => i.Status == IssueStatus.Resolved),
            ClosedIssues = issues.Count(i => i.Status == IssueStatus.Closed),
            CriticalIssues = issues.Count(i => i.Priority == IssuePriority.Critical)
        };
        return Ok(stats);
    }

    /// <summary>Admin: update an issue</summary>
    [HttpPut("admin/{id:int}")]
    [ProducesResponseType(typeof(IssueDto), 200)]
    [ProducesResponseType(400)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> UpdateIssue(int id, [FromBody] UpdateIssueDto dto)
    {
        try
        {
            var existing = await _issueService.GetIssueByIdAsync(id);
            if (existing == null) return NotFound();

            existing.Title = dto.Title;
            existing.Description = dto.Description;
            existing.AdminNotes = dto.AdminNotes;

            if (!string.IsNullOrEmpty(dto.Type) && Enum.TryParse<IssueType>(dto.Type, out var type))
                existing.Type = type;

            if (!string.IsNullOrEmpty(dto.Priority) && Enum.TryParse<IssuePriority>(dto.Priority, out var priority))
                existing.Priority = priority;

            if (!string.IsNullOrEmpty(dto.Status) && Enum.TryParse<IssueStatus>(dto.Status, out var status))
                existing.Status = status;

            var updated = await _issueService.UpdateIssueAsync(existing);
            return Ok(MapIssue(updated));
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error updating issue {IssueId}", id);
            return StatusCode(500, "An error occurred while updating the issue.");
        }
    }

    /// <summary>Admin: delete an issue</summary>
    [HttpDelete("admin/{id:int}")]
    [ProducesResponseType(204)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> DeleteIssue(int id)
    {
        var deleted = await _issueService.DeleteIssueAsync(id);
        if (!deleted) return NotFound();
        return NoContent();
    }

    /// <summary>Admin: mark an issue as in-progress</summary>
    [HttpPost("admin/{id:int}/start")]
    [ProducesResponseType(204)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> StartIssue(int id)
    {
        var success = await _issueService.StartIssueAsync(id);
        if (!success) return NotFound();
        return NoContent();
    }

    /// <summary>Admin: resolve an issue</summary>
    [HttpPost("admin/{id:int}/resolve")]
    [ProducesResponseType(204)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> ResolveIssue(int id, [FromBody] ResolveIssueDto? dto = null)
    {
        var success = await _issueService.ResolveIssueAsync(id, dto?.AdminNotes);
        if (!success) return NotFound();
        return NoContent();
    }

    /// <summary>Admin: close an issue</summary>
    [HttpPost("admin/{id:int}/close")]
    [ProducesResponseType(204)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> CloseIssue(int id)
    {
        var success = await _issueService.CloseIssueAsync(id);
        if (!success) return NotFound();
        return NoContent();
    }

    // ── Mapper ───────────────────────────────────────────────────────────────

    private static IssueDto MapIssue(Issue issue) => new()
    {
        Id = issue.Id,
        Title = issue.Title,
        Description = issue.Description,
        Type = issue.Type.ToString(),
        Priority = issue.Priority.ToString(),
        Status = issue.Status.ToString(),
        SubmitterName = issue.SubmitterName,
        SubmitterEmail = issue.SubmitterEmail,
        AdminNotes = issue.AdminNotes,
        ResolvedAt = issue.ResolvedAt,
        CreatedAt = issue.CreatedAt,
        UpdatedAt = issue.UpdatedAt
    };
}
