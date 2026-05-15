"""Lightweight rule-based routing for multi-model chat orchestration."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class IntentClassification:
    intent: str
    complexity: str
    confidence: float
    sentiment: str
    language: str
    normalized_message: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ModelProfile:
    model_id: str
    display_name: str
    route: str
    speed: str
    quality: str
    cost_per_1k_tokens: float
    description: str


@dataclass(frozen=True)
class RoutingDecision:
    mode: str
    assigned_model: str
    fallback_model: str
    classification: IntentClassification
    create_issue: bool
    escalate_to_human: bool
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["classification"] = self.classification.to_dict()
        return payload


MODEL_PROFILES: Dict[str, ModelProfile] = {
    "small": ModelProfile(
        model_id="small",
        display_name="Small",
        route="cheap",
        speed="fast",
        quality="good",
        cost_per_1k_tokens=0.0010,
        description="Low-cost FAQ and support triage model.",
    ),
    "sumotx": ModelProfile(
        model_id="sumotx",
        display_name="SUMOTX",
        route="balanced",
        speed="balanced",
        quality="strong",
        cost_per_1k_tokens=0.0040,
        description="Balanced product support and guided assistance model.",
    ),
    "gpt-4": ModelProfile(
        model_id="gpt-4",
        display_name="GPT-4",
        route="premium",
        speed="thoughtful",
        quality="best",
        cost_per_1k_tokens=0.0200,
        description="Premium reasoning model for technical or escalated work.",
    ),
}

DEFAULT_PRIMARY_MODEL = "gpt-4"
DEFAULT_FALLBACK_MODEL = "sumotx"
DEFAULT_ROUTING_MODE = "auto"


class MessageRouter:
    """Classify messages and choose an AI model profile."""

    def preprocess_message(self, message: str) -> str:
        normalized = re.sub(r"([!?.,])\1+", r"\1", message.strip())
        normalized = re.sub(r"\s+", " ", normalized)
        return normalized

    def detect_language(self, message: str) -> str:
        turkish_chars = "çğıöşüÇĞİÖŞÜ"
        return "tr" if any(char in message for char in turkish_chars) else "en"

    def classify(self, message: str) -> IntentClassification:
        normalized = self.preprocess_message(message)
        lowered = normalized.lower()

        intent = "general_chat"
        complexity = "low"
        sentiment = "neutral"
        confidence = 0.72

        if any(keyword in lowered for keyword in ("faq", "hours", "price", "pricing", "where", "when")):
            intent = "faq"
            confidence = 0.86
        if any(keyword in lowered for keyword in ("product", "plan", "feature", "integration")):
            intent = "product_question"
            complexity = "medium"
            confidence = 0.88
        if any(keyword in lowered for keyword in ("help", "support", "can't", "cannot", "order", "login")):
            intent = "support_request"
            complexity = "medium"
            confidence = 0.84
        if any(keyword in lowered for keyword in ("bug", "broken", "error", "exception", "not working", "fails")):
            intent = "bug_report"
            complexity = "high"
            confidence = 0.91
        if any(keyword in lowered for keyword in ("complaint", "angry", "frustrated", "unhappy", "refund")):
            intent = "complaint"
            complexity = "high"
            confidence = 0.90
        if any(keyword in lowered for keyword in ("feature request", "please add", "would love", "enhancement")):
            intent = "feature_request"
            complexity = "medium"
            confidence = 0.87
        if any(keyword in lowered for keyword in ("api", "stack trace", "architecture", "technical", "security")):
            complexity = "high"
            confidence = max(confidence, 0.9)

        if any(keyword in lowered for keyword in ("urgent", "broken", "not working", "refund", "angry", "failed")):
            sentiment = "negative"
        elif any(keyword in lowered for keyword in ("thanks", "great", "love", "awesome")):
            sentiment = "positive"

        return IntentClassification(
            intent=intent,
            complexity=complexity,
            confidence=confidence,
            sentiment=sentiment,
            language=self.detect_language(normalized),
            normalized_message=normalized,
        )

    def route(
        self,
        message: str,
        preferred_model: Optional[str] = None,
        fallback_model: Optional[str] = None,
        routing_mode: Optional[str] = None,
    ) -> RoutingDecision:
        classification = self.classify(message)
        mode = self.normalize_routing_mode(routing_mode)
        preferred = self.normalize_model(preferred_model, DEFAULT_PRIMARY_MODEL)
        fallback = self.normalize_model(fallback_model, DEFAULT_FALLBACK_MODEL)

        if mode == "cheap":
            assigned_model = "small"
            reason = "Cheap routing mode prefers the low-cost model."
        elif mode == "balanced":
            assigned_model = "sumotx"
            reason = "Balanced routing mode prefers the mid-tier model."
        elif mode == "premium":
            assigned_model = "gpt-4"
            reason = "Premium routing mode prefers the strongest model."
        elif classification.intent in {"complaint", "bug_report"} or classification.complexity == "high":
            assigned_model = "gpt-4"
            reason = "Escalated or technical message routed to premium reasoning."
        elif classification.intent == "product_question":
            assigned_model = "sumotx"
            reason = "Product questions route to the balanced model."
        elif classification.intent == "faq" and classification.complexity == "low":
            assigned_model = "small"
            reason = "Simple FAQ routed to the cheapest model."
        else:
            assigned_model = preferred
            reason = "Auto routing kept the configured preferred model."

        create_issue = (
            classification.intent in {"complaint", "bug_report", "support_request"}
            and classification.confidence >= 0.8
            and classification.complexity in {"medium", "high"}
        )
        escalate_to_human = (
            (classification.intent in {"complaint", "bug_report"} and classification.confidence >= 0.8)
            or (classification.complexity == "high" and classification.confidence >= 0.85)
        )

        return RoutingDecision(
            mode=mode,
            assigned_model=assigned_model,
            fallback_model=fallback,
            classification=classification,
            create_issue=create_issue,
            escalate_to_human=escalate_to_human,
            reason=reason,
        )

    def estimate_cost(self, model_id: str, total_tokens: int) -> float:
        profile = MODEL_PROFILES[self.normalize_model(model_id, DEFAULT_PRIMARY_MODEL)]
        return round((max(total_tokens, 0) / 1000.0) * profile.cost_per_1k_tokens, 6)

    def normalize_model(self, model_id: Optional[str], fallback: str) -> str:
        if not model_id:
            return fallback
        lowered = model_id.strip().lower()
        return lowered if lowered in MODEL_PROFILES else fallback

    def normalize_routing_mode(self, routing_mode: Optional[str]) -> str:
        lowered = (routing_mode or DEFAULT_ROUTING_MODE).strip().lower()
        return lowered if lowered in {"auto", "cheap", "balanced", "premium"} else DEFAULT_ROUTING_MODE
