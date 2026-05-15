using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PapaganCMS.Infrastructure.Data.Migrations
{
    /// <inheritdoc />
    public partial class AddConversationTrainingMetadata : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            // ── Training-ready metadata columns ───────────────────────────────

            migrationBuilder.AddColumn<string>(
                name: "Summary",
                table: "Conversations",
                type: "nvarchar(1000)",
                maxLength: 1000,
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Intent",
                table: "Conversations",
                type: "nvarchar(200)",
                maxLength: 200,
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Sentiment",
                table: "Conversations",
                type: "nvarchar(50)",
                maxLength: 50,
                nullable: true);

            migrationBuilder.AddColumn<double>(
                name: "SentimentScore",
                table: "Conversations",
                type: "float",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Category",
                table: "Conversations",
                type: "nvarchar(100)",
                maxLength: 100,
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "EscalationReason",
                table: "Conversations",
                type: "nvarchar(500)",
                maxLength: 500,
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "AnswerQuality",
                table: "Conversations",
                type: "nvarchar(50)",
                maxLength: 50,
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "ResolutionSource",
                table: "Conversations",
                type: "nvarchar(50)",
                maxLength: 50,
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(name: "Summary",          table: "Conversations");
            migrationBuilder.DropColumn(name: "Intent",           table: "Conversations");
            migrationBuilder.DropColumn(name: "Sentiment",        table: "Conversations");
            migrationBuilder.DropColumn(name: "SentimentScore",   table: "Conversations");
            migrationBuilder.DropColumn(name: "Category",         table: "Conversations");
            migrationBuilder.DropColumn(name: "EscalationReason", table: "Conversations");
            migrationBuilder.DropColumn(name: "AnswerQuality",    table: "Conversations");
            migrationBuilder.DropColumn(name: "ResolutionSource", table: "Conversations");
        }
    }
}
