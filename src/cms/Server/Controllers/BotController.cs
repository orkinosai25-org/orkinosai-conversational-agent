using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using PapaganCMS.Core.Interfaces.Services;
using PapaganCMS.Shared.DTOs.Bots;

namespace PapaganCMS.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class BotController : ControllerBase
{
    private readonly IBotService _botService;
    private readonly IAuthService _authService;
    private readonly ILogger<BotController> _logger;

    public BotController(IBotService botService, IAuthService authService, ILogger<BotController> logger)
    {
        _botService = botService;
        _authService = authService;
        _logger = logger;
    }

    [HttpGet]
    public async Task<ActionResult<List<BotDto>>> GetBots()
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            var bots = await _botService.GetUserBotsAsync(user.Id);
            return Ok(bots);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting bots");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<BotDto>> GetBot(string id)
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            var bot = await _botService.GetBotAsync(id, user.Id);
            if (bot == null) return NotFound();

            return Ok(bot);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting bot");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }

    [HttpPost]
    public async Task<ActionResult<BotDto>> CreateBot([FromBody] CreateBotDto dto)
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            var bot = await _botService.CreateBotAsync(dto, user.Id);
            return CreatedAtAction(nameof(GetBot), new { id = bot.Id }, bot);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating bot");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }

    [HttpPut("{id}")]
    public async Task<ActionResult<BotDto>> UpdateBot(string id, [FromBody] UpdateBotDto dto)
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            var bot = await _botService.UpdateBotAsync(id, dto, user.Id);
            if (bot == null) return NotFound();

            return Ok(bot);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error updating bot");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }

    [HttpDelete("{id}")]
    public async Task<ActionResult> DeleteBot(string id)
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            var success = await _botService.DeleteBotAsync(id, user.Id);
            if (!success) return NotFound();

            return NoContent();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error deleting bot");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }

    [HttpGet("{id}/documents")]
    public async Task<ActionResult<List<TrainingDocumentDto>>> GetDocuments(string id)
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            var documents = await _botService.GetTrainingDocumentsAsync(id, user.Id);
            return Ok(documents);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting training documents");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }

    [HttpPost("{id}/documents")]
    public async Task<ActionResult<TrainingDocumentDto>> UploadDocument(string id, IFormFile file)
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            if (file == null || file.Length == 0)
            {
                return BadRequest(new { message = "No file provided" });
            }

            // TODO: Implement file storage (Azure Blob Storage, etc.)
            var fileUrl = $"/uploads/{Guid.NewGuid()}_{file.FileName}";

            var document = await _botService.AddTrainingDocumentAsync(
                id,
                file.FileName,
                fileUrl,
                file.Length,
                file.ContentType,
                user.Id
            );

            return Ok(document);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error uploading document");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }

    [HttpDelete("documents/{documentId}")]
    public async Task<ActionResult> DeleteDocument(string documentId)
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            var success = await _botService.DeleteTrainingDocumentAsync(documentId, user.Id);
            if (!success) return NotFound();

            return NoContent();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error deleting document");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }

    [HttpGet("{id}/urls")]
    public async Task<ActionResult<List<TrainingUrlDto>>> GetUrls(string id)
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            var urls = await _botService.GetTrainingUrlsAsync(id, user.Id);
            return Ok(urls);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting training URLs");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }

    [HttpPost("{id}/urls")]
    public async Task<ActionResult<TrainingUrlDto>> AddUrl(string id, [FromBody] AddTrainingUrlDto dto)
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            var url = await _botService.AddTrainingUrlAsync(id, dto, user.Id);
            return Ok(url);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error adding training URL");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }

    [HttpDelete("urls/{urlId}")]
    public async Task<ActionResult> DeleteUrl(string urlId)
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            var success = await _botService.DeleteTrainingUrlAsync(urlId, user.Id);
            if (!success) return NotFound();

            return NoContent();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error deleting URL");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }

    [HttpGet("{id}/embed-code")]
    public async Task<ActionResult<string>> GetEmbedCode(string id)
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            var embedCode = await _botService.GenerateEmbedCodeAsync(id, user.Id);
            return Ok(new { embedCode });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error generating embed code");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }
}
