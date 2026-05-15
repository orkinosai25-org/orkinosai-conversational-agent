using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PapaganCMS.Infrastructure.Data.Migrations
{
    /// <inheritdoc />
    public partial class EnhanceConversationsSchema : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            // ── Conversations: new columns ────────────────────────────────────

            migrationBuilder.AddColumn<string>(
                name: "TenantId",
                table: "Conversations",
                type: "nvarchar(450)",
                maxLength: 450,
                nullable: true);

            migrationBuilder.AddColumn<int>(
                name: "Status",
                table: "Conversations",
                type: "int",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AddColumn<bool>(
                name: "WasEscalated",
                table: "Conversations",
                type: "bit",
                nullable: false,
                defaultValue: false);

            migrationBuilder.AddColumn<DateTime>(
                name: "LastActivityAtUtc",
                table: "Conversations",
                type: "datetime2",
                nullable: false,
                defaultValueSql: "GETUTCDATE()");

            migrationBuilder.AddColumn<string>(
                name: "MetadataJson",
                table: "Conversations",
                type: "nvarchar(max)",
                nullable: true);

            // ── ConversationMessages: new columns ─────────────────────────────

            migrationBuilder.AddColumn<int>(
                name: "SequenceNumber",
                table: "ConversationMessages",
                type: "int",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AddColumn<string>(
                name: "Model",
                table: "ConversationMessages",
                type: "nvarchar(100)",
                maxLength: 100,
                nullable: true);

            migrationBuilder.AddColumn<int>(
                name: "TokensInput",
                table: "ConversationMessages",
                type: "int",
                nullable: true);

            migrationBuilder.AddColumn<int>(
                name: "TokensOutput",
                table: "ConversationMessages",
                type: "int",
                nullable: true);

            migrationBuilder.AddColumn<double>(
                name: "Confidence",
                table: "ConversationMessages",
                type: "float",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "MessageMetadataJson",
                table: "ConversationMessages",
                type: "nvarchar(max)",
                nullable: true);

            // ── New indexes ───────────────────────────────────────────────────

            migrationBuilder.CreateIndex(
                name: "IX_Conversations_TenantId",
                table: "Conversations",
                column: "TenantId");

            migrationBuilder.CreateIndex(
                name: "IX_ConversationMessages_ConversationId_SequenceNumber",
                table: "ConversationMessages",
                columns: new[] { "ConversationId", "SequenceNumber" });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropIndex(
                name: "IX_ConversationMessages_ConversationId_SequenceNumber",
                table: "ConversationMessages");

            migrationBuilder.DropIndex(
                name: "IX_Conversations_TenantId",
                table: "Conversations");

            migrationBuilder.DropColumn(name: "MessageMetadataJson", table: "ConversationMessages");
            migrationBuilder.DropColumn(name: "Confidence",           table: "ConversationMessages");
            migrationBuilder.DropColumn(name: "TokensOutput",         table: "ConversationMessages");
            migrationBuilder.DropColumn(name: "TokensInput",          table: "ConversationMessages");
            migrationBuilder.DropColumn(name: "Model",                table: "ConversationMessages");
            migrationBuilder.DropColumn(name: "SequenceNumber",       table: "ConversationMessages");

            migrationBuilder.DropColumn(name: "MetadataJson",         table: "Conversations");
            migrationBuilder.DropColumn(name: "LastActivityAtUtc",    table: "Conversations");
            migrationBuilder.DropColumn(name: "WasEscalated",        table: "Conversations");
            migrationBuilder.DropColumn(name: "Status",               table: "Conversations");
            migrationBuilder.DropColumn(name: "TenantId",             table: "Conversations");
        }
    }
}
