"""
Billing and Subscription models

Data models for subscription and billing management.
To be copied from orkinosaicms.
"""

from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
from pydantic import Field
from ..base import BaseEntity, utc_now


class SubscriptionStatus(str, Enum):
    """Subscription status"""
    ACTIVE = "active"
    TRIAL = "trial"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PAST_DUE = "past_due"


class BillingCycle(str, Enum):
    """Billing cycle frequency"""
    MONTHLY = "monthly"
    YEARLY = "yearly"
    QUARTERLY = "quarterly"


class SubscriptionTier(BaseEntity):
    """
    Subscription tier definition
    
    Defines available subscription plans with features and pricing.
    """
    name: str
    code: str  # Unique tier code (e.g., "free", "pro", "enterprise")
    description: Optional[str] = None
    price_monthly: Decimal = Decimal("0.00")
    price_yearly: Decimal = Decimal("0.00")
    features: Dict[str, Any] = Field(default_factory=dict)
    max_users: int = 1
    max_storage_gb: int = 1
    is_published: bool = True
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True


class Subscription(BaseEntity):
    """
    Organization subscription
    
    Represents an organization's subscription to a specific tier.
    """
    organization_id: str
    tier_id: str
    status: SubscriptionStatus = SubscriptionStatus.TRIAL
    billing_cycle: BillingCycle = BillingCycle.MONTHLY
    current_period_start: datetime = Field(default_factory=utc_now)
    current_period_end: Optional[datetime] = None
    trial_end: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    auto_renew: bool = True
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True


class PaymentMethod(BaseEntity):
    """
    Payment method information
    
    Stores payment method details for billing.
    """
    organization_id: str
    user_id: str  # User who added the payment method
    payment_type: str  # "card", "bank", "paypal", etc.
    is_default: bool = False
    last_four: Optional[str] = None  # Last 4 digits of card/account
    brand: Optional[str] = None  # Card brand (Visa, Mastercard, etc.)
    expiry_month: Optional[int] = None
    expiry_year: Optional[int] = None
    external_id: Optional[str] = None  # ID from payment processor
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True


class Invoice(BaseEntity):
    """
    Billing invoice
    
    Represents a billing invoice for a subscription period.
    """
    organization_id: str
    subscription_id: str
    invoice_number: str
    amount: Decimal
    tax: Decimal = Decimal("0.00")
    total: Decimal
    currency: str = "USD"
    status: str = "draft"  # draft, sent, paid, void
    due_date: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    payment_method_id: Optional[str] = None
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True
