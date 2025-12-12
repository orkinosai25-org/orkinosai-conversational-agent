using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using PapaganCMS.Core.Interfaces.Services;
using PapaganCMS.Shared.DTOs.Onboarding;

namespace PapaganCMS.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class OnboardingController : ControllerBase
{
    private readonly IOnboardingService _onboardingService;
    private readonly IAuthService _authService;
    private readonly ILogger<OnboardingController> _logger;

    public OnboardingController(
        IOnboardingService onboardingService,
        IAuthService authService,
        ILogger<OnboardingController> logger)
    {
        _onboardingService = onboardingService;
        _authService = authService;
        _logger = logger;
    }

    [HttpGet("progress")]
    public async Task<ActionResult<OnboardingProgressDto>> GetProgress()
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            var progress = await _onboardingService.GetProgressAsync(user.Id);
            return Ok(progress);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting onboarding progress");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }

    [HttpPost("complete-step")]
    public async Task<ActionResult<OnboardingProgressDto>> CompleteStep([FromBody] CompleteStepDto dto)
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            var progress = await _onboardingService.CompleteStepAsync(user.Id, dto.Step);
            return Ok(progress);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error completing onboarding step");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }

    [HttpPost("skip")]
    public async Task<ActionResult> Skip()
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            await _onboardingService.SkipOnboardingAsync(user.Id);
            return Ok(new { success = true, message = "Onboarding skipped" });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error skipping onboarding");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }

    [HttpPost("setup-organization")]
    public async Task<ActionResult> SetupOrganization([FromBody] OrganizationSetupDto dto)
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            var success = await _onboardingService.SetupOrganizationAsync(user.Id, dto);
            if (!success)
            {
                return BadRequest(new { message = "Failed to setup organization" });
            }

            return Ok(new { success = true, message = "Organization setup complete" });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error setting up organization");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }

    [HttpPost("setup-bot")]
    public async Task<ActionResult> SetupBot([FromBody] BotSetupDto dto)
    {
        try
        {
            var user = await _authService.GetCurrentUserAsync();
            if (user == null) return Unauthorized();

            var success = await _onboardingService.SetupFirstBotAsync(user.Id, dto);
            if (!success)
            {
                return BadRequest(new { message = "Failed to setup bot" });
            }

            return Ok(new { success = true, message = "Bot setup complete" });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error setting up bot");
            return StatusCode(500, new { message = "An error occurred" });
        }
    }
}
