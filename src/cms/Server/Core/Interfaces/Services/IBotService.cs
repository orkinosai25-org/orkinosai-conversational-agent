using PapaganCMS.Core.Entities.Identity;
using PapaganCMS.Shared.DTOs.Bots;

namespace PapaganCMS.Core.Interfaces.Services;

public interface IBotService
{
    Task<List<BotDto>> GetUserBotsAsync(string userId);
    Task<BotDto?> GetBotAsync(string botId, string userId);
    Task<BotDto?> GetBotBySeatSlugAsync(string seatSlug);
    Task<BotDto> CreateBotAsync(CreateBotDto dto, string userId);
    Task<BotDto?> UpdateBotAsync(string botId, UpdateBotDto dto, string userId);
    Task<bool> DeleteBotAsync(string botId, string userId);
    Task<List<TrainingDocumentDto>> GetTrainingDocumentsAsync(string botId, string userId);
    Task<TrainingDocumentDto> AddTrainingDocumentAsync(string botId, string fileName, string fileUrl, long fileSize, string contentType, string userId);
    Task<bool> DeleteTrainingDocumentAsync(string documentId, string userId);
    Task<List<TrainingUrlDto>> GetTrainingUrlsAsync(string botId, string userId);
    Task<TrainingUrlDto> AddTrainingUrlAsync(string botId, AddTrainingUrlDto dto, string userId);
    Task<bool> DeleteTrainingUrlAsync(string urlId, string userId);
    Task<string> GenerateEmbedCodeAsync(string botId, string userId);
}
