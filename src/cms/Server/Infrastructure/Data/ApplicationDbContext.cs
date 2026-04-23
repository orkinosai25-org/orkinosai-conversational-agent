using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using PapaganCMS.Core.Entities.Identity;

namespace PapaganCMS.Infrastructure.Data;

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
    }
}
