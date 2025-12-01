"""
Role & Permission Management Module

This module handles RBAC (Role-Based Access Control) including
role definitions, permission assignments, and access control.

Source: To be copied from orkinosaicms
"""

from .models import Role, Permission, RolePermission
from .services import RoleService, PermissionService

__all__ = ['Role', 'Permission', 'RolePermission', 'RoleService', 'PermissionService']
