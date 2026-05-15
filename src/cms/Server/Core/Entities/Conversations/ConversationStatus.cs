namespace SiteChatCMS.Core.Entities.Conversations;

/// <summary>
/// Lifecycle state of a SiteChat conversation session.
/// </summary>
public enum ConversationStatus
{
    /// <summary>Conversation is in progress.</summary>
    Active = 0,

    /// <summary>Conversation ended and the AI answered the visitor's query.</summary>
    Resolved = 1,

    /// <summary>Conversation ended but the query was not resolved by the AI.</summary>
    Unresolved = 2,

    /// <summary>Conversation was escalated to a human agent or support ticket.</summary>
    Escalated = 3,

    /// <summary>Conversation is closed (no further action required).</summary>
    Closed = 4
}
