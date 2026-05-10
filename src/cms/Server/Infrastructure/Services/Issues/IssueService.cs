using Microsoft.EntityFrameworkCore;
using SiteChatCMS.Core.Entities.Issues;
using SiteChatCMS.Core.Interfaces.Services;
using SiteChatCMS.Infrastructure.Data;

namespace SiteChatCMS.Infrastructure.Services.Issues;

/// <summary>
/// EF Core-backed implementation of IIssueService.
/// Persists support issues to Azure SQL Database via ApplicationDbContext.
/// </summary>
public class IssueService : IIssueService
{
    private readonly ApplicationDbContext _db;

    public IssueService(ApplicationDbContext db)
    {
        _db = db;
    }

    // ── IIssueService implementation ─────────────────────────────────────────

    public async Task<IEnumerable<Issue>> GetAllIssuesAsync() =>
        await _db.Issues
            .OrderByDescending(i => i.CreatedAt)
            .ToListAsync();

    public async Task<IEnumerable<Issue>> GetIssuesByStatusAsync(IssueStatus status) =>
        await _db.Issues
            .Where(i => i.Status == status)
            .OrderByDescending(i => i.CreatedAt)
            .ToListAsync();

    public async Task<Issue?> GetIssueByIdAsync(int id) =>
        await _db.Issues.FindAsync(id);

    public async Task<Issue> CreateIssueAsync(Issue issue)
    {
        issue.CreatedAt = DateTime.UtcNow;
        issue.Status = IssueStatus.Open;
        _db.Issues.Add(issue);
        await _db.SaveChangesAsync();
        return issue;
    }

    public async Task<Issue> UpdateIssueAsync(Issue issue)
    {
        var existing = await _db.Issues.FindAsync(issue.Id)
            ?? throw new KeyNotFoundException($"Issue {issue.Id} not found.");

        // Copy all mutable fields via EF's value-setter so the tracked entity
        // reflects the incoming data; EF will only emit a SET for changed columns.
        _db.Entry(existing).CurrentValues.SetValues(issue);

        // Preserve immutable fields that must not be overwritten by the caller.
        existing.Id = issue.Id;
        existing.CreatedAt = existing.CreatedAt;  // keep original creation timestamp
        existing.UpdatedAt = DateTime.UtcNow;

        try
        {
            await _db.SaveChangesAsync();
        }
        catch (DbUpdateConcurrencyException ex)
        {
            throw new InvalidOperationException(
                $"Issue {issue.Id} was modified by another request. Reload and retry.", ex);
        }

        return existing;
    }

    public async Task<bool> DeleteIssueAsync(int id)
    {
        var issue = await _db.Issues.FindAsync(id);
        if (issue == null) return false;

        _db.Issues.Remove(issue);
        await _db.SaveChangesAsync();
        return true;
    }

    public async Task<bool> StartIssueAsync(int id)
    {
        var issue = await _db.Issues.FindAsync(id);
        if (issue == null) return false;

        issue.Status = IssueStatus.InProgress;
        issue.UpdatedAt = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return true;
    }

    public async Task<bool> ResolveIssueAsync(int id, string? adminNotes = null)
    {
        var issue = await _db.Issues.FindAsync(id);
        if (issue == null) return false;

        issue.Status = IssueStatus.Resolved;
        issue.ResolvedAt = DateTime.UtcNow;
        issue.UpdatedAt = DateTime.UtcNow;
        if (adminNotes != null)
            issue.AdminNotes = adminNotes;
        await _db.SaveChangesAsync();
        return true;
    }

    public async Task<bool> CloseIssueAsync(int id)
    {
        var issue = await _db.Issues.FindAsync(id);
        if (issue == null) return false;

        issue.Status = IssueStatus.Closed;
        issue.UpdatedAt = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return true;
    }
}
