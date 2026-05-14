using Azure.Storage.Blobs;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using OrkinosaiCMS.Core.Interfaces.Services;
using PapaganCMS.Client.Pages;
using PapaganCMS.Components;
using SiteChatCMS.Core.Entities.Identity;
using SiteChatCMS.Core.Interfaces.Services;
using SiteChatCMS.Infrastructure.Data;
using SiteChatCMS.Infrastructure.Services;
using SiteChatCMS.Infrastructure.Services.Adverts;
using SiteChatCMS.Infrastructure.Services.Conversations;
using SiteChatCMS.Infrastructure.Services.Issues;
using SiteChatCMS.Infrastructure.Services.Auth;
using SiteChatCMS.Infrastructure.Services.Bots;
using SiteChatCMS.Infrastructure.Services.Onboarding;
using SiteChatCMS.Infrastructure.Services.Subscriptions;

var builder = WebApplication.CreateBuilder(args);

// Add database context
// Development: use InMemory for fast iteration without a SQL instance.
// Production:  use Azure SQL Server — connection string supplied via
//              App Service configuration (ConnectionStrings:Default) or
//              the CONNECTIONSTRINGS__DEFAULT environment variable.
builder.Services.AddDbContext<ApplicationDbContext>(options =>
{
    if (builder.Environment.IsDevelopment())
    {
        options.UseInMemoryDatabase("SiteChatCMS");
    }
    else
    {
        var connectionString = builder.Configuration.GetConnectionString("Default")
            ?? throw new InvalidOperationException(
                "ConnectionStrings:Default is not set. " +
                "Configure it in Azure App Service → Configuration → Connection strings.");
        options.UseSqlServer(connectionString);
    }
});

// Register Azure Blob Storage client (used for training-document uploads).
// Connection string is read from Azure:BlobStorage:ConnectionString — set this
// in App Service → Configuration → Application settings.
var blobConnectionString = builder.Configuration["Azure:BlobStorage:ConnectionString"];
if (!string.IsNullOrWhiteSpace(blobConnectionString))
{
    builder.Services.AddSingleton(new BlobServiceClient(blobConnectionString));
}

// Add ASP.NET Identity
builder.Services.AddIdentity<ApplicationUser, IdentityRole>(options =>
{
    // Password settings
    options.Password.RequireDigit = true;
    options.Password.RequireLowercase = true;
    options.Password.RequireUppercase = true;
    options.Password.RequireNonAlphanumeric = false;
    options.Password.RequiredLength = 8;

    // User settings
    options.User.RequireUniqueEmail = true;

    // Sign in settings
    options.SignIn.RequireConfirmedEmail = false;
})
.AddEntityFrameworkStores<ApplicationDbContext>()
.AddDefaultTokenProviders();

// Configure cookie authentication
builder.Services.ConfigureApplicationCookie(options =>
{
    options.Cookie.HttpOnly = true;
    options.ExpireTimeSpan = TimeSpan.FromDays(7);
    options.LoginPath = "/login";
    options.LogoutPath = "/logout";
    options.AccessDeniedPath = "/access-denied";
    options.SlidingExpiration = true;
});

// Add services to the container.
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents()
    .AddInteractiveWebAssemblyComponents();

// Add API controllers
builder.Services.AddControllers()
    .AddNewtonsoftJson(); // Required for Stripe webhook processing

// Add HttpContextAccessor
builder.Services.AddHttpContextAccessor();

// Register a named HttpClient used by Blazor Server components (Pricing, Subscription, etc.).
// A scoped registration wraps IHttpClientFactory so that the BaseAddress is resolved
// dynamically from the incoming HTTP request, ensuring the correct host/scheme is used
// on every environment (local dev, Azure, etc.) without any hardcoded URLs.
builder.Services.AddHttpClient("BlazorServer");
builder.Services.AddScoped(sp =>
{
    var factory = sp.GetRequiredService<IHttpClientFactory>();
    var httpContextAccessor = sp.GetRequiredService<IHttpContextAccessor>();
    var client = factory.CreateClient("BlazorServer");
    var request = httpContextAccessor.HttpContext?.Request;
    if (request != null)
    {
        client.BaseAddress = new Uri($"{request.Scheme}://{request.Host}/");
    }
    return client;
});

// Configure HttpClient for chat agent backend
var backendUrl = builder.Configuration["ChatAgent:BackendUrl"] ?? "http://localhost:5000";
builder.Services.AddHttpClient("ChatBackend", client =>
{
    client.BaseAddress = new Uri(backendUrl);
    client.Timeout = TimeSpan.FromSeconds(30);
});

// Register application services
builder.Services.AddScoped<IAuthService, AuthService>();
builder.Services.AddScoped<IBotService, BotService>();
builder.Services.AddScoped<IOnboardingService, OnboardingService>();

// Register subscription services (using OrkinosaiCMS namespace)
builder.Services.AddSingleton<OrkinosaiCMS.Core.Interfaces.Services.IUserService, UserService>();
builder.Services.AddSingleton<ICustomerService, CustomerService>();
builder.Services.AddSingleton<ISubscriptionService, SubscriptionService>();
builder.Services.AddScoped<IStripeService, StripeService>();

// Register advert service
builder.Services.AddSingleton<IAdvertService, AdvertService>();

// Register issue service (scoped — depends on the scoped ApplicationDbContext)
builder.Services.AddScoped<IIssueService, IssueService>();

// Register conversation service (scoped — depends on the scoped ApplicationDbContext)
builder.Services.AddScoped<IConversationService, ConversationService>();

var app = builder.Build();

// EF Core migrations are applied by the CI/CD pipeline (GitHub Actions) before each
// deployment — see .github/workflows/main_papagan.yml (migrate job) and
// .github/workflows/azure-provision.yml (migrate job).
// No automatic migration is run at startup to avoid race conditions during
// rolling restarts and to keep migration failures visible in deployment logs
// rather than silently swallowed in application logs.

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseWebAssemblyDebugging();
}
else
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}
app.UseStatusCodePagesWithReExecute("/not-found", createScopeForStatusCodePages: true);
app.UseHttpsRedirection();

// Add authentication and authorization
app.UseAuthentication();
app.UseAuthorization();

app.UseAntiforgery();

app.MapStaticAssets();
app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode()
    .AddInteractiveWebAssemblyRenderMode()
    .AddAdditionalAssemblies(typeof(PapaganCMS.Client._Imports).Assembly);

// Map API controllers
app.MapControllers();

app.Run();
