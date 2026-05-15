using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using SiteChatCMS.Core.Entities.Conversations;
using SiteChatCMS.Core.Entities.Identity;
using SiteChatCMS.Core.Entities.Issues;

namespace SiteChatCMS.Infrastructure.Data;

/// <summary>
/// Application database context with ASP.NET Identity
/// </summary>
public class ApplicationDbContext : IdentityDbContext<ApplicationUser>
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<Organization> Organizations { get; set; }
    public DbSet<Bot> Bots { get; set; }
    public DbSet<TrainingDocument> TrainingDocuments { get; set; }
    public DbSet<TrainingUrl> TrainingUrls { get; set; }
    public DbSet<Issue> Issues { get; set; }
    public DbSet<Conversation> Conversations { get; set; }
    public DbSet<ConversationMessage> ConversationMessages { get; set; }

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);

        // Organization configuration
        builder.Entity<Organization>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).IsRequired().HasMaxLength(200);
            entity.HasMany(e => e.Users)
                .WithOne(e => e.Organization)
                .HasForeignKey(e => e.OrganizationId)
                .OnDelete(DeleteBehavior.SetNull);
            entity.HasMany(e => e.Bots)
                .WithOne(e => e.Organization)
                .HasForeignKey(e => e.OrganizationId)
                .OnDelete(DeleteBehavior.Cascade);
        });

        // ApplicationUser configuration
        builder.Entity<ApplicationUser>(entity =>
        {
            entity.Property(e => e.DisplayName).HasMaxLength(200);
            entity.Property(e => e.FirstName).HasMaxLength(100);
            entity.Property(e => e.LastName).HasMaxLength(100);
            entity.HasMany(e => e.Bots)
                .WithOne(e => e.User)
                .HasForeignKey(e => e.UserId)
                .OnDelete(DeleteBehavior.Cascade);
        });

        // Bot configuration
        builder.Entity<Bot>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).IsRequired().HasMaxLength(200);
            entity.Property(e => e.SiteUrl).HasMaxLength(1000);
            entity.Property(e => e.SeatSlug).IsRequired().HasMaxLength(200);
            entity.Property(e => e.UserId).IsRequired();
            entity.Property(e => e.PrimaryModel).IsRequired().HasMaxLength(50);
            entity.Property(e => e.FallbackModel).IsRequired().HasMaxLength(50);
            entity.Property(e => e.RoutingMode).IsRequired().HasMaxLength(50);
            entity.HasIndex(e => e.SeatSlug).IsUnique();
            entity.HasMany(e => e.TrainingDocuments)
                .WithOne(e => e.Bot)
                .HasForeignKey(e => e.BotId)
                .OnDelete(DeleteBehavior.Cascade);
            entity.HasMany(e => e.TrainingUrls)
                .WithOne(e => e.Bot)
                .HasForeignKey(e => e.BotId)
                .OnDelete(DeleteBehavior.Cascade);
        });

        // TrainingDocument configuration
        builder.Entity<TrainingDocument>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.FileName).IsRequired().HasMaxLength(500);
            entity.Property(e => e.BotId).IsRequired();
        });

        // TrainingUrl configuration
        builder.Entity<TrainingUrl>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Url).IsRequired().HasMaxLength(2000);
            entity.Property(e => e.BotId).IsRequired();
        });

        // Issue configuration
        builder.Entity<Issue>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Title).IsRequired().HasMaxLength(500);
            entity.Property(e => e.Description).IsRequired().HasMaxLength(4000);
            entity.Property(e => e.SubmitterName).IsRequired().HasMaxLength(200);
            entity.Property(e => e.SubmitterEmail).IsRequired().HasMaxLength(300);
            entity.Property(e => e.AdminNotes).HasMaxLength(4000);
            entity.Property(e => e.Type).IsRequired();
            entity.Property(e => e.Priority).IsRequired();
            entity.Property(e => e.Status).IsRequired();
            entity.HasIndex(e => e.Status);
            entity.HasIndex(e => e.CreatedAt);
        });

        // Conversation configuration
        builder.Entity<Conversation>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.SessionId).IsRequired().HasMaxLength(200);
            entity.Property(e => e.TenantId).HasMaxLength(450);
            entity.Property(e => e.BotId).HasMaxLength(450);
            entity.Property(e => e.SeatSlug).HasMaxLength(200);
            entity.Property(e => e.SourceUrl).HasMaxLength(2000);
            entity.Property(e => e.Language).HasMaxLength(20);
            entity.Property(e => e.VisitorName).HasMaxLength(200);
            entity.Property(e => e.VisitorEmail).HasMaxLength(254);
            entity.Property(e => e.Status).IsRequired();
            entity.Property(e => e.Summary).HasMaxLength(1000);
            entity.Property(e => e.Intent).HasMaxLength(200);
            entity.Property(e => e.Sentiment).HasMaxLength(50);
            entity.Property(e => e.Category).HasMaxLength(100);
            entity.Property(e => e.EscalationReason).HasMaxLength(500);
            entity.Property(e => e.AnswerQuality).HasMaxLength(50);
            entity.Property(e => e.ResolutionSource).HasMaxLength(50);
            entity.HasIndex(e => e.SessionId).IsUnique();
            entity.HasIndex(e => e.SeatSlug);
            entity.HasIndex(e => e.TenantId);
            entity.HasIndex(e => e.CreatedAt);
            entity.HasMany(e => e.Messages)
                .WithOne(e => e.Conversation)
                .HasForeignKey(e => e.ConversationId)
                .OnDelete(DeleteBehavior.Cascade);
            entity.HasOne(e => e.Ticket)
                .WithMany()
                .HasForeignKey(e => e.TicketId)
                .OnDelete(DeleteBehavior.SetNull);
        });

        // ConversationMessage configuration
        builder.Entity<ConversationMessage>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Role).IsRequired().HasMaxLength(50);
            entity.Property(e => e.Content).IsRequired().HasMaxLength(50000);
            entity.Property(e => e.Model).HasMaxLength(100);
            entity.HasIndex(e => e.ConversationId);
            entity.HasIndex(e => new { e.ConversationId, e.SequenceNumber });
            entity.HasIndex(e => e.Timestamp);
        });
    }
}
