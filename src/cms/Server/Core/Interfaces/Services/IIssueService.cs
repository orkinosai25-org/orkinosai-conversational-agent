using SiteChatCMS.Core.Entities.Issues;

namespace SiteChatCMS.Core.Interfaces.Services;

/// <summary>
/// Service for managing support issues
/// </summary>
public interface IIssueService
{
    // ── Issue CRUD ───────────────────────────────────────────────────────────

    /// <summary>Returns all issues (admin view)</summary>
    Task<IEnumerable<Issue>> GetAllIssuesAsync();

    /// <summary>Returns issues filtered by status</summary>
    Task<IEnumerable<Issue>> GetIssuesByStatusAsync(IssueStatus status);

    /// <summary>Returns a single issue by ID, or null if not found</summary>
    Task<Issue?> GetIssueByIdAsync(int id);

    /// <summary>Creates a new issue (status defaults to Open)</summary>
    Task<Issue> CreateIssueAsync(Issue issue);

    /// <summary>Updates fields on an existing issue</summary>
    Task<Issue> UpdateIssueAsync(Issue issue);

    /// <summary>Deletes an issue; returns false if not found</summary>
    Task<bool> DeleteIssueAsync(int id);

    // ── Admin workflow ───────────────────────────────────────────────────────

    /// <summary>Sets an issue's status to InProgress</summary>
    Task<bool> StartIssueAsync(int id);

    /// <summary>Sets an issue's status to Resolved</summary>
    Task<bool> ResolveIssueAsync(int id, string? adminNotes = null);

    /// <summary>Sets an issue's status to Closed</summary>
    Task<bool> CloseIssueAsync(int id);
}
