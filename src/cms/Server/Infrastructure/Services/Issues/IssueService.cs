using SiteChatCMS.Core.Entities.Issues;
using SiteChatCMS.Core.Interfaces.Services;

namespace SiteChatCMS.Infrastructure.Services.Issues;

/// <summary>
/// In-memory implementation of IIssueService.
/// TODO: Replace with database-backed implementation for production.
/// </summary>
public class IssueService : IIssueService
{
    private readonly List<Issue> _issues = new();
    private readonly object _syncLock = new();
    private int _nextId = 1;

    public IssueService()
    {
        SeedSampleIssues();
    }

    private void SeedSampleIssues()
    {
        var now = DateTime.UtcNow;

        _issues.AddRange(new[]
        {
            new Issue
            {
                Id = _nextId++,
                Title = "Chat widget not loading on mobile",
                Description = "The chat widget fails to initialise on iOS Safari 17. Console shows a CORS error.",
                Type = IssueType.Bug,
                Priority = IssuePriority.High,
                Status = IssueStatus.Open,
                SubmitterName = "Alice Johnson",
                SubmitterEmail = "alice@example.com",
                CreatedAt = now.AddDays(-3)
            },
            new Issue
            {
                Id = _nextId++,
                Title = "Add dark mode support",
                Description = "It would be great to have a dark theme option for the admin dashboard and the embed widget.",
                Type = IssueType.FeatureRequest,
                Priority = IssuePriority.Medium,
                Status = IssueStatus.InProgress,
                SubmitterName = "Bob Smith",
                SubmitterEmail = "bob@example.com",
                AdminNotes = "Accepted for next sprint. CSS variables already in place.",
                CreatedAt = now.AddDays(-7)
            },
            new Issue
            {
                Id = _nextId++,
                Title = "How do I export conversation history?",
                Description = "I can see conversations in the dashboard but cannot find an export button. Is this feature available?",
                Type = IssueType.Question,
                Priority = IssuePriority.Low,
                Status = IssueStatus.Resolved,
                SubmitterName = "Carol White",
                SubmitterEmail = "carol@example.com",
                AdminNotes = "Export is on the roadmap. Advised customer to copy transcripts manually for now.",
                ResolvedAt = now.AddDays(-1),
                CreatedAt = now.AddDays(-5)
            }
        });
    }

    // ── IIssueService implementation ─────────────────────────────────────────

    public Task<IEnumerable<Issue>> GetAllIssuesAsync() =>
        Task.FromResult<IEnumerable<Issue>>(_issues.OrderByDescending(i => i.CreatedAt).ToList());

    public Task<IEnumerable<Issue>> GetIssuesByStatusAsync(IssueStatus status)
    {
        var filtered = _issues.Where(i => i.Status == status).OrderByDescending(i => i.CreatedAt).ToList();
        return Task.FromResult<IEnumerable<Issue>>(filtered);
    }

    public Task<Issue?> GetIssueByIdAsync(int id) =>
        Task.FromResult(_issues.FirstOrDefault(i => i.Id == id));

    public Task<Issue> CreateIssueAsync(Issue issue)
    {
        lock (_syncLock)
        {
            issue.Id = _nextId++;
            issue.CreatedAt = DateTime.UtcNow;
            issue.Status = IssueStatus.Open;
            _issues.Add(issue);
        }
        return Task.FromResult(issue);
    }

    public Task<Issue> UpdateIssueAsync(Issue issue)
    {
        lock (_syncLock)
        {
            var index = _issues.FindIndex(i => i.Id == issue.Id);
            if (index < 0)
                return Task.FromException<Issue>(new KeyNotFoundException($"Issue {issue.Id} not found."));

            issue.UpdatedAt = DateTime.UtcNow;
            _issues[index] = issue;
            return Task.FromResult(issue);
        }
    }

    public Task<bool> DeleteIssueAsync(int id)
    {
        lock (_syncLock)
        {
            var issue = _issues.FirstOrDefault(i => i.Id == id);
            if (issue == null) return Task.FromResult(false);
            _issues.Remove(issue);
            return Task.FromResult(true);
        }
    }

    public Task<bool> StartIssueAsync(int id)
    {
        lock (_syncLock)
        {
            var issue = _issues.FirstOrDefault(i => i.Id == id);
            if (issue == null) return Task.FromResult(false);
            issue.Status = IssueStatus.InProgress;
            issue.UpdatedAt = DateTime.UtcNow;
            return Task.FromResult(true);
        }
    }

    public Task<bool> ResolveIssueAsync(int id, string? adminNotes = null)
    {
        lock (_syncLock)
        {
            var issue = _issues.FirstOrDefault(i => i.Id == id);
            if (issue == null) return Task.FromResult(false);
            issue.Status = IssueStatus.Resolved;
            issue.ResolvedAt = DateTime.UtcNow;
            issue.UpdatedAt = DateTime.UtcNow;
            if (adminNotes != null)
                issue.AdminNotes = adminNotes;
            return Task.FromResult(true);
        }
    }

    public Task<bool> CloseIssueAsync(int id)
    {
        lock (_syncLock)
        {
            var issue = _issues.FirstOrDefault(i => i.Id == id);
            if (issue == null) return Task.FromResult(false);
            issue.Status = IssueStatus.Closed;
            issue.UpdatedAt = DateTime.UtcNow;
            return Task.FromResult(true);
        }
    }
}
