using Microsoft.EntityFrameworkCore;
using System.Text.RegularExpressions;
using SiteChatCMS.Core.Entities.Identity;
using SiteChatCMS.Core.Interfaces.Services;
using SiteChatCMS.Infrastructure.Data;
using SiteChatCMS.Shared.DTOs.Bots;

namespace SiteChatCMS.Infrastructure.Services.Bots;

public class BotService : IBotService
{
    private readonly ApplicationDbContext _context;

    public BotService(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<List<BotDto>> GetUserBotsAsync(string userId)
    {
        var bots = await _context.Bots
            .Where(b => b.UserId == userId)
            .OrderByDescending(b => b.CreatedAt)
            .ToListAsync();

        return bots.Select(MapToBotDto).ToList();
    }

    public async Task<BotDto?> GetBotAsync(string botId, string userId)
    {
        var bot = await _context.Bots
            .FirstOrDefaultAsync(b => b.Id == botId && b.UserId == userId);

        return bot == null ? null : MapToBotDto(bot);
    }

    public async Task<BotDto?> GetBotBySeatSlugAsync(string seatSlug)
    {
        var normalizedSlug = seatSlug.Trim().ToLowerInvariant();
        var bot = await _context.Bots
            .FirstOrDefaultAsync(b => b.SeatSlug == normalizedSlug && b.IsActive);

        return bot == null ? null : MapToBotDto(bot);
    }

    public async Task<BotDto> CreateBotAsync(CreateBotDto dto, string userId)
    {
        var user = await _context.Users.FindAsync(userId);
        if (user == null)
        {
            throw new InvalidOperationException("User not found");
        }

        var bot = new Bot
        {
            Id = Guid.NewGuid().ToString(),
            Name = dto.Name,
            Description = dto.Description,
            SiteUrl = dto.SiteUrl,
            SeatSlug = await GenerateUniqueSeatSlugAsync(dto.Name),
            SystemPrompt = dto.SystemPrompt,
            Temperature = dto.Temperature,
            MaxTokens = dto.MaxTokens,
            UserId = userId,
            OrganizationId = user.OrganizationId,
            CreatedAt = DateTime.UtcNow,
            IsActive = true
        };

        _context.Bots.Add(bot);
        await _context.SaveChangesAsync();

        return MapToBotDto(bot);
    }

    public async Task<BotDto?> UpdateBotAsync(string botId, UpdateBotDto dto, string userId)
    {
        var bot = await _context.Bots
            .FirstOrDefaultAsync(b => b.Id == botId && b.UserId == userId);

        if (bot == null)
        {
            return null;
        }

        if (dto.Name != null) bot.Name = dto.Name;
        if (dto.Description != null) bot.Description = dto.Description;
        if (dto.AvatarUrl != null) bot.AvatarUrl = dto.AvatarUrl;
        if (dto.SystemPrompt != null) bot.SystemPrompt = dto.SystemPrompt;
        if (dto.Temperature.HasValue) bot.Temperature = dto.Temperature.Value;
        if (dto.MaxTokens.HasValue) bot.MaxTokens = dto.MaxTokens.Value;
        if (dto.IsActive.HasValue) bot.IsActive = dto.IsActive.Value;
        if (dto.IsPublic.HasValue) bot.IsPublic = dto.IsPublic.Value;
        if (dto.WidgetColor != null) bot.WidgetColor = dto.WidgetColor;
        if (dto.WidgetPosition != null) bot.WidgetPosition = dto.WidgetPosition;

        bot.UpdatedAt = DateTime.UtcNow;
        await _context.SaveChangesAsync();

        return MapToBotDto(bot);
    }

    public async Task<bool> DeleteBotAsync(string botId, string userId)
    {
        var bot = await _context.Bots
            .FirstOrDefaultAsync(b => b.Id == botId && b.UserId == userId);

        if (bot == null)
        {
            return false;
        }

        _context.Bots.Remove(bot);
        await _context.SaveChangesAsync();
        return true;
    }

    public async Task<List<TrainingDocumentDto>> GetTrainingDocumentsAsync(string botId, string userId)
    {
        var bot = await _context.Bots
            .FirstOrDefaultAsync(b => b.Id == botId && b.UserId == userId);

        if (bot == null)
        {
            return new List<TrainingDocumentDto>();
        }

        var documents = await _context.TrainingDocuments
            .Where(d => d.BotId == botId)
            .OrderByDescending(d => d.UploadedAt)
            .ToListAsync();

        return documents.Select(d => new TrainingDocumentDto
        {
            Id = d.Id,
            FileName = d.FileName,
            FileUrl = d.FileUrl,
            FileSize = d.FileSize,
            ContentType = d.ContentType,
            ProcessingStatus = d.ProcessingStatus,
            UploadedAt = d.UploadedAt
        }).ToList();
    }

    public async Task<TrainingDocumentDto> AddTrainingDocumentAsync(string botId, string fileName, string fileUrl, long fileSize, string contentType, string userId)
    {
        var bot = await _context.Bots
            .FirstOrDefaultAsync(b => b.Id == botId && b.UserId == userId);

        if (bot == null)
        {
            throw new InvalidOperationException("Bot not found");
        }

        var document = new TrainingDocument
        {
            Id = Guid.NewGuid().ToString(),
            BotId = botId,
            FileName = fileName,
            FileUrl = fileUrl,
            FileSize = fileSize,
            ContentType = contentType,
            ProcessingStatus = "pending",
            UploadedAt = DateTime.UtcNow,
            CreatedAt = DateTime.UtcNow
        };

        _context.TrainingDocuments.Add(document);
        bot.TrainedDocumentsCount++;
        bot.LastTrainedAt = DateTime.UtcNow;
        await _context.SaveChangesAsync();

        return new TrainingDocumentDto
        {
            Id = document.Id,
            FileName = document.FileName,
            FileUrl = document.FileUrl,
            FileSize = document.FileSize,
            ContentType = document.ContentType,
            ProcessingStatus = document.ProcessingStatus,
            UploadedAt = document.UploadedAt
        };
    }

    public async Task<bool> DeleteTrainingDocumentAsync(string documentId, string userId)
    {
        var document = await _context.TrainingDocuments
            .Include(d => d.Bot)
            .FirstOrDefaultAsync(d => d.Id == documentId && d.Bot!.UserId == userId);

        if (document == null)
        {
            return false;
        }

        if (document.Bot != null)
        {
            document.Bot.TrainedDocumentsCount--;
        }

        _context.TrainingDocuments.Remove(document);
        await _context.SaveChangesAsync();
        return true;
    }

    public async Task<List<TrainingUrlDto>> GetTrainingUrlsAsync(string botId, string userId)
    {
        var bot = await _context.Bots
            .FirstOrDefaultAsync(b => b.Id == botId && b.UserId == userId);

        if (bot == null)
        {
            return new List<TrainingUrlDto>();
        }

        var urls = await _context.TrainingUrls
            .Where(u => u.BotId == botId)
            .OrderByDescending(u => u.AddedAt)
            .ToListAsync();

        return urls.Select(u => new TrainingUrlDto
        {
            Id = u.Id,
            Url = u.Url,
            Title = u.Title,
            ProcessingStatus = u.ProcessingStatus,
            AddedAt = u.AddedAt,
            LastCrawledAt = u.LastCrawledAt
        }).ToList();
    }

    public async Task<TrainingUrlDto> AddTrainingUrlAsync(string botId, AddTrainingUrlDto dto, string userId)
    {
        var bot = await _context.Bots
            .FirstOrDefaultAsync(b => b.Id == botId && b.UserId == userId);

        if (bot == null)
        {
            throw new InvalidOperationException("Bot not found");
        }

        var trainingUrl = new TrainingUrl
        {
            Id = Guid.NewGuid().ToString(),
            BotId = botId,
            Url = dto.Url,
            ProcessingStatus = "pending",
            AddedAt = DateTime.UtcNow,
            CreatedAt = DateTime.UtcNow
        };

        _context.TrainingUrls.Add(trainingUrl);
        bot.TrainedUrlsCount++;
        bot.LastTrainedAt = DateTime.UtcNow;
        await _context.SaveChangesAsync();

        return new TrainingUrlDto
        {
            Id = trainingUrl.Id,
            Url = trainingUrl.Url,
            Title = trainingUrl.Title,
            ProcessingStatus = trainingUrl.ProcessingStatus,
            AddedAt = trainingUrl.AddedAt,
            LastCrawledAt = trainingUrl.LastCrawledAt
        };
    }

    public async Task<bool> DeleteTrainingUrlAsync(string urlId, string userId)
    {
        var url = await _context.TrainingUrls
            .Include(u => u.Bot)
            .FirstOrDefaultAsync(u => u.Id == urlId && u.Bot!.UserId == userId);

        if (url == null)
        {
            return false;
        }

        if (url.Bot != null)
        {
            url.Bot.TrainedUrlsCount--;
        }

        _context.TrainingUrls.Remove(url);
        await _context.SaveChangesAsync();
        return true;
    }

    public async Task<string> GenerateEmbedCodeAsync(string botId, string userId)
    {
        var bot = await _context.Bots
            .FirstOrDefaultAsync(b => b.Id == botId && b.UserId == userId);

        if (bot == null)
        {
            throw new InvalidOperationException("Bot not found");
        }

        var embedCode = $@"<!-- SiteChat Agent Chatbot Widget -->
<script src=""https://your-domain.com/widget/sitechat-widget.js""></script>
<script data-seat-id=""{botId}"">
  SiteChatWidget.init({{
    seatId: '{botId}',
    botId: '{botId}',
    apiUrl: 'https://your-domain.com/api',
    position: '{bot.WidgetPosition ?? "bottom-right"}',
    color: '{bot.WidgetColor ?? "#4CAF50"}'
  }});
</script>";

        bot.EmbedCode = embedCode;
        await _context.SaveChangesAsync();

        return embedCode;
    }

    private BotDto MapToBotDto(Bot bot)
    {
        return new BotDto
        {
            Id = bot.Id,
            Name = bot.Name,
            Description = bot.Description,
            SiteUrl = bot.SiteUrl,
            SeatSlug = bot.SeatSlug,
            AvatarUrl = bot.AvatarUrl,
            SystemPrompt = bot.SystemPrompt,
            Temperature = bot.Temperature,
            MaxTokens = bot.MaxTokens,
            IsActive = bot.IsActive,
            IsPublic = bot.IsPublic,
            TrainedDocumentsCount = bot.TrainedDocumentsCount,
            TrainedUrlsCount = bot.TrainedUrlsCount,
            LastTrainedAt = bot.LastTrainedAt,
            WidgetColor = bot.WidgetColor,
            WidgetPosition = bot.WidgetPosition,
            EmbedCode = bot.EmbedCode,
            CreatedAt = bot.CreatedAt
        };
    }

    private async Task<string> GenerateUniqueSeatSlugAsync(string botName)
    {
        var baseSlug = Regex.Replace(botName.ToLowerInvariant(), @"[^a-z0-9]+", "-").Trim('-');
        if (string.IsNullOrWhiteSpace(baseSlug))
        {
            baseSlug = "seat";
        }

        var slug = baseSlug;
        var counter = 2;

        while (await _context.Bots.AnyAsync(b => b.SeatSlug == slug))
        {
            slug = $"{baseSlug}-{counter}";
            counter++;
        }

        return slug;
    }
}
