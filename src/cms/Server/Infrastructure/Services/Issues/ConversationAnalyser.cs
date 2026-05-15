namespace SiteChatCMS.Infrastructure.Services.Issues;

/// <summary>
/// Rule-based conversation analyser for sentiment detection, extractive summarisation,
/// and issue type / priority classification. Used when converting a SiteChat transcript
/// into a support ticket without calling an external AI service.
/// </summary>
internal static class ConversationAnalyser
{
    // ── AI analysis markers ────────────────────────────────────────────────────

    /// <summary>Prefix written to AdminNotes for the extractive summary line.</summary>
    public const string SummaryPrefix = "[AI Summary]";

    /// <summary>Prefix written to AdminNotes for the sentiment line.</summary>
    public const string SentimentPrefix = "[Sentiment]";

    // ── Priority thresholds ────────────────────────────────────────────────────

    private const int HighPriorityNegativeThreshold = 5;
    private const int MediumPriorityNegativeThreshold = 2;

    // ── Keyword lists ──────────────────────────────────────────────────────────

    private static readonly string[] PositiveWords =
    [
        "thank", "thanks", "great", "excellent", "wonderful", "love", "happy",
        "please", "appreciate", "helpful", "resolved", "working", "perfect",
        "awesome", "fantastic", "brilliant", "glad", "satisfied", "pleased"
    ];

    private static readonly string[] NegativeWords =
    [
        "broken", "error", "crash", "fail", "failure", "not working", "bug",
        "problem", "issue", "wrong", "bad", "terrible", "awful", "urgent",
        "critical", "cannot", "can't", "doesn't", "don't", "won't", "frustrat",
        "disappoint", "horrible", "stuck", "blocked", "slow", "timeout", "hang"
    ];

    private static readonly string[] BugKeywords =
    [
        "error", "crash", "bug", "broken", "fail", "exception", "stack trace",
        "not working", "doesn't work", "won't load", "blank screen", "500", "404",
        "keeps crashing", "freezing", "infinite loop", "null reference"
    ];

    private static readonly string[] FeatureKeywords =
    [
        "feature", "add", "enhance", "improve", "would like", "wish", "want",
        "suggest", "request", "could you add", "can you add", "it would be nice",
        "roadmap", "support for", "allow us to", "please add"
    ];

    private static readonly string[] QuestionKeywords =
    [
        "how do", "how can", "what is", "where is", "when will", "why does",
        "is there", "does it", "can i", "how to", "help me understand",
        "i don't understand", "what does", "where do", "who can"
    ];

    private static readonly string[] UrgentKeywords =
    [
        "critical", "urgent", "immediately", "asap", "down", "outage",
        "all users", "production", "can't work", "blocked", "emergency",
        "losing data", "data loss", "security breach", "breach"
    ];

    // ── Public API ─────────────────────────────────────────────────────────────

    /// <summary>
    /// Scores the sentiment of <paramref name="text"/> based on keyword counts.
    /// Returns a label (Positive / Negative / Mixed / Neutral) and a confidence
    /// score in the range 0.0 – 1.0 where 1.0 means fully positive.
    /// </summary>
    public static (string Label, double Score) DetectSentiment(string text)
    {
        var lower = text.ToLowerInvariant();
        var pos = PositiveWords.Count(w => lower.Contains(w));
        var neg = NegativeWords.Count(w => lower.Contains(w));
        var total = pos + neg;

        if (total == 0) return ("Neutral", 0.5);

        var score = (double)pos / total;
        return score switch
        {
            >= 0.7 => ("Positive", score),
            <= 0.3 => ("Negative", score),
            _ => ("Mixed", score)
        };
    }

    /// <summary>
    /// Produces an extractive summary of a conversation transcript by selecting
    /// the highest-scoring sentences (by keyword density) up to
    /// <paramref name="maxSentences"/> sentences.
    /// </summary>
    public static string Summarise(string transcript, int maxSentences = 3)
    {
        var sentences = transcript
            .Split(['.', '!', '?', '\n'], StringSplitOptions.RemoveEmptyEntries)
            .Select(s => s.Trim())
            .Where(s => s.Length > 20)
            .ToList();

        if (sentences.Count <= maxSentences)
            return string.Join(". ", sentences).Trim() + ".";

        // Build a single keyword set to avoid repeated concat on each sentence
        var allKeywords = BugKeywords
            .Concat(FeatureKeywords)
            .Concat(QuestionKeywords)
            .Concat(UrgentKeywords)
            .ToArray();

        var scored = sentences
            .Select(s =>
            {
                var lower = s.ToLowerInvariant();
                var score = allKeywords.Count(k => lower.Contains(k));
                return (Sentence: s, Score: score);
            })
            .OrderByDescending(x => x.Score)
            .Take(maxSentences)
            .ToList();

        // Restore original order before joining
        var result = scored
            .OrderBy(x => sentences.IndexOf(x.Sentence))
            .Select(x => x.Sentence);

        return string.Join(". ", result).Trim() + ".";
    }

    /// <summary>
    /// Classifies the conversation as Bug / FeatureRequest / Question / Other
    /// using a scoring approach so that the type with the most keyword matches wins,
    /// rather than the first match.  Returns the IssueType string value.
    /// </summary>
    public static string DetectType(string text)
    {
        var lower = text.ToLowerInvariant();

        var scores = new Dictionary<string, int>
        {
            ["Bug"] = BugKeywords.Count(w => lower.Contains(w)),
            ["FeatureRequest"] = FeatureKeywords.Count(w => lower.Contains(w)),
            ["Question"] = QuestionKeywords.Count(w => lower.Contains(w))
        };

        var best = scores.OrderByDescending(kv => kv.Value).First();
        return best.Value > 0 ? best.Key : "Other";
    }

    /// <summary>
    /// Estimates the urgency of a conversation as Critical / High / Medium / Low
    /// based on keyword matching and negative-word density.
    /// </summary>
    public static string DetectPriority(string text)
    {
        var lower = text.ToLowerInvariant();
        if (UrgentKeywords.Any(w => lower.Contains(w))) return "Critical";
        var negCount = NegativeWords.Count(w => lower.Contains(w));
        return negCount switch
        {
            >= HighPriorityNegativeThreshold => "High",
            >= MediumPriorityNegativeThreshold => "Medium",
            _ => "Low"
        };
    }
}
